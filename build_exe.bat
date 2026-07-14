@echo off
REM Clipboard Reply - PyInstaller Build Script
REM This script builds the EXE file for Windows 11

echo.
echo ╔════════════════════════════════════════╗
echo ║   🤖 Clipboard Reply - Build Script    ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if required files exist
if not exist "main.py" (
    echo ❌ ERROR: main.py not found in current directory
    echo.
    pause
    exit /b 1
)

if not exist "prompts.json" (
    echo ❌ ERROR: prompts.json not found in current directory
    echo.
    pause
    exit /b 1
)

echo ✅ Required files found
echo.

REM Install/upgrade PyInstaller
echo 📦 Installing PyInstaller (if not already installed)...
pip install --upgrade pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Failed to install PyInstaller
    echo.
    pause
    exit /b 1
)

echo ✅ PyInstaller ready
echo.

REM Clean previous build
if exist "build" (
    echo 🧹 Cleaning previous build artifacts...
    rmdir /s /q build >nul 2>&1
)

if exist "dist" (
    echo 🧹 Cleaning previous dist folder...
    rmdir /s /q dist >nul 2>&1
)

if exist "Clipboard Reply.spec" (
    del "Clipboard Reply.spec" >nul 2>&1
)

echo.
echo 🔨 Building EXE file...
echo.

REM Build with PyInstaller
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Clipboard Reply" ^
    --add-data "prompts.json;." ^
    --add-data ".env.example;." ^
    --distpath dist ^
    --buildpath build ^
    --specpath build ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Build failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.

REM Copy additional files to dist
echo 📋 Copying configuration files...
if exist ".env.example" (
    copy ".env.example" "dist\.env.example" >nul 2>&1
    echo   ✅ .env.example copied
)

if exist "prompts.json" (
    copy "prompts.json" "dist\prompts.json" >nul 2>&1
    echo   ✅ prompts.json copied
)

if exist "README.md" (
    copy "README.md" "dist\README.md" >nul 2>&1
    echo   ✅ README.md copied
)

echo.
echo ╔════════════════════════════════════════╗
echo ║        ✨ BUILD SUCCESSFUL! ✨          ║
echo ╚════════════════════════════════════════╝
echo.
echo 📁 Output folder: dist\
echo.
echo 📦 Inside dist\ folder you'll find:
echo    • Clipboard Reply.exe (Main application)
echo    • prompts.json (AI prompts)
echo    • .env.example (Configuration template)
echo    • README.md (Instructions)
echo.
echo 🚀 Next steps:
echo    1. Go to dist\ folder
echo    2. Create .env file (copy from .env.example)
echo    3. Add your OpenRouter API key
echo    4. Double-click "Clipboard Reply.exe" to run
echo    5. Press Ctrl+Shift+R to test!
echo.
echo 📤 To release:
echo    1. Right-click dist\Clipboard Reply.exe
echo    2. Send to → Compressed folder
echo    3. Upload to GitHub Releases
echo.
pause
