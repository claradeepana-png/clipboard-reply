import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import keyboard
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import threading
import sys

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-3.5-turbo")
HOTKEY = os.getenv("HOTKEY", "ctrl+shift+r")

# Load prompts
with open('prompts.json', 'r') as f:
    PROMPTS_DATA = json.load(f)

class ClipboardReplyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Reply")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set dark theme colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#6366f1"
        
        self.root.configure(bg=self.bg_color)
        
        self.current_model = DEFAULT_MODEL
        self.current_prompt_id = 1
        self.is_processing = False
        
        self.setup_ui()
        self.setup_hotkey()
        self.log("✅ App started. Press Ctrl+Shift+R to activate.")
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.accent_color)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="🤖 Clipboard Reply", font=("Arial", 16, "bold"), 
                         bg=self.accent_color, fg=self.fg_color)
        title.pack(pady=10)
        
        # Model Selection
        model_frame = tk.Frame(self.root, bg=self.bg_color)
        model_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(model_frame, text="Model:", font=("Arial", 10, "bold"), 
                bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT)
        
        models = [
            "openai/gpt-4",
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-haiku",
            "google/palm-2",
            "mistral/mistral-7b"
        ]
        
        self.model_var = tk.StringVar(value=self.current_model)
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                     values=models, state="readonly", width=30)
        model_dropdown.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        model_dropdown.bind("<<ComboboxSelected>>", self.on_model_changed)
        
        # Prompt Selection
        prompt_frame = tk.Frame(self.root, bg=self.bg_color)
        prompt_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(prompt_frame, text="Prompts:", font=("Arial", 10, "bold"), 
                bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W)
        
        # Prompt buttons grid
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.BOTH, padx=15, pady=10, expand=False)
        
        self.prompt_buttons = {}
        for prompt in PROMPTS_DATA['prompts']:
            btn = tk.Button(button_frame, 
                           text=f"{prompt['icon']} {prompt['name']}",
                           command=lambda p=prompt: self.on_prompt_selected(p),
                           bg=self.accent_color, fg=self.fg_color,
                           font=("Arial", 9),
                           padx=10, pady=8,
                           relief=tk.RAISED,
                           bd=0,
                           cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3, pady=3)
            self.prompt_buttons[prompt['id']] = btn
        
        # Output display
        output_label = tk.Label(self.root, text="Output:", font=("Arial", 10, "bold"), 
                               bg=self.bg_color, fg=self.fg_color)
        output_label.pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        self.output_text = tk.Text(self.root, height=12, width=60,
                                   bg="#2d2d44", fg=self.fg_color,
                                   font=("Courier", 9),
                                   relief=tk.FLAT,
                                   padx=10, pady=10)
        self.output_text.pack(padx=15, pady=(0, 10), fill=tk.BOTH, expand=True)
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, padx=15, pady=10)
        
        copy_btn = tk.Button(btn_frame, text="📋 Copy Result", command=self.copy_result,
                            bg=self.accent_color, fg=self.fg_color,
                            font=("Arial", 10, "bold"),
                            padx=15, pady=8,
                            relief=tk.FLAT,
                            cursor="hand2")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(btn_frame, text="🗑️  Clear", command=self.clear_output,
                             bg="#3d3d54", fg=self.fg_color,
                             font=("Arial", 10),
                             padx=15, pady=8,
                             relief=tk.FLAT,
                             cursor="hand2")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_hotkey(self):
        try:
            keyboard.add_hotkey(HOTKEY, self.on_hotkey_pressed)
        except Exception as e:
            self.log(f"❌ Hotkey error: {e}")
    
    def on_hotkey_pressed(self):
        if self.is_processing:
            return
        
        try:
            clipboard_text = pyperclip.paste()
            if not clipboard_text.strip():
                self.log("⚠️  Clipboard is empty!")
                return
            
            self.log(f"📋 Processing: {clipboard_text[:50]}...")
            self.is_processing = True
            
            # Run in background thread
            thread = threading.Thread(target=self.process_text, args=(clipboard_text,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.is_processing = False
    
    def on_prompt_selected(self, prompt):
        self.current_prompt_id = prompt['id']
        clipboard_text = pyperclip.paste()
        
        if not clipboard_text.strip():
            self.log("⚠️  Clipboard is empty!")
            return
        
        self.log(f"🔄 Using prompt: {prompt['name']}")
        self.is_processing = True
        
        thread = threading.Thread(target=self.process_text, args=(clipboard_text, prompt['prompt']))
        thread.daemon = True
        thread.start()
    
    def process_text(self, text, custom_prompt=None):
        try:
            model = self.model_var.get()
            
            if custom_prompt:
                full_prompt = f"{custom_prompt}\n\n{text}"
            else:
                full_prompt = text
            
            self.log(f"⏳ Sending to {model}...")
            
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": full_prompt}],
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            result = data["choices"][0]["message"]["content"]
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, result)
            self.log(f"✅ Done!")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            self.is_processing = False
    
    def on_model_changed(self, event=None):
        self.current_model = self.model_var.get()
        self.log(f"🧠 Model changed to: {self.current_model}")
    
    def copy_result(self):
        text = self.output_text.get(1.0, tk.END).strip()
        if text:
            pyperclip.copy(text)
            self.log("✅ Copied to clipboard!")
        else:
            self.log("⚠️  No text to copy!")
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.log("🗑️  Cleared!")
    
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def main():
    if not OPENROUTER_API_KEY:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "OPENROUTER_API_KEY not found in .env file!\n\nPlease add your API key to the .env file.")
        sys.exit(1)
    
    root = tk.Tk()
    app = ClipboardReplyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
