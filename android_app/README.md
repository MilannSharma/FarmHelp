# farmHelp Android App

This Android app packages the Farmer Guider AI Flask web application into a mobile APK.

## Prerequisites

1. Android Studio (latest version recommended)
2. Android SDK with API level 21+ (Android 5.0+)
3. Java JDK 8 or higher

## Setup Instructions

### Option 1: Using Android Studio (Recommended)

1. **Clone or copy the android_app directory** to your Android Studio projects folder

2. **Open in Android Studio:**
   - Launch Android Studio
   - Select "Open an existing Android Studio project"
   - Navigate to the android_app directory and select it
   - Wait for Gradle sync to complete

3. **Configure the Flask App URL:**
   - The app currently loads `http://127.0.0.1:5000/` (localhost)
   - For production, change this URL in `MainActivity.java` to your hosted Flask app URL
   - For local testing, ensure your Flask app is running on port 5000

4. **Build the APK:**
   - Go to `Build > Build Bundle(s)/APK(s) > Build APK(s)`
   - Wait for the build to complete
   - Find the APK in `android_app/app/build/outputs/apk/debug/`

### Option 2: Using Command Line (Faster)

1. **Set ANDROID_HOME Environment Variable**
   - Follow the detailed guide in `ANDROID_SDK_SETUP_GUIDE.md`
   - This is required for command-line builds

2. **Download Gradle Wrapper (if needed)**
   ```bash
   cd android_app
   download_gradle_wrapper.bat
   ```

3. **Build the APK**
   ```bash
   cd android_app
   build_apk.bat
   ```

4. **Find the APK**
   - APK will be at: `android_app/app/build/outputs/apk/debug/app-debug.apk`

## Features

- WebView wrapper for the complete Farmer Guider AI web app
- Crop prediction functionality
- AI chatbot integration
- Responsive mobile interface
- Offline-capable (when Flask app is hosted locally)

## Important Notes

- The Flask app must be running and accessible for the Android app to work
- For offline functionality, consider hosting the Flask app on a local server or using a framework like Kivy for full Python integration
- Internet permission is required for external resources (Botpress chatbot, etc.)

## Troubleshooting

- If the app shows a blank screen, check that your Flask app is running and the URL is correct
- Ensure your device/emulator has internet access for external resources
- For local Flask app access, use your computer's IP address instead of 127.0.0.1
