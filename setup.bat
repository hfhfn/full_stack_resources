@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ============================================
echo   GitHub + HuggingFace Dual-Storage Setup
echo ============================================
echo.

:: 1. 检查 Python
echo [1/6] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: 2. 检查并安装依赖
echo.
echo [2/6] 安装/检查依赖...
python -c "import huggingface_hub" >nul 2>&1
if %errorlevel% neq 0 (
    echo   正在安装 huggingface_hub...
    pip install -q "huggingface_hub>=0.17.0"
) else (
    echo   OK: huggingface_hub 已安装
)

:: 3. HuggingFace 认证引导
echo.
echo [3/6] HuggingFace 认证
python -c "from huggingface_hub import HfApi; HfApi().whoami()" >nul 2>&1
if %errorlevel% neq 0 (
    echo   未检测到登录信息
    echo   1. 现在运行 huggingface-cli login
    echo   2. 稍后手动设置 HF_TOKEN
    echo   3. 跳过过程
    echo.
    set /p hf_choice="  请选择 1/2/3 [默认 3]: "
    if /i "!hf_choice!"=="1" (
        huggingface-cli login
    ) else if /i "!hf_choice!"=="2" (
        echo   请获取 Token: https://huggingface.co/settings/tokens
    )
) else (
    echo   OK: 已检测到 HuggingFace 登录状态
)

:: 4. 运行文件分发逻辑
echo.
echo [4/6] 运行分发引擎 [扫描大文件]...
python scripts\distribute_files.py

:: 5. 自动 Git 提交
echo.
echo [5/6] 准备 Git 提交...
git add .
git diff --cached --quiet
if %errorlevel% neq 0 (
    set /p commit_msg="  请输入提交信息 [直接回车使用默认: Auto update]: "
    if "!commit_msg!"=="" set commit_msg=Auto update
    git commit -m "!commit_msg!"
    echo   OK: 已完成本地提交
) else (
    echo   OK: 无需提交，没有变更
)

:: 6. 推送到 GitHub
echo.
echo [6/6] 推送到 GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] 推送失败。可能是网络波动或远程冲突。
    echo 请手动检查后运行: git push origin main
) else (
    echo   OK: 推送成功！
)

echo.
echo ============================================
echo   全部配置完成！
echo   资源导航页正在构建中...
echo ============================================
pause
