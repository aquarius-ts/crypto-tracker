@echo off
echo ==========================================
echo   Building Crypto Tracker Executable
echo ==========================================
echo.

REM Check if pyinstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Build executable
echo Building executable...
pyinstaller crypto_tracker.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo BUILD SUCCESSFUL!
    echo ==========================================
    echo.
    echo Executable location: dist\CryptoTracker.exe
    echo.
    echo To run: dist\CryptoTracker.exe
) else (
    echo.
    echo ==========================================
    echo BUILD FAILED!
    echo ==========================================
    exit /b 1
)

pause
