@echo off
title Build Shadows of Valor EXE
echo =======================================
echo     Shadows of Valor Build Script
echo =======================================

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python is not detected on this system!
    echo Please install Python 3.x from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

REM Remove old build folders if they exist
IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist
IF EXIST ShadowsOfValor.exe del /f /q ShadowsOfValor.exe

REM Ensure the icon file exists
IF NOT EXIST "game_icon.ico" (
    echo.
    echo ERROR: game_icon.ico not found in the project folder!
    echo Place your .ico file in the same folder as shadows_of_valor.py and rename it to game_icon.ico
    pause
    exit /b
)

REM Build the executable with icon, onefile
echo Building ShadowsOfValor.exe...
python -m PyInstaller --onefile --name ShadowsOfValor --icon="game_icon.ico" shadows_of_valor.py

REM Move the EXE directly to the project folder
IF EXIST dist\ShadowsOfValor.exe (
    move /Y dist\ShadowsOfValor.exe .\
)

REM Clean up build/dist folders
IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist

echo.
echo Build Complete!
echo ShadowsOfValor.exe is now in your project folder.
echo You can double-click it to play!
pause