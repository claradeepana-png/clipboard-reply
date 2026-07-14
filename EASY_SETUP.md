# 🤖 Clipboard Reply - Easy Setup Guide

## ⚠️ IMPORTANT: Before you start
You MUST have **Python installed** on your computer.

### Step 1: Install Python (IF YOU DON'T HAVE IT)

1. Go to: https://www.python.org/downloads/
2. Click the big **Download Python 3.11** button
3. Open the downloaded file and install
4. **IMPORTANT:** Check the box that says **"Add Python to PATH"** ✓
5. Click **Install Now**
6. Wait for it to finish

---

## 🚀 Super Easy Installation (3 Steps)

### Step 1: Download this folder
- Click the green **Code** button at the top
- Click **Download ZIP**
- Extract the ZIP file to your Desktop or Documents

### Step 2: Get Your API Key (FREE)
1. Go to: https://openrouter.ai
2. Click **Sign Up** (it's FREE)
3. Create your account
4. Go to **Keys** 
5. Copy your API key (starts with "sk-or-")
6. Keep it safe!

### Step 3: Create the `.env` File
1. Open Notepad
2. Copy and paste this:
```
OPENROUTER_API_KEY=paste_your_key_here
DEFAULT_MODEL=openai/gpt-3.5-turbo
HOTKEY=ctrl+shift+r
```
3. Replace `paste_your_key_here` with your actual API key
4. Click **File** → **Save As**
5. Name it: `.env` (exactly this!)
6. Set "Save as type" to **All Files**
7. Save it in the clipboard-reply folder

---

## ⚡ Run the App

### Option A: Easy Batch File (RECOMMENDED)
1. In the clipboard-reply folder, double-click **`run_simple.bat`**
2. A window opens - it installs everything automatically
3. Click anywhere to close when it says ✅ DONE
4. The app starts automatically!

### Option B: Manual Python
If Option A doesn't work:
1. Right-click in the clipboard-reply folder
2. Click **Open PowerShell here** (or Command Prompt)
3. Type: `python main.py`
4. Press Enter
5. The app opens!

---

## 🎯 Using the App

1. **Copy any text** to your clipboard
2. **Press `Ctrl+Shift+R`** (or your custom hotkey)
3. **Pick a prompt** (Summarize, Explain, etc.)
4. **Wait** for the AI response
5. **Click "Copy Result"** to copy the answer
6. **Paste it anywhere!**

---

## ❓ Troubleshooting

### Problem: "Python not found" or "Python is not recognized"
**Solution:**
- Reinstall Python
- Make sure to check "Add Python to PATH"
- Restart your computer after installing

### Problem: `.env` file won't work
**Solution:**
- Make sure it's named exactly `.env` (not `.env.txt`)
- It should be in the same folder as `main.py`
- Check that your API key is correct (starts with `sk-or-`)

### Problem: App opens but crashes
**Solution:**
- Make sure `.env` file is in the folder
- Check your API key is correct
- Try running with admin privileges

### Problem: Hotkey doesn't work
**Solution:**
- Try a different hotkey in `.env` file
- Examples: `alt+r` or `shift+f1`

---

## 📞 Need Help?

If something doesn't work:
1. Take a screenshot of the error
2. Share it with me
3. I'll help you fix it!

---

## 🎉 That's It!

You now have AI in your clipboard. Enjoy! 🚀

Press `Ctrl+Shift+R` and start using it!
