#!/bin/bash
echo "=========================================="
echo "  GitHub + HuggingFace Dual-Storage Setup"
echo "  Architecture: v4.0 (Pull-First)"
echo "=========================================="
echo ""

# 1. 环境检查
echo "[1/7] Checking environment..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found."
    exit 1
fi

# 2. 检查依赖
echo ""
echo "[2/7] Checking dependencies..."
if ! python3 -c "import huggingface_hub" &> /dev/null; then
    pip3 install -q "huggingface_hub>=0.17.0"
else
    echo "  OK: huggingface_hub is installed"
fi

# 3. 同步远程 (核心修复: 优先拉取减少冲突的可能性)
echo ""
echo "[3/7] Syncing remote changes (git pull --rebase)..."
git pull --rebase origin main
if [ $? -ne 0 ]; then
    echo "[ERROR] Sync failed. Please resolve conflicts or run: git rebase --abort"
    exit 1
fi

# 4. 运行分发引擎
echo ""
echo "[4/7] Running distribution engine..."
python3 scripts/distribute_files.py

# 5. Local Commit
echo ""
echo "[5/7] Preparing Git commit..."
git add .
if ! git diff --cached --quiet; then
    read -p "  Enter commit message [Default: Auto update]: " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Auto update"
    fi
    git commit -m "$commit_msg"
    echo "  OK: Committed locally"
else
    echo "  OK: No changes to commit"
fi

# 6. Push
echo ""
echo "[6/7] Pushing to GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "  All Done!"
echo "=========================================="
