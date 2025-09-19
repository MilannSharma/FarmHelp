# How to Set ANDROID_HOME Environment Variable on Windows

## Step 1: Locate Your Android SDK Path

1. Open Android Studio.
2. Go to `File > Settings` (or `Android Studio > Preferences` on Mac).
3. Navigate to `Appearance & Behavior > System Settings > Android SDK`.
4. Note the "Android SDK Location" path at the top (e.g., `C:\Users\YourUser\AppData\Local\Android\Sdk`).

## Step 2: Set ANDROID_HOME Environment Variable

1. Press `Win + R`, type `sysdm.cpl`, and press Enter.
2. In the System Properties window, go to the `Advanced` tab.
3. Click on `Environment Variables`.
4. Under "User variables" or "System variables", click `New`.
5. Enter the following:
   - Variable name: `ANDROID_HOME`
   - Variable value: *Your Android SDK path from Step 1* (e.g., `C:\Users\YourUser\AppData\Local\Android\Sdk`)
6. Click `OK` to save.

## Step 3: Add SDK Tools to PATH

1. In the Environment Variables window, find the `Path` variable under "User variables" or "System variables".
2. Select it and click `Edit`.
3. Click `New` and add the following paths:
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\tools`
   - `%ANDROID_HOME%\tools\bin`
4. Click `OK` to save all changes.

## Step 4: Verify Setup

1. Open a new Command Prompt window.
2. Run:
   ```
   echo %ANDROID_HOME%
   ```
   It should print your SDK path.
3. Run:
   ```
   adb --version
   ```
   It should display the Android Debug Bridge version.

## Step 5: Retry Building APK

After setting the environment variable, restart your terminal or IDE and run the build script again:
```
cd android_app
build_apk.bat
```

---

If you need further assistance, feel free to ask!
