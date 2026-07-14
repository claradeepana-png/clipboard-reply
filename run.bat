@echo off
REM Clipboard Suite - Control Center
REM Main app for managing everything

echo.
echo ========================================
echo   CLIPBOARD SUITE - CONTROL CENTER
echo ========================================
echo.

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo   ERROR: PYTHON NOT FOUND
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo.
    echo Python is not installed!
    echo.
    echo Install from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [STEP 1/3] Python found... OK
echo.

REM Check if .env exists
if not exist ".env" (
    echo [STEP 2/3] Creating .env file...
    (
        echo OPENROUTER_API_KEY=your_key_here
        echo DEFAULT_MODEL=openai/gpt-3.5-turbo
        echo HOTKEY=ctrl+shift+r
    ) > .env
    echo WARNING: .env created with default values
    echo Please edit .env and add your API key!
    echo.
) else (
    echo [STEP 2/3] .env file found... OK
    echo.
)

echo [STEP 3/3] Starting Control Center...
echo.

python control_center.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start app
    echo.
    pause
    exit /b 1
)
