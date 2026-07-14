@echo off
REM Todo List Application - Simple Run Script

echo.
echo ========================================
echo   TODO LIST - STARTING
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

echo [STEP 1/2] Python found... OK
echo.

echo [STEP 2/2] Starting Todo List...
echo.

python todo_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start app
    echo.
    pause
    exit /b 1
)
