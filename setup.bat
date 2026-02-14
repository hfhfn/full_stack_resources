@echo off
setlocal enabledelayedexpansion
:: 使用 65001 (UTF-8) 以支持中文字符显示
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

:: 2. 检查并安装依赖
echo.
echo [2/7] 安装/检查依赖...
python -c "import huggingface_hub" >nul 2>&1
if !errorlevel! neq 0 (
    echo   正在安装 huggingface_hub...
    pip install -q "huggingface_hub>=0.17.0"
) else (
    echo   OK: huggingface_hub 已安装
)

:: 3. HuggingFace 认证引导
echo.
echo [3/7] HuggingFace 认证
python -c "from huggingface_hub import HfApi; HfApi().whoami()" >nul 2>&1
if !errorlevel! neq 0 (
    echo   说明: 未检测到登录信息
    echo   - 请在稍后运行: huggingface-cli login
    echo.
) else (
    echo   OK: 已检测到 HuggingFace 登录状态
)

:: 4. 运行文件分发逻辑
echo.
echo [4/7] 运行分发引擎 [扫描大文件]...
python scripts\distribute_files.py

:: 5. 同步远程更改 [防止 Push 被拒绝]
echo.
echo [5/7] 同步远程更改...
git pull --rebase origin main

:: 6. 自动 Git 提交
echo.
echo [6/7] 准备 Git 提交...
git add .
git diff --cached --quiet
if !errorlevel! neq 0 (
    echo   检测到变更，正在执行本地提交...
    git commit -m "Auto update via setup.bat"
) else (
    echo   OK: 无需提交，没有变更
)

:: 7. 推送到 GitHub
echo.
echo [7/7] 推送到 GitHub...
git push origin main
if !errorlevel! neq 0 (
    echo.
    echo [WARNING] 推送失败。请手动执行: git push origin main
) else (
    echo   OK: 推送完成！
)

echo.
echo ============================================
echo   全部配置完成！
echo ============================================
pause
