# Clipboard Suite - Installation Guide

## ❌ Error: ModuleNotFoundError

If you see an error like:
```
ModuleNotFoundError: No module named 'pyperclip'
```

**This means the required packages are not installed!**

---

## ✅ FIX: Install Dependencies

### **Option 1: Automatic (EASIEST)**

1. In the clipboard-reply folder
2. **Double-click: `install_dependencies.bat`**
3. Wait for all packages to install (2-3 minutes)
4. Press any key when done
5. Now **double-click `run.bat`** to start!

### **Option 2: Manual (If Option 1 doesn't work)

1. Right-click in the clipboard-reply folder
2. Click **"Open PowerShell here"** (or Command Prompt)
3. Copy and paste this:
```
pip install pyperclip keyboard requests python-dotenv
```
4. Press Enter
5. Wait for installation
6. Now run: `python control_center.py`

---

## 📦 What Gets Installed:

- **pyperclip** - Clipboard management
- **keyboard** - Hotkey support
- **requests** - API communication
- **python-dotenv** - Configuration loading

---

## ✅ After Installation:

Just double-click **`run.bat`** and enjoy!

---

## 🆘 Still Having Issues?

1. Make sure Python is installed
2. Check "Add Python to PATH" is enabled
3. Restart your computer
4. Try Option 2 (Manual)

