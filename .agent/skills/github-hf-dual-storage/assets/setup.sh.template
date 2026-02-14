#!/bin/bash
echo "=========================================="
echo "  GitHub + HuggingFace Dual-Storage Setup"
echo "=========================================="
echo ""

# 1. 检查 Python
echo "[1/6] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] 未找到 python3，请先安装 Python 3.8+。"
    exit 1
fi

# 2. 检查并安装依赖
echo ""
echo "[2/6] 安装/检查依赖..."
if ! python3 -c "import huggingface_hub" &> /dev/null; then
    echo "  正在安装 huggingface_hub..."
    pip3 install -q "huggingface_hub>=0.17.0"
else
    echo "  OK: huggingface_hub 已安装"
fi

# 3. HuggingFace 认证引导
echo ""
echo "[3/6] HuggingFace 认证"
if python3 -c "from huggingface_hub import HfApi; HfApi().whoami()" &> /dev/null; then
    echo "  OK: 已检测到 HuggingFace 登录状态"
else
    echo "  未检测到登录信息。"
    read -p "  是否现在运行 huggingface-cli login? (y/n) [n]: " login_choice
    if [[ "$login_choice" == "y" || "$login_choice" == "Y" ]]; then
        huggingface-cli login
    fi
fi

# 4. 运行文件分发逻辑
echo ""
echo "[4/6] 运行分发引擎 (扫描大文件)..."
python3 scripts/distribute_files.py

# 5. 自动 Git 提交
echo ""
echo "[5/6] 准备 Git 提交..."
git add .
if ! git diff --cached --quiet; then
    echo -n "  请输入提交信息 (直接回车使用默认: Auto update): "
    read commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Auto update"
    fi
    git commit -m "$commit_msg"
    echo "  OK: 已完成本地提交"
else
    echo "  ✨ 无需提交，没有变更"
fi

# 6. 推送到 GitHub
echo ""
echo "[6/6] 推送到 GitHub..."
git push origin main
if [ $? -ne 0 ]; then
    echo ""
    echo "[WARNING] 推送失败。可能是网络波动或远程冲突。"
    echo "请手动检查后运行: git push origin main"
else
    echo "  OK: 推送成功！"
fi

echo ""
echo "=========================================="
echo "  全部配置完成！"
echo "  资源导航页正在 GitHub Actions 中构建..."
echo "=========================================="
