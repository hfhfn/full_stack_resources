#!/bin/bash
# 快速启动脚本：环境检查 + 依赖安装 + 首次分发 (Linux/macOS)

echo ""
echo "============================================"
echo "  Full Stack Resources - 自动文件分发系统"
echo "============================================"
echo ""

# --- 1. 检查 Python ---
echo "[1/5] 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] 未找到 python3，请先安装。"
    exit 1
fi
python3 --version

# --- 2. 安装依赖 ---
echo ""
echo "[2/5] 安装 huggingface_hub..."
pip3 install -q huggingface_hub
echo "  OK: huggingface_hub 已安装"

# --- 3. HuggingFace 认证 ---
echo ""
echo "[3/5] HuggingFace 认证"
# 简单检查是否已登录
if python3 -c "from huggingface_hub import HfApi; HfApi().whoami()" &> /dev/null; then
    echo "  已登录 HuggingFace。"
else
    echo "  未检测到登录状态。"
    read -p "  是否现在登录? (y/n) [n]: " login_choice
    if [[ "$login_choice" == "y" || "$login_choice" == "Y" ]]; then
        huggingface-cli login
    else
        echo "  跳过登录，仅生成清单。"
    fi
fi

# --- 4. 运行分发脚本 ---
echo ""
echo "[4/5] 运行分发脚本..."
# 切换到脚本所在目录的上一级 (项目根目录)
cd "$(dirname "$0")/.."
python3 scripts/distribute_files.py

# --- 5. Git 提交与推送 ---
echo ""
echo "[5/5] 提交并推送到 GitHub..."
git add .
if ! git diff --cached --quiet; then
    git commit -m "Auto: Initial setup and file distribution"
    echo "  已提交更改。"
else
    echo "  没有需要提交的更改。"
fi

echo "  正在推送到 origin main..."
git push origin main

echo ""
echo "============================================"
echo "  全部完成！"
echo "============================================"
echo ""
