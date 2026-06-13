@echo off
echo ===============================================
echo   SmartEval AI — Backend Startup
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Go to the Backend folder (same folder as this .bat file)
cd /d "%~dp0"

echo [1/3] Installing required packages...
pip install flask flask-cors PyMuPDF Pillow google-generativeai
echo.

echo [2/3] Checking API key...
if "%GEMINI_API_KEY%"=="" (
    echo.
    echo -----------------------------------------------
    echo  IMPORTANT: Set your Gemini API key first!
    echo -----------------------------------------------
    echo.
    set /p GEMINI_API_KEY="Paste your Gemini API key here and press Enter: "
    echo.
)

echo [3/3] Starting Flask server on http://127.0.0.1:5000
echo.
echo  Keep this window open while using SmartEval.
echo  Open your browser at:  Frontend/index.html
echo.
echo -----------------------------------------------

python app.py

pause
