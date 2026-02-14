#!/usr/bin/env python3
"""
Dual-Storage Distribution Script v2.1
- Scans project for large files (>50MB).
- Uploads large files to HuggingFace (hfhfn/full_stack_resources).
- Removes large files from Git index (git rm --cached) and adds to .gitignore.
- Generates data/file_manifest.json for the web interface.
"""
import os
import sys
import json
import subprocess
from pathlib import Path

# --- Configuration ---
SIZE_THRESHOLD = 50 * 1024 * 1024  # 50MB
HF_REPO_ID = "hfhfn/full_stack_resources"  # Agent: Replace this!
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Exclude directories
EXCLUDE_DIRS = {'.git', '.idea', '.vscode', 'venv', 'node_modules', '__pycache__', '.serena'}

def get_file_size(path):
    return path.stat().st_size

def run_git_cmd(args):
    try:
        subprocess.run(['git'] + args, cwd=PROJECT_ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def scan_files():
    large_files = []
    small_files = []
    print(f"🔍 Scanning files (Threshold: {SIZE_THRESHOLD/1024/1024:.0f}MB)...")

    for path in PROJECT_ROOT.rglob('*'):
        if not path.is_file(): continue
        parts = path.relative_to(PROJECT_ROOT).parts
        if any(p.startswith('.') and p not in ['.gitignore', '.gitattributes'] for p in parts): continue
        if any(ex in parts for ex in EXCLUDE_DIRS): continue

        try:
            size = get_file_size(path)
            if size >= SIZE_THRESHOLD:
                large_files.append(path)
            else:
                small_files.append(path)
        except OSError: pass

    return large_files, small_files

def upload_to_hf(files):
    if not files: return
    print(f"🚀 Uploading {len(files)} large files to HuggingFace ({HF_REPO_ID})...")
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        user = api.whoami()
        print(f"   Logged in as: {user['name']}")

        # Ensure the repo exists
        try:
            api.create_repo(repo_id=HF_REPO_ID, repo_type="dataset", exist_ok=True)
        except Exception as e:
            print(f"   ⚠️ Could not create/check repo {HF_REPO_ID}: {e}")

        for file_path in files:
            rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
            print(f"   📤 Uploading: {rel_path} ({get_file_size(file_path)/1024/1024:.1f} MB)")
            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=rel_path,
                repo_id=HF_REPO_ID,
                repo_type="dataset",
                commit_message=f"Upload large file: {os.path.basename(rel_path)}"
            )
        print("✅ Upload complete")
        return True
    except ImportError:
        print("❌ Error: huggingface_hub not installed. Run: pip install huggingface_hub")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return False

def update_gitignore_and_git(large_files):
    if not large_files: return
    print("\n🛡️  Processing Git tracking & .gitignore...")
    gitignore_path = PROJECT_ROOT / '.gitignore'
    existing_rules = set()
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_rules = {line.strip() for line in f if line.strip() and not line.startswith('#')}

    new_rules = []
    for file_path in large_files:
        rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
        if rel_path not in existing_rules:
            new_rules.append(rel_path)
        print(f"   🚫 Git stop tracking: {rel_path}")
        run_git_cmd(['rm', '--cached', str(file_path)])

    if new_rules:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write("\n# [Auto] Large files managed by HuggingFace\n")
            for rule in new_rules:
                f.write(f"{rule}\n")
        print(f"   📝 Added {len(new_rules)} rules to .gitignore")

def generate_manifest(large_files):
    print("\n📋 Generating file manifest (data/file_manifest.json)...")
    manifest = {"hf_repo_id": HF_REPO_ID, "files": []}

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
    print("✅ Manifest generated")

def main():
    large, small = scan_files()
    print(f"   -> Found {len(large)} large files, {len(small)} small files")

    if large:
        upload_to_hf(large)
        update_gitignore_and_git(large)
        generate_manifest(large)
    else:
        print("🎉 No files > 50MB found.")

    print("\n✅ All steps complete! Ready for git push.")

if __name__ == "__main__":
    main()
