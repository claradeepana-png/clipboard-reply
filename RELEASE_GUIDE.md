# 📦 Release Instructions for Clipboard Reply

Follow these steps to build and release the EXE file.

---

## 🚀 Step-by-Step Build Guide

### Prerequisites
- Windows 11
- Python 3.8+ installed ([Download](https://www.python.org/downloads/))
- Git (optional, for cloning)

### Step 1: Setup Environment

```bash
# Navigate to your clipboard-reply folder
cd C:\Users\YourName\Desktop\clipboard-reply

# Create .env file with your OpenRouter API key
# (Get key from https://openrouter.ai/keys)
```

Create a file named `.env`:
```
OPENROUTER_API_KEY=sk-or-your-api-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo
HOTKEY=ctrl+shift+r
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed keyboard pyperclip python-dotenv requests
```

### Step 3: Build the EXE

**Option A: Automatic (Recommended)**
```bash
.\build_exe.bat
```

**Option B: Manual**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Clipboard Reply" main.py
copy .env.example dist\
copy prompts.json dist\
```

### Step 4: Verify the Build

✅ Check that these files exist in the `dist` folder:
- `Clipboard Reply.exe` (main application)
- `prompts.json` (AI prompts)
- `.env.example` (configuration template)

### Step 5: Test the EXE

1. Navigate to `dist` folder
2. Double-click `Clipboard Reply.exe`
3. Add your API key to `.env` in the same folder
4. Press `Ctrl+Shift+R` and test with some copied text

---

## 📤 Upload to GitHub Releases

### Option A: GitHub Web Interface (Easiest)

1. Go to: **https://github.com/claradeepana-png/clipboard-reply/releases**
2. Click **"Create a new release"**
3. **Tag version:** `v1.0.0`
4. **Title:** `Clipboard Reply v1.0.0 - Stable Release`
5. **Description:**
```markdown
# 🤖 Clipboard Reply v1.0.0

Pre-built Windows 11 executable - No Python installation needed!

## Features
- ✨ 8 AI-powered prompts
- 🧠 Multiple AI models (GPT-4, Claude, Mistral, etc.)
- ⌨️ Global hotkey: Ctrl+Shift+R
- 📋 One-click copy to clipboard
- 🎨 Beautiful dark UI

## Installation
1. Download `Clipboard Reply.exe`
2. Double-click to run
3. Add your OpenRouter API key to `.env`
4. Press Ctrl+Shift+R to activate!

## Get Your Free API Key
1. Visit https://openrouter.ai
2. Sign up (free)
3. Copy your API key
4. Create `.env` file with: `OPENROUTER_API_KEY=your_key`

## System Requirements
- Windows 11
- 500MB disk space
- Internet connection

[📖 Full Documentation](https://github.com/claradeepana-png/clipboard-reply#readme)
```

6. Click **"Attach binaries"** → Upload:
   - `dist\Clipboard Reply.exe`
   - `.env.example`
   - `prompts.json`

7. Click **"Publish release"**

### Option B: GitHub CLI (Advanced)

```bash
# Install GitHub CLI from https://cli.github.com/

# Create release
gh release create v1.0.0 ^
  --title "Clipboard Reply v1.0.0 - Stable Release" ^
  --notes "Pre-built EXE for Windows 11. No Python needed!" ^
  "dist/Clipboard Reply.exe" ^
  ".env.example" ^
  "prompts.json"
```

---

## 📋 Pre-Release Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `.env.example` has correct format
- [ ] `prompts.json` has 8 prompts
- [ ] `main.py` tested locally
- [ ] EXE built successfully in `dist` folder
- [ ] EXE runs without errors
- [ ] Hotkey works (Ctrl+Shift+R)
- [ ] API key integration works
- [ ] README.md is up to date
- [ ] No debug files included

---

## 🔄 Update Process (Next Releases)

1. Make code changes
2. Test locally
3. Run `build_exe.bat` again
4. Go to GitHub Releases
5. Create new release with incremented version (v1.0.1, v1.1.0, etc.)
6. Upload new EXE

---

## 📝 Version Naming

- **v1.0.0** - Initial release
- **v1.0.1** - Bug fixes
- **v1.1.0** - New features
- **v2.0.0** - Major changes

---

## 🎯 What Users Will See

When users visit: **https://github.com/claradeepana-png/clipboard-reply**

They'll see:
1. **README.md** - Beautiful intro + features
2. **Green "Releases" tab** - Click to download
3. **Latest Release** - Shows `Clipboard Reply.exe`
4. **One-click download** - Direct link to EXE

---

## ✅ That's It!

Users can now:
1. Click the "Releases" tab
2. Download `Clipboard Reply.exe`
3. Double-click to run
4. Add API key
5. Start using it immediately!

---

## 🆘 Troubleshooting

### EXE won't build
- Reinstall pyinstaller: `pip install --upgrade pyinstaller`
- Make sure `.env` exists
- Try from a folder without spaces in path

### EXE won't start
- Check Windows 11 is up to date
- Try right-clicking → Run as Administrator
- Check `.env` file has API key

### Release upload failed
- Make sure you're logged in to GitHub
- Check file size (EXE should be ~100MB)
- Try uploading in parts

---

**Need help?** Check the main [README.md](README.md) for more details!
