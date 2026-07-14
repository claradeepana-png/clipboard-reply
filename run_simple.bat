@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  Clipboard Reply - SIMPLE RUN SCRIPT
REM  Just double-click this file!
REM ============================================

cls
echo.
echo ========================================
echo   CLIPBOARD REPLY - STARTING
echo ========================================
echo.

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo   ERROR: PYTHON NOT FOUND
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo.
    echo Python is not installed or not in PATH
    echo.
    echo FIX: Install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: When installing, check:
    echo "Add Python to PATH" checkbox
    echo.
    echo Then restart your computer.
    echo.
    pause
    exit /b 1
)

echo [STEP 1/4] Checking Python... OK
echo.

REM Check .env file
if not exist ".env" (
    echo [STEP 2/4] Checking .env file...
    echo.
    echo WARNING: .env file not found!
    echo.
    echo You need to:
    echo   1. Go to https://openrouter.ai
    echo   2. Sign up (FREE)
    echo   3. Get your API key
    echo   4. Create .env file with your key
    echo.
    echo Create .env file now? (y/n)
    set /p choice=
    if /i "!choice!"=="y" (
        (
            echo OPENROUTER_API_KEY=your_key_here
            echo DEFAULT_MODEL=openai/gpt-3.5-turbo
            echo HOTKEY=ctrl+shift+r
        ) > .env
        echo.
        echo .env file created!
        echo Please edit it and add your API key
        pause
        exit /b 1
    )
) else (
    echo [STEP 2/4] .env file found... OK
    echo.
)

REM Install requirements
echo [STEP 3/4] Installing dependencies...
pip install -q -r requirements.txt 2>nul
if errorlevel 1 (
    echo ERROR installing requirements
    pause
    exit /b 1
)
echo Dependencies installed... OK
echo.

REM Start the app
echo [STEP 4/4] Starting app...
echo.
echo ========================================
echo   APP STARTING - PLEASE WAIT
echo ========================================
echo.

python main.py

REM If we reach here, app crashed
echo.
echo ERROR: App closed unexpectedly
echo.
echo Check that:
echo   1. .env file exists in this folder
echo   2. API key is correct in .env
echo   3. You're connected to the internet
echo.
pause
