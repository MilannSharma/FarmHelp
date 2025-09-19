# Step-by-Step Guide to Run Farmer Guider AI App

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Android Studio** (latest version) or Android SDK
3. **Java JDK 8+** installed
4. **Android device or emulator** for testing

---

## Step 1: Prepare the Flask Backend

### 1.1 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 1.2 Verify Model and Data Files
Ensure these files exist in your project root:
- `model.pkl` (ML model)
- `agriculture_knowledge_base.json` (knowledge base)
- `crops_dataset.csv` (training data)
- All files in `templates/` directory

### 1.3 Test Flask App Locally
```bash
# Run the Flask app
python app.py
```

**Expected Output:**
```
🌐 Launching app at: http://127.0.0.1:5000/
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 1.4 Verify Flask App is Working
1. Open browser and go to: `http://127.0.0.1:5000/`
2. Test the main features:
   - Home page loads
   - Navigation works
   - Chat with Nax AI works
   - Dashboard loads
3. Keep the Flask app running in the background

---

## Step 2: Build the Android APK

### Option A: Using Android Studio (Recommended)

#### 2.1 Open Project in Android Studio
1. Launch Android Studio
2. Select "Open an existing Android Studio project"
3. Navigate to `android_app` folder and select it
4. Wait for Gradle sync to complete

#### 2.2 Configure Build Settings
1. In Android Studio, go to `File > Project Structure`
2. Ensure:
   - Compile SDK Version: API 34
   - Target SDK Version: API 34
   - Minimum SDK Version: API 21

#### 2.3 Build the APK
1. Go to `Build > Build Bundle(s)/APK(s) > Build APK(s)`
2. Wait for build to complete
3. Find APK at: `android_app/app/build/outputs/apk/debug/app-debug.apk`

### Option B: Using Command Line (Windows)

#### 2.1 Navigate to Android Project
```bash
cd android_app
```

#### 2.2 Run Build Script
```bash
build_apk.bat
```

**Expected Output:**
```
Building farmHelp APK...

Cleaning previous build...
Building APK...

Build successful!
APK location: app\build\outputs\apk\debug\app-debug.apk
```

---

## Step 3: Install and Run on Android Device

### 3.1 Enable Developer Options (if not already enabled)
1. Go to Android Settings
2. Tap "About Phone" 7 times
3. Go back to Settings > Developer Options
4. Enable "USB Debugging"
5. Enable "Install via USB"

### 3.2 Transfer APK to Device
**Method 1: USB Transfer**
1. Connect Android device to computer via USB
2. Copy `app-debug.apk` to device storage
3. On device, open File Manager
4. Navigate to the APK file
5. Tap to install

**Method 2: Email/Cloud Transfer**
1. Upload APK to Google Drive/Dropbox
2. Download on Android device
3. Open downloaded file to install

### 3.3 Install the APK
1. When prompted, tap "Install"
2. If asked about permissions, grant them
3. Wait for installation to complete

### 3.4 Launch the App
1. Find "farmHelp" app icon on home screen or app drawer
2. Tap to launch
3. The app will load the Flask web interface

---

## Step 4: Test the App Functionality

### 4.1 Basic Navigation Test
1. **Home Page**: Should load with welcome message and navigation
2. **Chat with Nax AI**: Should open chat interface with Botpress integration
3. **Dashboard**: Should display analytics and data
4. **Crop Prediction**: Should allow input of parameters and show results

### 4.2 Feature Testing
1. **Chatbot**: Try asking farming-related questions
2. **Prediction**: Enter sample values (temperature, humidity, pH, rainfall)
3. **Navigation**: Test all menu links
4. **Responsiveness**: Test on different screen orientations

---

## Step 5: Troubleshooting

### Flask App Issues
**Problem**: Flask app won't start
**Solution**:
```bash
# Check Python version
python --version

# Install missing dependencies
pip install flask joblib numpy scikit-learn

# Check if model file exists
dir model.pkl
```

**Problem**: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
```

### Android Build Issues
**Problem**: Build fails with Gradle errors
**Solution**:
1. In Android Studio: `File > Invalidate Caches / Restart`
2. Clean project: `Build > Clean Project`
3. Rebuild: `Build > Rebuild Project`

**Problem**: SDK not found
**Solution**:
1. In Android Studio: `File > Settings > Appearance & Behavior > System Settings > Android SDK`
2. Install required SDK versions

### Android App Issues
**Problem**: App shows blank screen
**Solution**:
1. Ensure Flask app is running on the correct IP/port
2. Check device has internet access
3. For local testing, use your computer's IP instead of 127.0.0.1

**Problem**: Cannot install APK
**Solution**:
1. Enable "Install unknown apps" in Settings > Apps
2. Check device storage space
3. Try different APK transfer method

---

## Step 6: Production Deployment (Optional)

### 6.1 Deploy Flask App to Server
For production use, deploy Flask app to a cloud server:

1. **Heroku Deployment**:
   ```bash
   # Install Heroku CLI
   # Create requirements.txt and Procfile
   # Deploy
   heroku create your-app-name
   git push heroku main
   ```

2. **Update Android App**:
   - Change URL in `MainActivity.java` from `http://127.0.0.1:5000/` to your deployed URL
   - Rebuild APK

### 6.2 Build Release APK
1. In Android Studio: `Build > Generate Signed Bundle/APK`
2. Create signing key or use existing
3. Select APK, fill details
4. Build and distribute

---

## Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test Flask app
python app.py

# 3. Build Android APK
cd android_app
build_apk.bat

# 4. Install APK on device and test
```

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure Flask app is accessible from Android device
4. Check Android Studio logs for build errors

The app should now be fully functional on your Android device!
