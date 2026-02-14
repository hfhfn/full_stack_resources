#!/usr/bin/env python3
"""
自动分发脚本 v2.0 (Ported from rec_sys_guide)
核心功能：
1. 扫描全项目文件
2. 大文件 (>50MB) -> 上传 HuggingFace -> 写入 .gitignore -> 从 Git 索引移除
3. 生成 data/file_manifest.json
"""
import os
import sys
import json
import subprocess
from pathlib import Path

# --- 配置 ---
SIZE_THRESHOLD = 50 * 1024 * 1024  # 50MB
# TODO: 如有需要，请修改下方的 HuggingFace 仓库 ID
HF_REPO_ID = "hfhfn/full_stack_resources"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 排除目录
EXCLUDE_DIRS = {'.git', '.idea', '.vscode', 'venv', 'node_modules', '__pycache__', '.serena'}

def get_file_size(path):
    return path.stat().st_size

def run_git_cmd(args):
    """运行 git 命令，忽略错误"""
    try:
        subprocess.run(['git'] + args, cwd=PROJECT_ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def scan_files():
    large_files = []
    small_files = []
    
    print(f"🔍 正在扫描文件 (阈值: {SIZE_THRESHOLD/1024/1024:.0f}MB)...")
    
    for path in PROJECT_ROOT.rglob('*'):
        if not path.is_file():
            continue
            
        # 排除路径
        parts = path.relative_to(PROJECT_ROOT).parts
        if any(p.startswith('.') and p != '.gitignore' and p != '.gitattributes' for p in parts):
            continue
        if any(ex in parts for ex in EXCLUDE_DIRS):
            continue
            
        try:
            size = get_file_size(path)
            if size >= SIZE_THRESHOLD:
                large_files.append(path)
            else:
                small_files.append(path)
        except OSError:
            pass
            
    return large_files, small_files

def get_hf_api():
    try:
        from huggingface_hub import HfApi
        return HfApi()
    except ImportError:
        print("❌ 错误: 未安装 huggingface_hub。请运行: pip install huggingface_hub")
        sys.exit(1)

def upload_to_hf(api, files):
    if not files:
        return
    
    print(f"\n🚀 正在上传 {len(files)} 个大文件到 HuggingFace ({HF_REPO_ID})...")
    try:
        # 验证登录状态
        user = api.whoami()
        print(f"   已登录用户: {user['name']}")
        
        for file_path in files:
            rel_path = file_path.relative_to(PROJECT_ROOT).as_posix() # 使用正斜杠
            print(f"   📤 上传: {rel_path} ({get_file_size(file_path)/1024/1024:.1f} MB)")
            
            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=rel_path,
                repo_id=HF_REPO_ID,
                repo_type="dataset",
                commit_message=f"Upload large file: {os.path.basename(rel_path)}"
            )
        print("✅ 上传完成")
        return True
    except ImportError:
        print("❌ 错误: 未安装 huggingface_hub。请运行: pip install huggingface_hub")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 上传出错: {str(e)}")
        return False

def sync_hf_deletions(api, local_large_files):
    """同步删除：如果文件在 HF 上存在但本地已删除，则从 HF 移除"""
    print(f"\n🗑️  正在检查同步删除 ({HF_REPO_ID})...")
    try:
        # 获取 HF 上的文件列表
        remote_files = api.list_repo_files(repo_id=HF_REPO_ID, repo_type="dataset")
        
        # 本地当前的大文件路径（相对于项目根目录的 posix 路径）
        local_rel_paths = {f.relative_to(PROJECT_ROOT).as_posix() for f in local_large_files}
        
        # 找出需要删除的文件：在 HF 上但在本地 RelPaths 中不存在
        # 注意：排除一些特殊文件如 .gitattributes, README.md 等
        to_delete = []
        for remote_file in remote_files:
            if remote_file in ['.gitattributes', 'README.md', '.gitignore']:
                continue
            if remote_file not in local_rel_paths:
                to_delete.append(remote_file)
        
        if to_delete:
            print(f"   发现 {len(to_delete)} 个冗余文件，准备从 HF 删除...")
            for file_path in to_delete:
                print(f"   ␡ 删除: {file_path}")
                api.delete_file(
                    path_in_repo=file_path,
                    repo_id=HF_REPO_ID,
                    repo_type="dataset",
                    commit_message=f"Sync delete: {os.path.basename(file_path)}"
                )
            print("   ✅ HF 同步删除完成")
        else:
            print("   ✨ HF 仓库已是最新，无需删除")
            
    except Exception as e:
        print(f"   ⚠️ 同步删除失败: {str(e)}")

def update_gitignore_and_git(large_files):
    if not large_files:
        return

    print("\\n🛡️  正在处理 Git 追踪及 .gitignore...")
    gitignore_path = PROJECT_ROOT / '.gitignore'
    
    # 读取现有规则
    existing_rules = set()
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_rules = {line.strip() for line in f if line.strip() and not line.startswith('#')}

    new_rules = []
    
    for file_path in large_files:
        rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
        
        # 1. 如果不在 gitignore 中，则添加
        if rel_path not in existing_rules:
            new_rules.append(rel_path)
            
        # 2. 关键步骤：从 git 索引中强制移除（保留本地文件）
        # 这一步保证了 git push 不会包含这个大文件
        print(f"   🚫 Git 停止追踪: {rel_path}")
        run_git_cmd(['rm', '--cached', str(file_path)])

    # 追加新规则到 .gitignore
    if new_rules:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write("\n# [Auto] Large files managed by HuggingFace\n")
            for rule in new_rules:
                f.write(f"{rule}\n")
        print(f"   📝 已将 {len(new_rules)} 个大文件写入 .gitignore")

def generate_manifest(large_files):
    print("\\n📋 生成文件清单 (data/file_manifest.json)...")
    manifest = {
        "hf_repo_id": HF_REPO_ID,
        "files": []
    }
    
    for file_path in large_files:
        rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
        size_mb = get_file_size(file_path) / (1024 * 1024)
        hf_url = f"https://huggingface.co/datasets/{HF_REPO_ID}/resolve/main/{rel_path}"
        
        manifest["files"].append({
            "name": file_path.name,
            "path": rel_path,
            "size_mb": round(size_mb, 2),
            "url": hf_url
        })
        
    manifest_dir = PROJECT_ROOT / 'data'
    manifest_dir.mkdir(exist_ok=True)
    
    with open(manifest_dir / 'file_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("✅ 清单生成完毕")

def main():
    # 1. 扫描本地文件
    large, small = scan_files()
    print(f"   -> 发现 {len(large)} 个大文件, {len(small)} 个小文件")
    
    # 2. 获取 API 实例
    api = get_hf_api()
    
    # 3. 同步删除 (HF 有但本地没有的文件)
    # 我们根据扫描结果对比 HF
    sync_hf_deletions(api, large)
    
    # 4. 上传新大文件
    if large:
        upload_to_hf(api, large)
        
        # 5. 处理 Git (移除追踪 + 更新 ignore)
        update_gitignore_and_git(large)
        
        # 6. 生成清单
        generate_manifest(large)
    else:
        print("🎉 没有发现大于 50MB 的文件。")
        # 即使没有大文件，也可能需要清理清单（如果之前有现在没了）
        generate_manifest([])

    print("\n✅ 所有步骤完成！")
    print("👉 现在你可以放心地运行: git add . && git commit -m 'update' && git push")

if __name__ == "__main__":
    main()
