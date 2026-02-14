#!/bin/bash
echo "=========================================="
echo "  GitHub + HuggingFace Dual-Storage Setup"
echo "  Architecture: v4.0 (Pull-First Optimized)"
echo "=========================================="
echo ""

# 1. Check Python
echo "[1/7] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.8+"
    exit 1
fi

# 2. Check Dependencies
echo ""
echo "[2/7] Checking Dependencies..."
if ! python3 -c "import huggingface_hub" &> /dev/null; then
    echo "   Installing huggingface_hub..."
    pip3 install -q "huggingface_hub>=0.17.0"
else
    echo "   OK: huggingface_hub installed"
fi

# 3. Sync Remote (Architecture v4.1: Autostash mode)
echo ""
echo "[3/7] Syncing Remote (git pull --rebase --autostash)..."
git pull --rebase --autostash origin main
if [ $? -ne 0 ]; then
    echo "[ERROR] Sync failed. Resolve conflicts manually: git rebase --abort"
    exit 1
else
    echo "   OK: Local and remote synced successfully"
fi

# 5. Run Distribution Engine
echo ""
echo "[5/7] Running Distribution Script..."
python3 scripts/distribute_files.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Distribution script had errors. Check output above."
fi

# 6. Local Commit
echo ""
echo "[6/7] Preparing Commit..."
git add .
if ! git diff --cached --quiet; then
    read -p "  Enter message (default: Auto update): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Auto update"
    fi
    git commit -m "$commit_msg"
    echo "   OK: Committed locally"
else
    echo "   OK: No changes to commit"
fi

# 7. Push
echo ""
echo "[7/7] Pushing to GitHub..."
git push origin main
if [ $? -ne 0 ]; then
    echo "[WARNING] Push failed. Retry manually: git push origin main"
else
    echo "   OK: Push successful"
fi

echo ""
echo "=========================================="
echo "   Setup Complete!"
echo "=========================================="

