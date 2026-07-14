@echo off
REM Install all required packages

echo.
echo ========================================
echo   INSTALLING DEPENDENCIES
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

echo Python found!
echo.
echo Installing required packages...
echo.

REM Install packages
pip install --upgrade pip >nul 2>&1
echo [1/5] pip upgraded

pip install pyperclip >nul 2>&1
echo [2/5] pyperclip installed

pip install keyboard >nul 2>&1
echo [3/5] keyboard installed

pip install requests >nul 2>&1
echo [4/5] requests installed

pip install python-dotenv >nul 2>&1
echo [5/5] python-dotenv installed

echo.
echo ========================================
echo   ALL PACKAGES INSTALLED SUCCESSFULLY!
echo ========================================
echo.
echo You can now run: run.bat
echo.
pause
