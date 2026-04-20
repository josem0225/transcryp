@echo off
echo ============================================
echo              Transcryp Setup
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [+] Installing Python...
    winget install Python.Python.3 --silent --accept-package-agreements --accept-source-agreements
    echo.
    echo [!] Python was just installed. Please close VS Code completely, reopen it, and run setup.bat again.
    pause
    exit /b 0
) else (
    echo [ok] Python already installed.
)

echo [+] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo   Done! Run: python transcriber.py
echo ============================================
pause
