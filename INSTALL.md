# 🚀 Clipboard Reply - Installation Guide for Windows 11

## ⚡ Easiest Option: Pre-Built EXE (Coming Soon!)

We're preparing a pre-built EXE file that you can download directly from **Releases** without needing Python.

---

## 📋 Manual Setup (5 minutes)

If you want to build it yourself right now, follow these steps:

### Step 1: Install Python (if you don't have it)
- Download from: https://www.python.org/downloads/
- ✅ Check **"Add Python to PATH"** during installation
- Click **Install Now**

### Step 2: Setup Your API Key
1. Go to: https://openrouter.ai
2. Sign up (free account, get free credits)
3. Get your API key from Dashboard → API Keys
4. Create a file named `.env` in the app folder:
```
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxx
DEFAULT_MODEL=openai/gpt-3.5-turbo
HOTKEY=ctrl+shift+r
```

### Step 3: Install Dependencies
Open Command Prompt in the app folder and run:
```bash
pip install -r requirements.txt
```

### Step 4: Build the EXE
Double-click `build_exe.bat`
- This will create the standalone EXE in the `dist` folder
- No Python needed to run it after this!

### Step 5: Run It
- Find `Clipboard Reply.exe` in the `dist` folder
- Double-click to run
- Press `Ctrl+Shift+R` on any text to activate

---

## 🎯 How to Use

1. **Copy any text** on your screen
2. **Press `Ctrl+Shift+R`** (customizable hotkey)
3. **Click a prompt button** (Summarize, Explain, Email, etc.)
4. **Result appears instantly** in the app
5. **Click "📋 Copy Result"** to copy to clipboard
6. **Paste anywhere** with `Ctrl+V`

---

## 🧠 Available AI Models
- OpenAI GPT-4
- OpenAI GPT-3.5 Turbo
- Claude 3 Opus/Sonnet/Haiku
- Google PaLM-2
- Mistral 7B

---

## ❓ Need Help?
1. Check you have Python 3.8+
2. Check `.env` file has your API key
3. Try running `python main.py` to test

Enjoy! 🎉
