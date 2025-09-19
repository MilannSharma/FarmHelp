@echo off
echo Testing Flask app for Android WebView...
echo.

cd /d ..

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import flask, joblib, numpy, warnings" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install flask joblib numpy scikit-learn
)

REM Start Flask app
echo Starting Flask app on http://127.0.0.1:5000/
echo You can now test the Android app or access the web interface
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
