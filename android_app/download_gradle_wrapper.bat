@echo off
echo Downloading Gradle Wrapper JAR...
echo.

REM Create wrapper directory if it doesn't exist
if not exist "gradle\wrapper" mkdir gradle\wrapper

REM Download the Gradle wrapper JAR
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/gradle/gradle/raw/v8.5.0/gradle/wrapper/gradle-wrapper.jar' -OutFile 'gradle\wrapper\gradle-wrapper.jar'}"

if %errorlevel% equ 0 (
    echo.
    echo Gradle wrapper JAR downloaded successfully!
    echo You can now run: gradlew.bat assembleDebug
) else (
    echo.
    echo Failed to download Gradle wrapper JAR.
    echo Please download it manually from:
    echo https://github.com/gradle/gradle/raw/v8.5.0/gradle/wrapper/gradle-wrapper.jar
    echo and place it in android_app\gradle\wrapper\gradle-wrapper.jar
)

pause
