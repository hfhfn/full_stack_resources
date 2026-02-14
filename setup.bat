@echo off
setlocal enabledelayedexpansion
:: 使用 65001 (UTF-8) 以支持中文字符显示
chcp 65001 >nul

echo ============================================
echo   GitHub + HuggingFace Dual-Storage Setup
echo   架构版本: v4.0 (拉取优先模式)
echo ============================================
echo.

:: 1. 环境检查
echo [1/7] 检查环境...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: 2. 检查依赖
echo.
echo [2/7] 检查依赖...
python -c "import huggingface_hub" >nul 2>&1
if !errorlevel! neq 0 (
    echo   正在安装 huggingface_hub...
    pip install -q "huggingface_hub>=0.17.0"
) else (
    echo   OK: huggingface_hub 已安装
)

:: 3. 同步远程 (在所有本地操作之前进行)
:: 这样可以确保后续的 distribute_files.py 基于最新的远程清单运行
echo.
echo [3/7] 同步远程更改 (防止清单冲突)...
git pull --rebase origin main
if !errorlevel! neq 0 (
    echo.
    echo [ERROR] 同步失败。如果存在冲突，请手动解决或运行: git rebase --abort
    pause
    exit /b 1
)

:: 4. 运行分发引擎
echo.
echo [4/7] 运行分发引擎 [扫描大文件并更新清单]...
python scripts\distribute_files.py

:: 5. 准备本地提交
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

:: 6. 推送至 GitHub
echo.
echo [6/7] 推送到 GitHub...
git push origin main
if !errorlevel! neq 0 (
    echo.
    echo [WARNING] 推送失败。可能是短时间内的并发推送，请重试或手动运行: git push origin main
) else (
    echo   OK: 推送完成！
)

echo.
echo ============================================
echo   全部配置完成！
echo ============================================
pause
