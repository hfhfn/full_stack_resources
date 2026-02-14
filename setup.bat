@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ============================================
echo   GitHub + HuggingFace Dual-Storage Setup
echo ============================================
echo.

:: 1. 检查 Python
echo [1/7] 检查 Python 环境...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: 2. 检查依赖
echo.
echo [2/7] 安装/检查依赖...
python -c "import huggingface_hub" >nul 2>&1
if !errorlevel! neq 0 (
    echo   正在安装 huggingface_hub...
    pip install -q "huggingface_hub>=0.17.0"
) else (
    echo   OK: huggingface_hub 已安装
)

:: 3. HF 认证
echo.
echo [3/7] HuggingFace 认证
python -c "from huggingface_hub import HfApi; HfApi().whoami()" >nul 2>&1
if !errorlevel! neq 0 (
    echo   说明: 未检测到登录信息，后续请运行 huggingface-cli login。
) else (
    echo   OK: 已检测到 HuggingFace 登录状态
)

:: 4. 运行分发
echo.
echo [4/7] 运行分发引擎 [扫描大文件]...
python scripts\distribute_files.py

:: 5. 准备本地提交 (必须先 Commit 才能安全 Rebase)
echo.
echo [5/7] 准备本地提交...
git add .
git diff --cached --quiet
if !errorlevel! neq 0 (
    echo   检测到变更...
    set /p commit_msg="  请输入提交信息 [默认: Auto update]: "
    if "!commit_msg!"=="" set commit_msg=Auto update
    git commit -m "!commit_msg!"
    echo   OK: 已完成本地提交
) else (
    echo   OK: 无需提交，没有变更
)

:: 6. 同步远程 [解决 Push Rejected 问题]
echo.
echo [6/7] 同步远程更改 (git pull --rebase)...
git pull --rebase origin main

:: 7. 推送至 GitHub
echo.
echo [7/7] 推送到 GitHub...
git push origin main
if !errorlevel! neq 0 (
    echo.
    echo [WARNING] 推送失败。请尝试手动运行: git push origin main
) else (
    echo   OK: 推送完成！
)

echo.
echo ============================================
echo   全部配置完成！
echo ============================================
pause
