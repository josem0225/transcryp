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
    echo [!] Python was just installed. Please restart your terminal and run setup.bat again.
    pause
    exit /b 0
) else (
    echo [ok] Python already installed.
)

ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [+] Installing ffmpeg...
    winget install Gyan.FFmpeg --silent --accept-package-agreements --accept-source-agreements
    echo [+] Adding ffmpeg to PATH...
    for /d %%D in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*") do (
        setx PATH "%PATH%;%%D\ffmpeg-*-full_build\bin" >nul 2>&1
        for /d %%F in ("%%D\ffmpeg-*-full_build\bin") do setx PATH "%PATH%;%%F" >nul
    )
    echo [!] ffmpeg installed. Please close VS Code completely, reopen it, and run setup.bat again.
    pause
    exit /b 0
) else (
    echo [ok] ffmpeg already installed.
)

echo [+] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo   Done! Run: python transcriber.py
echo ============================================
pause
