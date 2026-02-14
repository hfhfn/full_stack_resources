#!/bin/bash
echo "=========================================="
echo "  GitHub + HuggingFace Dual-Storage Setup"
echo "=========================================="
echo ""

# 1. 检查 Python
echo "[1/7] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] 未找到 python3，请先安装 Python 3.8+。"
    exit 1
fi

# 2. 检查并安装依赖
echo ""
echo "[2/7] 安装/检查依赖..."
if ! python3 -c "import huggingface_hub" &> /dev/null; then
    echo "  正在安装 huggingface_hub..."
    pip3 install -q "huggingface_hub>=0.17.0"
else
    echo "  OK: huggingface_hub 已安装"
fi

# 3. HuggingFace 认证引导
echo ""
echo "[3/7] HuggingFace 认证"
if python3 -c "from huggingface_hub import HfApi; HfApi().whoami()" &> /dev/null; then
    echo "  OK: 已检测到 HuggingFace 登录状态"
else
    echo "  未检测到登录信息，后续请运行 huggingface-cli login。"
fi

# 4. 运行文件分发逻辑
echo ""
echo "[4/7] 运行分发引擎 (扫描大文件)..."
python3 scripts/distribute_files.py

# 5. 同步远程更改
echo ""
echo "[5/7] 同步远程更改 (防止 Push 冲突)..."
git pull --rebase origin main

# 6. 自动 Git 提交
echo ""
echo "[6/7] 准备 Git 提交..."
git add .
if ! git diff --cached --quiet; then
    git commit -m "Auto update via setup.sh"
    echo "  OK: 已完成本地提交"
else
    echo "  ✨ 无需提交，没有变更"
fi

# 7. 推送到 GitHub
echo ""
echo "[7/7] 推送到 GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "  全部配置完成！"
echo "=========================================="
