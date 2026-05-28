@echo off
REM Build script for MarkItDown Windows application
REM Requires Python 3.10+ and pip

echo ============================================
echo   MarkItDown App - Windows Build Script
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment
echo [1/4] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/4] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
pip install -e . >nul 2>&1

REM Build executable
echo [3/4] Building executable with PyInstaller...
pyinstaller build.spec --distpath dist --workpath build_temp --clean -y

REM Cleanup
echo [4/4] Cleaning up...
rmdir /s /q build_temp 2>nul

echo.
echo ============================================
echo   Build complete!
echo   Executable: dist\MarkItDown.exe
echo ============================================
pause
