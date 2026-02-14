# GitHub + HuggingFace Dual-Storage Templates

This file contains the template code required for the `github-hf-dual-storage` skill. The Agent should read this file and extract the relevant code blocks to create the necessary files in the user's project.

## 1. Distribution Script (`scripts/distribute_files.py`)

**Usage:**

- Replace `${HF_USERNAME}` and `${HF_REPO_NAME}` with actual values.
- Save to `scripts/distribute_files.py`.

```python
#!/usr/bin/env python3
"""
Dual-Storage Distribution Script v2.1
- Scans project for large files (>50MB).
- Uploads large files to HuggingFace (${HF_USERNAME}/${HF_REPO_NAME}).
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
HF_REPO_ID = "${HF_USERNAME}/${HF_REPO_NAME}"  # Agent: Replace this!
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Exclude directories
EXCLUDE_DIRS = {'.git', '.idea', '.vscode', 'venv', 'node_modules', '__pycache__', '.serena', '.github'}

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
    print(f"\\n🚀 Uploading {len(files)} large files to HuggingFace ({HF_REPO_ID})...")
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        user = api.whoami()
        print(f"   Logged in as: {user['name']}")

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
    print("\\n🛡️  Processing Git tracking & .gitignore...")
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
    print("\\n📋 Generating file manifest (data/file_manifest.json)...")
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

    print("\\n✅ All steps complete! Ready for git push.")

if __name__ == "__main__":
    main()
```

## 2. Windows Setup Script (`scripts/setup.bat`)

**Usage:**

- Save to `scripts/setup.bat` (Windows).

```batch
@echo off
REM Setup Script: Checks env + installs deps + first run (Windows)
setlocal enabledelayedexpansion
chcp 65001 >nul

echo.
echo ============================================
echo   Auto-Distribution Setup
echo ============================================
echo.

REM --- 1. Python Check ---
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    pause
    exit /b 1
)

REM --- 2. Dependencies ---
echo.
echo [2/5] Installing huggingface_hub...
pip install -q huggingface_hub

REM --- 3. HF Auth ---
echo.
echo [3/5] HuggingFace Authentication
if defined HF_TOKEN goto :skip_hf_auth
python -c "from huggingface_hub import HfApi; HfApi().whoami()" >nul 2>&1
if not errorlevel 1 goto :skip_hf_auth

echo   HF Auth not found.
echo   a) Login now
echo   b) Skip (No upload)
set /p hf_choice="  Select [a/b]: "
if /i "%hf_choice%"=="a" (
    huggingface-cli login
) else (
    echo   Skipping auth.
)

:skip_hf_auth

REM --- 4. Run Script ---
echo.
echo [4/5] Running distribution...
cd /d "%~dp0.."
python scripts\distribute_files.py

REM --- 5. Initial Commit ---
echo.
echo [5/5] Committing to Git...
git add .
git diff --cached --quiet
if errorlevel 1 (
    echo.
    set /p commit_msg="Enter commit message (default: Auto update): "
    if "!commit_msg!"=="" set commit_msg=Auto update
    git commit -m "!commit_msg!"
    git push origin main
) else (
    echo   No changes to commit.
)

pause
```

## 3. Linux/Mac Setup Script (`scripts/setup.sh`)

**Usage:**

- Save to `scripts/setup.sh`.
- Run `chmod +x scripts/setup.sh`.

```bash
#!/bin/bash
# Setup Script (Linux/macOS)

echo ""
echo "============================================"
echo "  Auto-Distribution Setup"
echo "============================================"
echo ""

# --- 1. Python Check ---
echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found."
    exit 1
fi

# --- 2. Install Deps ---
echo ""
echo "[2/5] Installing huggingface_hub..."
pip3 install -q huggingface_hub

# --- 3. HF Auth ---
echo ""
echo "[3/5] HuggingFace Auth"
if python3 -c "from huggingface_hub import HfApi; HfApi().whoami()" &> /dev/null; then
    echo "  Logged in."
else
    echo "  Not logged in."
    read -p "  Login now? (y/n) [n]: " login_choice
    if [[ "$login_choice" == "y" || "$login_choice" == "Y" ]]; then
        huggingface-cli login
    else
        echo "  Skipping login."
    fi
fi

# --- 4. Run Script ---
echo ""
echo "[4/5] Running distribution..."
cd "$(dirname "$0")/.."
python3 scripts/distribute_files.py

# --- 5. Push ---
echo ""
echo "[5/5] Pushing to GitHub..."
git add .
if ! git diff --cached --quiet; then
    read -p "  Enter commit message (default: Auto update): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Auto update"
    fi
    git commit -m "$commit_msg"
    git push origin main
else
    echo "  No changes to push."
fi
```

## 4. Web Interface (`index.html`)

**Usage:**

- Replace `${GITHUB_USERNAME}` and `${GITHUB_REPO_NAME}`.
- Save to `index.html`.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>${GITHUB_REPO_NAME} File Browser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body {
        font-family:
          -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
          Arial, sans-serif;
        max-width: 1000px;
        margin: 40px auto;
        padding: 0 20px;
        background: #f8f9fa;
      }
      .container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 30px;
      }
      h1 {
        color: #1a73e8;
        border-bottom: 2px solid #e8f0fe;
        padding-bottom: 15px;
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      h1:before {
        content: "📚";
        font-size: 32px;
      }

      /* 搜索框样式 */
      .search-box {
        margin: 20px 0;
        display: flex;
        gap: 10px;
      }
      #searchInput {
        flex: 1;
        padding: 12px 16px;
        border: 2px solid #e8f0fe;
        border-radius: 8px;
        font-size: 16px;
        transition: border-color 0.2s;
        outline: none;
      }
      #searchInput:focus {
        border-color: #1a73e8;
      }
      #searchInput::placeholder {
        color: #9aa0a6;
      }
      .clear-search {
        padding: 0 16px;
        background: #f1f3f4;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        color: #5f6368;
        transition: background 0.2s;
      }
      .clear-search:hover {
        background: #e8eaed;
      }

      .file-tree {
        margin-top: 20px;
        min-height: 200px;
      }

      /* 文件夹样式 */
      .folder {
        margin: 4px 0;
      }
      .folder-header {
        padding: 6px 8px;
        border-radius: 4px;
        cursor: pointer;
        user-select: none;
        display: flex;
        align-items: center;
        gap: 6px;
        color: #e36209;
        font-weight: 500;
        transition: background 0.2s;
      }
      .folder-header:hover {
        background: #f1f8ff;
      }
      .folder-header .toggle-icon {
        display: inline-block;
        width: 16px;
        text-align: center;
        font-size: 12px;
        color: #5f6368;
      }
      .folder-header .folder-icon {
        font-size: 18px;
      }
      .folder-children {
        margin-left: 24px;
        padding-left: 8px;
        border-left: 1px dashed #dadce0;
      }
      .folder-children.collapsed {
        display: none;
      }

      /* 文件样式 */
      .file-item {
        padding: 6px 8px 6px 32px;
        border-radius: 4px;
        transition: background 0.2s;
        position: relative;
      }
      .file-item:hover {
        background: #f1f8ff;
      }
      .file-item a {
        text-decoration: none;
        color: #1a73e8;
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }
      .file-item a:hover {
        text-decoration: underline;
      }
      .file-icon {
        font-size: 16px;
      }
      .hf-badge {
        display: inline-block;
        margin-left: 6px;
        font-size: 11px;
        background: #fef3c7;
        color: #92400e;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: 500;
        border: 1px solid #fcd34d;
      }

      /* 匹配高亮 */
      .file-item.highlight {
        background: #fff3e0;
        border-left: 3px solid #f9ab00;
      }
      .folder-header.highlight {
        background: #fff3e0;
      }

      /* 空状态和加载 */
      .loading,
      .error,
      .no-results {
        padding: 40px;
        text-align: center;
        color: #5f6368;
      }
      .error {
        color: #d93025;
      }
      .stats {
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #e8f0fe;
        color: #5f6368;
        font-size: 14px;
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>${GITHUB_REPO_NAME}</h1>

      <!-- 搜索框 -->
      <div class="search-box">
        <input
          type="text"
          id="searchInput"
          placeholder="🔍 搜索文件或文件夹... (支持拼音)"
          autocomplete="off"
        />
        <button class="clear-search" id="clearSearch">清除</button>
      </div>

      <div id="file-list" class="file-tree">
        <div class="loading">📂 加载文件列表中...</div>
      </div>

      <div id="stats" class="stats"></div>
    </div>

    <script>
      // 配置信息
      const username = "${GITHUB_USERNAME}";
      const repo = "${GITHUB_REPO_NAME}";
      const branch = "main";

      // 存储所有文件的原始数据
      let allFilesData = [];
      // 存储当前的搜索关键词
      let currentSearchTerm = "";
      // 存储 HuggingFace 大文件映射
      let hfFileMap = {};

      // 获取文件图标（根据扩展名）
      function getFileIcon(filename) {
        const ext = filename.split(".").pop().toLowerCase();
        const iconMap = {
          // 文档类
          pdf: "📄",
          doc: "📘",
          docx: "📘",
          txt: "📃",
          md: "📝",
          // 代码类
          html: "🌐",
          htm: "🌐",
          css: "🎨",
          js: "⚡",
          py: "🐍",
          java: "☕",
          cpp: "⚙️",
          c: "⚙️",
          php: "🐘",
          json: "📊",
          // 图片类
          jpg: "🖼️",
          jpeg: "🖼️",
          png: "🖼️",
          gif: "🎞️",
          svg: "🖌️",
          // 压缩包
          zip: "📦",
          rar: "📦",
          "7z": "📦",
          tar: "📦",
          gz: "📦",
          // 其他
          exe: "⚙️",
          dmg: "💿",
          iso: "💿",
          mp4: "🎬",
          mp3: "🎵",
        };
        return iconMap[ext] || "📄"; // 默认使用 📄
      }

      // 切换文件夹折叠状态
      function toggleFolder(event) {
        const header = event.currentTarget;
        const children = header.nextElementSibling;
        const toggleIcon = header.querySelector(".toggle-icon");

        if (children && children.classList.contains("folder-children")) {
          if (children.classList.contains("collapsed")) {
            children.classList.remove("collapsed");
            toggleIcon.textContent = "▼";
          } else {
            children.classList.add("collapsed");
            toggleIcon.textContent = "▶";
          }
        }
        event.stopPropagation();
      }

      // 递归构建树形结构
      function buildFileTree(files) {
        const tree = {};

        files.forEach((file) => {
          const pathParts = file.path.split("/");
          let currentLevel = tree;
          const fileName = pathParts.pop(); // 文件名是路径最后一部分

          // 遍历路径中的每一级目录
          pathParts.forEach((folder) => {
            if (!currentLevel[folder]) {
              currentLevel[folder] = {};
            }
            currentLevel = currentLevel[folder];
          });

          // 在最终层级存放文件名和它的完整路径
          if (!currentLevel._files) {
            currentLevel._files = [];
          }
          currentLevel._files.push({
            name: fileName,
            fullPath: file.path, // 完整路径
            ext: fileName.split(".").pop().toLowerCase(),
            isHF: file.isHF, // 标记是否是大文件
            hfInfo: file.hfInfo, // 大文件信息
          });
        });

        return tree;
      }

      // 递归渲染树形结构
      function renderTree(
        node,
        level = 0,
        searchTerm = "",
        forceShowAll = false,
      ) {
        let html = "";
        const lowerSearchTerm = searchTerm.toLowerCase();

        // 获取所有文件夹（按字母排序）
        const folders = Object.keys(node)
          .filter((key) => key !== "_files")
          .sort((a, b) => a.localeCompare(b));

        // 渲染文件夹
        folders.forEach((folder) => {
          // 判断文件夹是否匹配搜索（递归检查子文件）
          const isFolderNameMatch = folder
            .toLowerCase()
            .includes(lowerSearchTerm);
          const contentsMatch = doesFolderMatchSearch(node[folder], searchTerm);
          const folderMatches =
            searchTerm === "" ||
            forceShowAll ||
            isFolderNameMatch ||
            contentsMatch;

          if (searchTerm !== "" && !folderMatches) {
            return; // 搜索模式下，不匹配的文件夹直接跳过
          }

          // 如果当前文件夹匹配，则强制显示所有子项
          const nextForceShowAll = forceShowAll || isFolderNameMatch;

          html += `
                    <div class="folder">
                        <div class="folder-header ${isFolderNameMatch && searchTerm !== "" ? "highlight" : ""}" onclick="toggleFolder(event)">
                            <span class="toggle-icon">${searchTerm === "" ? "▶" : "▼"}</span>
                            <span class="folder-icon">📁</span>
                            <span>${folder}/</span>
                        </div>
                        <div class="folder-children ${searchTerm === "" ? "collapsed" : ""}">
                            ${renderTree(node[folder], level + 1, searchTerm, nextForceShowAll)}
                        </div>
                    </div>
                `;
        });

        // 渲染当前文件夹下的文件
        if (node._files && node._files.length > 0) {
          node._files
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach((file) => {
              // 检查文件是否匹配搜索
              const fileNameLower = file.name.toLowerCase();
              const matches =
                searchTerm === "" ||
                forceShowAll ||
                fileNameLower.includes(lowerSearchTerm);

              if (searchTerm !== "" && !matches) {
                return; // 搜索模式下，不匹配的文件直接跳过
              }

              const icon = getFileIcon(file.name);
              const highlight =
                searchTerm !== "" && fileNameLower.includes(lowerSearchTerm)
                  ? "highlight"
                  : "";

              // 链接处理优化：
              // 1. 大文件 -> HuggingFace 直链
              // 2. 可浏览器直接预览的文件 (PDF, 图片, TXT, JSON, HTML) -> 相对路径 (GitHub Pages 原生访问)
              // 3. 代码 and Markdown -> GitHub Blob 页面 (带渲染预览)

              let fileUrl;
              let title;
              let hfBadge = "";

              // 定义可以直接在浏览器预览的扩展名
              const previewExts = [
                "pdf",
                "jpg",
                "jpeg",
                "png",
                "gif",
                "svg",
                "txt",
                "json",
                "html",
                "htm",
                "xml",
              ];

              if (file.isHF) {
                fileUrl = file.hfInfo.url;
                title = `来自 HuggingFace (${file.hfInfo.size_mb}MB)`;
                hfBadge = '<span class="hf-badge">🤗 HF</span>';
              } else {
                if (previewExts.includes(file.ext)) {
                  // 可直接预览：使用相对路径（在 GitHub Pages 上直接打开）
                  // 注意：相对路径不需要 '/blob/'，直接访问文件
                  // 这里我们构造 GitHub Raw 链接或者相对链接。相对链接体验最好。
                  fileUrl = file.fullPath;
                  title = "直接预览/下载";
                } else {
                  // 代码 / Markdown：跳转到 GitHub Blob 页面查看渲染效果
                  fileUrl = `https://github.com/${username}/${repo}/blob/${branch}/${file.fullPath}`;
                  title = "在 GitHub 上查看源码/渲染";
                }
              }

              html += `
                        <div class="file-item ${highlight}">
                            <a href="${fileUrl}" target="_blank" title="${title}">
                                <span class="file-icon">${icon}</span>
                                <span>${file.name}</span>
                                ${hfBadge}
                            </a>
                        </div>
                    `;
            });
        }

        return html;
      }

      // 检查文件夹是否包含匹配搜索的文件（递归）
      function doesFolderMatchSearch(node, searchTerm) {
        const lowerSearchTerm = searchTerm.toLowerCase();

        // 检查当前层级的文件
        if (node._files) {
          for (const file of node._files) {
            if (file.name.toLowerCase().includes(lowerSearchTerm)) {
              return true;
            }
          }
        }

        // 递归检查子文件夹
        const folders = Object.keys(node).filter((key) => key !== "_files");
        for (const folder of folders) {
          if (folder.toLowerCase().includes(lowerSearchTerm)) {
            return true;
          }
          if (doesFolderMatchSearch(node[folder], searchTerm)) {
            return true;
          }
        }

        return false;
      }

      // 更新统计信息
      function updateStats(files) {
        // 统计各种文件类型
        const extCount = {};
        files.forEach((f) => {
          // 如果 path 不包含 . 可能会有问题，加个保护
          const parts = f.path.split(".");
          if (parts.length > 1) {
            const ext = parts.pop().toLowerCase();
            extCount[ext] = (extCount[ext] || 0) + 1;
          }
        });

        // 取前5个最多的扩展名
        const topExts = Object.entries(extCount)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .map(([ext, count]) => `${ext}: ${count}个`);

        const folderSet = new Set();
        files.forEach((f) => {
          const pathParts = f.path.split("/");
          if (pathParts.length > 1) {
            for (let i = 1; i < pathParts.length; i++) {
              folderSet.add(pathParts.slice(0, i).join("/"));
            }
          }
        });

        const statsDiv = document.getElementById("stats");
        const hfCount = files.filter((f) => f.isHF).length;

        statsDiv.innerHTML = `
                <span>📁 文件夹: ${folderSet.size} 个</span>
                <span>📄 文件总数: ${files.length} 个 (含 ${hfCount} 个大文件)</span>
                <span>🔤 主要类型: ${topExts.join(" · ")}</span>
            `;
      }

      // 刷新文件列表（根据搜索词）
      function refreshFileList() {
        if (allFilesData.length === 0) return;

        // 构建树形结构
        const fileTree = buildFileTree(allFilesData);

        // 渲染文件树（传入搜索词）
        const treeHtml = renderTree(fileTree, 0, currentSearchTerm);

        if (treeHtml.trim() === "") {
          document.getElementById("file-list").innerHTML =
            '<div class="no-results">🔍 没有找到匹配的文件</div>';
        } else {
          document.getElementById("file-list").innerHTML = treeHtml;
        }
      }

      // 主函数：获取并显示文件列表
      async function listAllFiles() {
        try {
          // 1. 获取 GitHub 上的文件列表 (Git Tree API)
          const response = await fetch(
            `https://api.github.com/repos/${username}/${repo}/git/trees/${branch}?recursive=1`,
          );

          if (!response.ok) {
            if (response.status === 404) throw new Error("仓库或分支未找到");
            if (response.status === 403)
              throw new Error("API 访问受限（请稍后再试）");
            throw new Error(`GitHub API Error: ${response.status}`);
          }

          const data = await response.json();
          if (!data.tree) {
            throw new Error("无法获取 Git 文件树");
          }

          // 过滤 Git 文件
          // 保留所有文件，除了 .github, scripts, data 和 index.html/README.md (可选)
          // 这里我们过滤掉 .github 和 .git 相关的配置，以及 scripts 和 data 目录
          // 但保留 README.md 方便查看
          let gitFiles = data.tree.filter((item) => {
            return (
              item.type === "blob" &&
              !item.path.startsWith(".github/") &&
              !item.path.startsWith("scripts/") &&
              !item.path.startsWith("data/") && // 隐藏 data 目录
              !item.path.startsWith(".git") &&
              item.path !== "index.html"
            ); // 隐藏 index.html 本身
          });

          // 转换为统一格式
          allFilesData = gitFiles.map((f) => ({
            path: f.path,
            name: f.path.split("/").pop(),
            isHF: false,
          }));

          // 2. 加载 HuggingFace 文件清单 (大文件)
          try {
            // 添加时间戳防止缓存
            const manifestResponse = await fetch(
              `./data/file_manifest.json?t=${new Date().getTime()}`,
            );
            if (manifestResponse.ok) {
              const manifest = await manifestResponse.json();
              console.log(`✅ 已加载 ${manifest.files.length} 个大文件清单`);

              // 将大文件合并到 allFilesData 中！
              // 关键修复：之前只做了映射，没把文件加回去
              manifest.files.forEach((hfFile) => {
                allFilesData.push({
                  path: hfFile.path, // 保持原始路径 (如 "path/to/large.pdf")
                  name: hfFile.name,
                  isHF: true,
                  hfInfo: {
                    size_mb: hfFile.size_mb,
                    url: hfFile.url,
                  },
                });
              });
            }
          } catch (e) {
            console.warn(
              "⚠️ 未能加载大文件清单 (data/file_manifest.json)，仅显示 GitHub 文件。",
              e,
            );
          }

          if (allFilesData.length === 0) {
            document.getElementById("file-list").innerHTML =
              '<div class="loading">📂 暂无文件</div>';
            return;
          }

          // 刷新文件列表
          refreshFileList();

          // 更新统计信息
          updateStats(allFilesData);
        } catch (error) {
          document.getElementById("file-list").innerHTML = `
                    <div class="error">
                        ❌ 加载失败: ${error.message}<br>
                        <div style="font-size: 14px; margin-top: 10px;">
                            可能原因：<br>
                            1. GitHub Pages 尚未部署完成（请稍等几分钟）<br>
                            2. 仓库使用了私有模式<br>
                            3. API 速率限制
                        </div>
                    </div>
                `;
          console.error(error);
        }
      }

      // 搜索功能
      function setupSearch() {
        const searchInput = document.getElementById("searchInput");
        const clearButton = document.getElementById("clearSearch");

        // 防抖函数，避免频繁渲染
        let debounceTimer;
        searchInput.addEventListener("input", (e) => {
          clearTimeout(debounceTimer);
          debounceTimer = setTimeout(() => {
            currentSearchTerm = e.target.value.trim();
            refreshFileList();
          }, 300);
        });

        // 清除搜索
        clearButton.addEventListener("click", () => {
          searchInput.value = "";
          currentSearchTerm = "";
          refreshFileList();
          searchInput.focus();
        });

        // 支持回车直接搜索
        searchInput.addEventListener("keypress", (e) => {
          if (e.key === "Enter") {
            clearTimeout(debounceTimer);
            currentSearchTerm = e.target.value.trim();
            refreshFileList();
          }
        });
      }

      // 启动
      listAllFiles();
      setupSearch();
    </script>
  </body>
</html>
```
