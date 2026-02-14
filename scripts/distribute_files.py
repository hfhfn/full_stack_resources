#!/usr/bin/env python3
"""
Dual-Storage Distribution Script v3.1
- Scans project for all files.
- Uploads large files (>50MB) to HuggingFace.
- Implement retry logic for network stability.
- Generates a full manifest (including small files) to avoid GitHub API rate limits.
- Sync Deletion: Cleans up redundant files on HF.
"""
import os
import sys
import json
import logging
import time
import subprocess
from pathlib import Path
from datetime import datetime
from functools import wraps

# --- Configuration ---
SIZE_THRESHOLD = 50 * 1024 * 1024  # 50MB
HF_REPO_ID = "hfhfn/full_stack_resources"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Exclude directories
EXCLUDE_DIRS = {'.git', '.idea', '.vscode', 'venv', 'node_modules', '__pycache__', '.serena', '.github'}

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / 'distribute.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def retry(exceptions, tries=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff."""
    def decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
        mtries, mdelay = tries, delay
        while mtries > 1:
          try:
            return f(*args, **kwargs)
          except exceptions as e:
            logger.warning(f"{str(e)}, Retrying in {mdelay} seconds...")
            time.sleep(mdelay)
            mtries -= 1
            mdelay *= backoff
        return f(*args, **kwargs)
      return wrapper
    return decorator

def get_file_info(path):
    stats = path.stat()
    return {
        "size": stats.st_size,
        "mtime": stats.st_mtime
    }

def run_git_cmd(args):
    try:
        subprocess.run(['git'] + args, cwd=PROJECT_ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        logger.debug(f"Git command failed: {args} - {e}")

def scan_files():
    large_files = []
    small_files = []
    logger.info(f"Scanning files (Threshold: {SIZE_THRESHOLD/1024/1024:.0f}MB)...")

    for path in PROJECT_ROOT.rglob('*'):
        if not path.is_file(): continue
        parts = path.relative_to(PROJECT_ROOT).parts
        
        # 严格过滤逻辑
        if any(p.startswith('.') for p in parts): continue # 隐藏文件/文件夹
        if any(ex in parts for ex in EXCLUDE_DIRS): continue # 排除目录
        if 'scripts' in parts: continue # 明确排除 scripts 文件夹
        if 'data' in parts: continue # 排除清单存储目录
        if path.name in ['index.html', 'README.md', 'setup.bat', 'setup.sh', 'distribute.log', '.gitignore', '.gitattributes']: continue

        try:
            info = get_file_info(path)
            if info["size"] >= SIZE_THRESHOLD:
                large_files.append(path)
            else:
                small_files.append(path)
        except OSError: pass

    return large_files, small_files

@retry(Exception, tries=3, delay=5)
def upload_file_to_hf(api, file_path, rel_path):
    logger.info(f"   > Uploading: {rel_path} ({get_file_info(file_path)['size']/1024/1024:.1f} MB)")
    api.upload_file(
        path_or_fileobj=str(file_path),
        path_in_repo=rel_path,
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        commit_message=f"Upload large file: {os.path.basename(rel_path)}"
    )

def upload_to_hf(files):
    if not files: return
    logger.info(f"Uploading {len(files)} files to HuggingFace ({HF_REPO_ID})...")
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        user = api.whoami()
        logger.info(f"Logged in as: {user['name']}")

        for file_path in files:
            rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
            upload_file_to_hf(api, file_path, rel_path)
        
        logger.info("[OK] HF Upload complete")
        return True
    except ImportError:
        logger.error("huggingface_hub not installed. Run: pip install huggingface_hub")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Upload flow failed: {str(e)}")
        return False

def sync_hf_deletions(local_large_files):
    logger.info(f"Checking for redundant files on HuggingFace ({HF_REPO_ID})...")
    try:
        from huggingface_hub import HfApi, list_repo_files
        api = HfApi()
        remote_files = list_repo_files(repo_id=HF_REPO_ID, repo_type="dataset")
        local_rel_paths = {f.relative_to(PROJECT_ROOT).as_posix() for f in local_large_files}

        to_delete = [rf for rf in remote_files if rf not in local_rel_paths and not rf.endswith(('.gitattributes', 'README.md', '.gitignore'))]

        if to_delete:
            logger.info(f"Found {len(to_delete)} redundant files. Deleting...")
            for rf in to_delete:
                logger.info(f"   - Deleting: {rf}")
                api.delete_file(path_in_repo=rf, repo_id=HF_REPO_ID, repo_type="dataset", commit_message=f"Sync delete: {os.path.basename(rf)}")
            logger.info(f"[OK] Sync deletion complete (Removed {len(to_delete)} files)")
        else:
            logger.info("No redundant files found.")
    except Exception as e:
        logger.warning(f"Sync deletion failed: {str(e)}")

def update_gitignore_and_git(large_files):
    logger.info("Processing Git tracking & .gitignore...")
    gitignore_path = PROJECT_ROOT / '.gitignore'
    
    lines = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    header = "# [Auto] Large files managed by HuggingFace\n"
    new_content = []
    skip = False
    for line in lines:
        if line == header: skip = True; continue
        if skip and line.strip() == "": skip = False; continue
        if not skip: new_content.append(line)

    new_rules = []
    for f in large_files:
        rel = f.relative_to(PROJECT_ROOT).as_posix()
        new_rules.append(rel)
        run_git_cmd(['rm', '--cached', str(f)])

    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)
        if new_rules:
            if new_content and not new_content[-1].endswith('\n'): f.write('\n')
            f.write("\n" + header)
            for rule in sorted(new_rules): f.write(f"{rule}\n")
    logger.info(f"Updated .gitignore with {len(new_rules)} rules")

def generate_manifest(large_files, small_files):
    logger.info("Generating full manifest (data/file_manifest.json)...")
    manifest = {
        "hf_repo_id": HF_REPO_ID,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": []
    }

    # Helper to add file to manifest
    def add_to_manifest(file_list, is_hf):
        for f in file_list:
            rel = f.relative_to(PROJECT_ROOT).as_posix()
            info = get_file_info(f)
            # Use raw.githubusercontent for small files to avoid API limits
            url = f"https://huggingface.co/datasets/{HF_REPO_ID}/resolve/main/{rel}" if is_hf else f"https://raw.githubusercontent.com/hfhfn/full_stack_resources/main/{rel}"
            
            manifest["files"].append({
                "name": f.name,
                "path": rel,
                "extension": f.suffix.lower().lstrip('.'),
                "size_mb": round(info["size"] / (1024 * 1024), 2),
                "url": url,
                "is_hf": is_hf,
                "last_modified": datetime.fromtimestamp(info["mtime"]).strftime("%Y-%m-%d %H:%M:%S")
            })

    add_to_manifest(large_files, True)
    add_to_manifest(small_files, False)

    manifest_dir = PROJECT_ROOT / 'data'
    manifest_dir.mkdir(exist_ok=True)
    with open(manifest_dir / 'file_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    logger.info(f"[OK] Manifest generated with {len(manifest['files'])} total files")

def main():
    start_time = time.time()
    try:
        large, small = scan_files()
        logger.info(f"Stats: {len(large)} large files, {len(small)} small files")

        upload_to_hf(large)
        sync_hf_deletions(large)
        update_gitignore_and_git(large)
        generate_manifest(large, small)

        elapsed = time.time() - start_time
        logger.info(f"\n[OK] All steps complete in {elapsed:.1f}s! Ready for git push.")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
