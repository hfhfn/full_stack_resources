#!/bin/bash
echo "=========================================="
echo "  GitHub + HuggingFace Dual-Storage Setup"
echo "=========================================="
echo ""

# 1. 检查 Python
echo "[1/7] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found."
    exit 1
fi

# 2. 检查依赖
echo ""
echo "[2/7] 安装/检查依赖..."
if ! python3 -c "import huggingface_hub" &> /dev/null; then
    pip3 install -q "huggingface_hub>=0.17.0"
else
    echo "  OK: huggingface_hub 已安装"
fi

# 3. HF 认证
echo ""
echo "[3/7] HuggingFace 认证"
if python3 -c "from huggingface_hub import HfApi; HfApi().whoami()" &> /dev/null; then
    echo "  OK: 已检测到 HuggingFace 登录状态"
else
    echo "  说明: 未检测到登录信息"
fi

# 4. 运行分发
echo ""
echo "[4/7] 运行分发引擎..."
python3 scripts/distribute_files.py

# 5. 准备本地提交
echo ""
echo "[5/7] 准备本地提交..."
git add .
if ! git diff --cached --quiet; then
    read -p "  请输入提交信息 [默认: Auto update]: " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Auto update"
    fi
    git commit -m "$commit_msg"
    echo "  OK: 已本地提交"
else
    echo "  OK: 无需提交"
fi

# 6. 同步远程
echo ""
echo "[6/7] 同步远程更改 (git pull --rebase)..."
git pull --rebase origin main

# 7. 推送
echo ""
echo "[7/7] 推送到 GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "  全部配置完成！"
echo "=========================================="
