@echo off
echo ============================================
echo              Transcryp Setup
echo ============================================
echo.

set PYTHON_CMD=

REM Try py launcher first
py --version >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=py

REM Try python command
if "%PYTHON_CMD%"=="" (
    python --version >nul 2>&1
    if %errorlevel% == 0 set PYTHON_CMD=python
)

REM Try standard Windows install location
if "%PYTHON_CMD%"=="" (
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%D\python.exe" set PYTHON_CMD=%%D\python.exe
    )
)

REM Try uv install location (any version)
if "%PYTHON_CMD%"=="" (
    for /d %%D in ("%APPDATA%\uv\python\cpython*") do (
        if exist "%%D\python.exe" set PYTHON_CMD=%%D\python.exe
    )
)

REM Try .local/bin (uv on some setups)
if "%PYTHON_CMD%"=="" (
    if exist "%USERPROFILE%\.local\bin\python3.exe" set PYTHON_CMD=%USERPROFILE%\.local\bin\python3.exe
)

REM Last resort: install via uv
if "%PYTHON_CMD%"=="" (
    echo [~] Python not found. Trying to install via uv...
    pip install uv >nul 2>&1
    uv python install >nul 2>&1
    for /d %%D in ("%APPDATA%\uv\python\cpython*") do (
        if exist "%%D\python.exe" set PYTHON_CMD=%%D\python.exe
    )
)

if "%PYTHON_CMD%"=="" (
    echo [!] Python not found.
    echo     Install it from https://www.python.org/downloads/
    echo     Check "Add Python to PATH" during installation, then run this script again.
    pause
    exit /b 1
)

echo [ok] Python found.

if not exist ".venv" (
    echo [+] Creating virtual environment...
    "%PYTHON_CMD%" -m venv .venv
) else (
    echo [ok] Virtual environment already exists.
)

echo [+] Installing dependencies...
.venv\Scripts\pip install -r requirements.txt

echo.
echo ============================================
echo   Done! To run the script:
echo   1. .venv\Scripts\activate
echo   2. python transcriber.py
echo ============================================
pause
