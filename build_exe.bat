@echo off
echo Building Clipboard Reply EXE...
echo.
echo Installing PyInstaller...
pip install pyinstaller
echo.
echo Creating EXE...
pyinstaller --onefile --windowed --name "Clipboard Reply" main.py
echo.
echo Copying files to dist folder...
copy .env.example dist\
copy prompts.json dist\
echo.
echo Done! EXE is in the 'dist' folder.
echo.
pause
