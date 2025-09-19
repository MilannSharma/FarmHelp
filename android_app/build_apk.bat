@echo off
echo Building farmHelp APK...
echo.

REM Check if Android SDK is available
if "%ANDROID_HOME%"=="" (
    echo Error: ANDROID_HOME environment variable not set.
    echo Please set ANDROID_HOME to your Android SDK path.
    echo Follow the instructions in ANDROID_SDK_SETUP_GUIDE.md
    pause
    exit /b 1
)

REM Navigate to the project directory
cd /d %~dp0

REM Download Gradle wrapper if not present
if not exist "gradle\wrapper\gradle-wrapper.jar" (
    echo Downloading Gradle wrapper...
    call download_gradle_wrapper.bat
    if not exist "gradle\wrapper\gradle-wrapper.jar" (
        echo Error: Gradle wrapper JAR not found. Please run download_gradle_wrapper.bat first.
        pause
        exit /b 1
    )
)

REM Clean and build the APK
echo Cleaning previous build...
call gradlew.bat clean

if %errorlevel% neq 0 (
    echo.
    echo Clean failed. Continuing with build...
)

echo Building APK...
call gradlew.bat assembleDebug

if %errorlevel% equ 0 (
    echo.
    echo Build successful!
    echo APK location: app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo You can now install the APK on your Android device.
    echo.
    echo To test the app, make sure your Flask app is running on http://127.0.0.1:5000/
) else (
    echo.
    echo Build failed. Please check the error messages above.
    echo Common issues:
    echo - Make sure ANDROID_HOME is set correctly
    echo - Ensure you have Android SDK API 21+ installed
    echo - Check that Java JDK 8+ is installed
)

pause
