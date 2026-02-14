@echo off
setlocal enabledelayedexpansion
:: UTF-8 support for Chinese characters
chcp 65001 >nul

echo ============================================
echo   GitHub + HuggingFace Dual-Storage Setup
echo   Architecture: v4.0 (Pull-First Optimized)
echo ============================================
echo.

:: 1. Check Python
echo [1/7] Checking Python...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found. Install Python 3.8+
    pause
    exit /b 1
)

:: 2. Check Dependencies
echo.
echo [2/7] Checking Dependencies...
python -c "import huggingface_hub" >nul 2>&1
if !errorlevel! neq 0 (
    echo   Installing huggingface_hub...
    pip install -q "huggingface_hub>=0.17.0"
) else (
    echo   OK: huggingface_hub installed
)

:: 3. Clean unstaged changes before pull (FIX: Prevent "unstaged changes" error)
echo.
echo [3/7] Preparing Git (cleanup unstaged changes)...
git diff --quiet >nul 2>&1
if !errorlevel! neq 0 (
    echo   Stashing local changes...
    git stash
)

:: 4. Sync Remote with Rebase
echo.
echo [4/7] Syncing Remote (git pull --rebase)...
git pull --rebase origin main
if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Sync failed. Resolve conflicts: git rebase --abort
    echo   Or restore stash: git stash pop
    pause
    exit /b 1
) else (
    echo   OK: Synced with remote
)

:: 5. Run Distribution Engine
echo.
echo [5/7] Running Distribution Script...
python scripts\distribute_files.py
if !errorlevel! neq 0 (
    echo [WARNING] Distribution script had errors. Check output above.
)

:: 6. Local Commit
echo.
echo [6/7] Preparing Commit...
git add .
git diff --cached --quiet
if !errorlevel! neq 0 (
    echo   Changes detected.
    set /p commit_msg="  Enter message (default: Auto update): "
    if "!commit_msg!"=="" set commit_msg=Auto update
    git commit -m "!commit_msg!"
    echo   OK: Committed locally
) else (
    echo   OK: No changes to commit
)

:: 7. Push to GitHub
echo.
echo [7/7] Pushing to GitHub...
git push origin main
if !errorlevel! neq 0 (
    echo [WARNING] Push failed. Retry manually: git push origin main
) else (
    echo   OK: Push successful
)

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
pause
