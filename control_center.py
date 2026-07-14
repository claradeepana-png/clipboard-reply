import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyperclip
import keyboard
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import threading
import subprocess
import sys

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-3.5-turbo")
HOTKEY = os.getenv("HOTKEY", "ctrl+shift+r")

# Load prompts
try:
    with open('prompts.json', 'r') as f:
        PROMPTS_DATA = json.load(f)
except FileNotFoundError:
    PROMPTS_DATA = {'prompts': []}

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Clipboard Suite - Control Center")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#6366f1"
        self.success_color = "#4CAF50"
        self.warning_color = "#ff9800"
        self.error_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        # Config file
        self.config_file = "app_config.json"
        self.config = self.load_config()
        
        # History file
        self.history_file = "clipboard_history.json"
        self.history = self.load_history()
        
        self.todo_window = None
        self.clipboard_window = None
        self.is_hotkey_active = True
        
        self.setup_ui()
        self.setup_hotkey()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "api_key": OPENROUTER_API_KEY or "",
            "model": DEFAULT_MODEL,
            "hotkey": HOTKEY,
            "hotkey_enabled": True
        }
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-50:], f, indent=2)  # Keep last 50
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.accent_color)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="🚀 Clipboard Suite Control Center", 
                        font=("Arial", 14, "bold"), 
                        bg=self.accent_color, fg=self.fg_color)
        title.pack(pady=12)
        
        # Main notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style for notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.configure('TFrame', background=self.bg_color)
        
        # Tab 1: Dashboard
        self.setup_dashboard_tab()
        
        # Tab 2: Clipboard Reply
        self.setup_clipboard_tab()
        
        # Tab 3: Todo List
        self.setup_todo_tab()
        
        # Tab 4: Settings
        self.setup_settings_tab()
        
        # Tab 5: History
        self.setup_history_tab()
        
    def setup_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        dashboard_frame.configure(style='TFrame')
        
        # Status section
        status_frame = tk.Frame(dashboard_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        status_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(status_frame, text="⚙️  System Status", font=("Arial", 12, "bold"),
                bg="#2d2d44", fg=self.accent_color).pack(anchor=tk.W, padx=15, pady=10)
        
        # Status items
        api_status = "✅ Connected" if self.config["api_key"] else "❌ Not Set"
        hotkey_status = "✅ Active" if self.config["hotkey_enabled"] else "❌ Disabled"
        
        tk.Label(status_frame, text=f"API Key: {api_status}", font=("Arial", 10),
                bg="#2d2d44", fg=self.fg_color).pack(anchor=tk.W, padx=25, pady=5)
        
        tk.Label(status_frame, text=f"Hotkey: {hotkey_status} ({self.config['hotkey']})", 
                font=("Arial", 10),
                bg="#2d2d44", fg=self.fg_color).pack(anchor=tk.W, padx=25, pady=5)
        
        tk.Label(status_frame, text=f"Model: {self.config['model']}", font=("Arial", 10),
                bg="#2d2d44", fg=self.fg_color).pack(anchor=tk.W, padx=25, pady=5)
        
        # Quick actions
        actions_frame = tk.Frame(dashboard_frame, bg=self.bg_color)
        actions_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(actions_frame, text="⚡ Quick Actions", font=("Arial", 12, "bold"),
                bg=self.bg_color, fg=self.accent_color).pack(anchor=tk.W, pady=(0, 10))
        
        btn_frame = tk.Frame(actions_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="🤖 Open Clipboard Reply", command=self.open_clipboard_app,
                 bg=self.accent_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(btn_frame, text="📝 Open Todo List", command=self.open_todo_app,
                 bg=self.success_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5, pady=5)
        
        # Info section
        info_frame = tk.Frame(dashboard_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(info_frame, text="ℹ️  How to Use", font=("Arial", 12, "bold"),
                bg="#2d2d44", fg=self.accent_color).pack(anchor=tk.W, padx=15, pady=10)
        
        info_text = """
1. CLIPBOARD REPLY:
   • Copy any text
   • Press your hotkey (default: Ctrl+Shift+R)
   • Select a prompt
   • Get AI response!

2. TODO LIST:
   • Open Todo List from dashboard
   • Add tasks
   • Mark as done
   • Auto-saves!

3. SETTINGS:
   • Change API key
   • Set custom hotkey
   • Choose AI model
   • Toggle hotkey on/off
        """
        
        tk.Label(info_frame, text=info_text, font=("Arial", 9),
                bg="#2d2d44", fg=self.fg_color, justify=tk.LEFT).pack(anchor=tk.NW, padx=15, pady=10)
    
    def setup_clipboard_tab(self):
        clip_frame = ttk.Frame(self.notebook)
        self.notebook.add(clip_frame, text="🤖 Clipboard Reply")
        
        clip_frame.configure(style='TFrame')
        
        # Status
        status_label = tk.Label(clip_frame, text="✨ Ready to process clipboard text", 
                               font=("Arial", 10), bg=self.bg_color, fg=self.success_color)
        status_label.pack(pady=15)
        
        # Instructions
        instructions = """
QUICK START:
1. Copy any text to clipboard
2. Press: Ctrl+Shift+R (or your custom hotkey)
3. Choose a prompt from the popup
4. Wait for AI response
5. Copy result to clipboard

AVAILABLE PROMPTS:
        """
        
        tk.Label(clip_frame, text=instructions, font=("Arial", 9), 
                bg=self.bg_color, fg=self.fg_color, justify=tk.LEFT).pack(anchor=tk.NW, padx=15, pady=10)
        
        # Prompts list
        prompts_frame = tk.Frame(clip_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        prompts_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        scrollbar = tk.Scrollbar(prompts_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        prompts_text = tk.Text(prompts_frame, height=10, bg="#2d2d44", fg=self.fg_color,
                              yscrollcommand=scrollbar.set, relief=tk.FLAT, padx=10, pady=10)
        prompts_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=prompts_text.yview)
        
        for prompt in PROMPTS_DATA.get('prompts', []):
            prompts_text.insert(tk.END, f"{prompt['icon']} {prompt['name']}\n")
            prompts_text.insert(tk.END, f"   {prompt['prompt']}\n\n")
        
        prompts_text.config(state=tk.DISABLED)
        
        # Test button
        tk.Button(clip_frame, text="🧪 Test Hotkey", command=self.test_hotkey,
                 bg=self.accent_color, fg=self.fg_color, font=("Arial", 10),
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack(pady=15)
    
    def setup_todo_tab(self):
        todo_frame = ttk.Frame(self.notebook)
        self.notebook.add(todo_frame, text="📝 Todo List")
        
        todo_frame.configure(style='TFrame')
        
        tk.Label(todo_frame, text="📝 Task Management", font=("Arial", 12, "bold"),
                bg=self.bg_color, fg=self.accent_color).pack(pady=15)
        
        instructions = """
FEATURES:
✅ Add and manage tasks
✅ Mark tasks as complete
✅ Delete individual tasks
✅ Clear completed tasks
✅ Auto-save to local storage
✅ Persistent storage (todos.json)

KEYBOARD SHORTCUTS:
• Double-click task to toggle done
• Right-click to see options
• Enter to add task

STORAGE:
All tasks are saved automatically to todos.json
        """
        
        tk.Label(todo_frame, text=instructions, font=("Arial", 9),
                bg=self.bg_color, fg=self.fg_color, justify=tk.LEFT).pack(anchor=tk.NW, padx=15, pady=10)
        
        tk.Button(todo_frame, text="📝 Open Todo List", command=self.open_todo_app,
                 bg=self.success_color, fg=self.fg_color, font=("Arial", 11, "bold"),
                 padx=30, pady=15, relief=tk.FLAT, cursor="hand2").pack(pady=20)
    
    def setup_settings_tab(self):
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️  Settings")
        
        settings_frame.configure(style='TFrame')
        
        # API Key section
        api_frame = tk.Frame(settings_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        api_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(api_frame, text="🔑 API Key", font=("Arial", 11, "bold"),
                bg="#2d2d44", fg=self.accent_color).pack(anchor=tk.W, padx=15, pady=10)
        
        api_btn_frame = tk.Frame(api_frame, bg="#2d2d44")
        api_btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Button(api_btn_frame, text="📝 Update API Key", command=self.update_api_key,
                 bg=self.accent_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(api_btn_frame, text="🔗 Get API Key", command=self.open_api_link,
                 bg=self.warning_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Hotkey section
        hotkey_frame = tk.Frame(settings_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        hotkey_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(hotkey_frame, text="⌨️  Hotkey Settings", font=("Arial", 11, "bold"),
                bg="#2d2d44", fg=self.accent_color).pack(anchor=tk.W, padx=15, pady=10)
        
        hotkey_display = tk.Label(hotkey_frame, text=f"Current Hotkey: {self.config['hotkey']}", 
                                 font=("Arial", 10),
                                 bg="#2d2d44", fg=self.fg_color)
        hotkey_display.pack(anchor=tk.W, padx=15, pady=5)
        
        hotkey_btn_frame = tk.Frame(hotkey_frame, bg="#2d2d44")
        hotkey_btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Button(hotkey_btn_frame, text="🔧 Change Hotkey", command=self.change_hotkey,
                 bg=self.accent_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Model section
        model_frame = tk.Frame(settings_frame, bg="#2d2d44", relief=tk.RAISED, bd=1)
        model_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(model_frame, text="🧠 AI Model", font=("Arial", 11, "bold"),
                bg="#2d2d44", fg=self.accent_color).pack(anchor=tk.W, padx=15, pady=10)
        
        tk.Label(model_frame, text=f"Current Model: {self.config['model']}", font=("Arial", 10),
                bg="#2d2d44", fg=self.fg_color).pack(anchor=tk.W, padx=15, pady=5)
        
        models = [
            "openai/gpt-4",
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "google/palm-2",
            "mistral/mistral-7b"
        ]
        
        self.model_var = tk.StringVar(value=self.config['model'])
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var,
                                     values=models, state="readonly")
        model_dropdown.pack(fill=tk.X, padx=15, pady=(5, 15))
        model_dropdown.bind("<<ComboboxSelected>>", self.change_model)
    
    def setup_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📊 History")
        
        history_frame.configure(style='TFrame')
        
        tk.Label(history_frame, text="📊 Clipboard History", font=("Arial", 12, "bold"),
                bg=self.bg_color, fg=self.accent_color).pack(pady=15)
        
        # History list
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=15, bg="#2d2d44", fg=self.fg_color,
                                   yscrollcommand=scrollbar.set, relief=tk.FLAT, padx=10, pady=10)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        scrollbar.config(command=self.history_text.yview)
        
        # Refresh history display
        self.refresh_history_display()
        
        # Clear history button
        tk.Button(history_frame, text="🗑️  Clear History", command=self.clear_history,
                 bg=self.error_color, fg=self.fg_color, font=("Arial", 10),
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(pady=10)
    
    def refresh_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not self.history:
            self.history_text.insert(tk.END, "No history yet")
            self.history_text.config(state=tk.DISABLED)
            return
        
        for i, entry in enumerate(reversed(self.history[-50:]), 1):
            self.history_text.insert(tk.END, f"{i}. {entry['timestamp']}\n")
            self.history_text.insert(tk.END, f"   Input: {entry['input'][:50]}...\n")
            self.history_text.insert(tk.END, f"   Output: {entry['output'][:50]}...\n\n")
        
        self.history_text.config(state=tk.DISABLED)
    
    def update_api_key(self):
        new_key = simpledialog.askstring("Update API Key", 
                                        "Enter your OpenRouter API key (starts with sk-or-):")
        if new_key:
            self.config["api_key"] = new_key
            self.save_config()
            messagebox.showinfo("Success", "✅ API Key updated!")
    
    def change_hotkey(self):
        new_hotkey = simpledialog.askstring("Change Hotkey", 
                                           "Enter new hotkey (e.g., ctrl+shift+r, alt+r, shift+f1):")
        if new_hotkey:
            try:
                self.config["hotkey"] = new_hotkey
                self.save_config()
                self.setup_hotkey()
                messagebox.showinfo("Success", f"✅ Hotkey changed to: {new_hotkey}")
            except:
                messagebox.showerror("Error", "❌ Invalid hotkey format!")
    
    def change_model(self, event=None):
        self.config["model"] = self.model_var.get()
        self.save_config()
    
    def open_api_link(self):
        import webbrowser
        webbrowser.open("https://openrouter.ai")
    
    def test_hotkey(self):
        messagebox.showinfo("Test", "✅ Hotkey is working!\n\nNow go copy some text and press your hotkey!")
    
    def setup_hotkey(self):
        try:
            keyboard.remove_all_hotkeys()
            if self.config["hotkey_enabled"]:
                keyboard.add_hotkey(self.config["hotkey"], self.on_hotkey_pressed)
        except:
            pass
    
    def on_hotkey_pressed(self):
        try:
            clipboard_text = pyperclip.paste()
            if not clipboard_text.strip():
                messagebox.showwarning("Empty", "Clipboard is empty!")
                return
            
            # Show prompt selection
            self.show_prompt_dialog(clipboard_text)
        except:
            pass
    
    def show_prompt_dialog(self, text):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Prompt")
        dialog.geometry("400x400")
        dialog.configure(bg=self.bg_color)
        
        tk.Label(dialog, text="Choose a Prompt:", font=("Arial", 12, "bold"),
                bg=self.bg_color, fg=self.accent_color).pack(pady=10)
        
        frame = tk.Frame(dialog, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def process_with_prompt(prompt_text):
            dialog.destroy()
            self.process_clipboard(text, prompt_text)
        
        for prompt in PROMPTS_DATA.get('prompts', []):
            btn = tk.Button(frame, text=f"{prompt['icon']} {prompt['name']}",
                           command=lambda p=prompt['prompt']: process_with_prompt(p),
                           bg=self.accent_color, fg=self.fg_color,
                           font=("Arial", 10), padx=10, pady=8,
                           relief=tk.FLAT, cursor="hand2")
            btn.pack(fill=tk.X, pady=5)
    
    def process_clipboard(self, text, prompt):
        try:
            full_prompt = f"{prompt}\n\n{text}"
            
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.config["model"],
                "messages": [{"role": "user", "content": full_prompt}],
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            result = response.json()["choices"][0]["message"]["content"]
            
            pyperclip.copy(result)
            
            # Save to history
            self.history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input": text[:100],
                "output": result[:100]
            })
            self.save_history()
            
            messagebox.showinfo("Success", "✅ Response copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
    
    def open_clipboard_app(self):
        messagebox.showinfo("Info", "✨ Use the hotkey (Ctrl+Shift+R) to activate!\n\nOr use the 'Clipboard Reply' tab above.")
    
    def open_todo_app(self):
        if self.todo_window and self.todo_window.winfo_exists():
            self.todo_window.lift()
        else:
            subprocess.Popen([sys.executable, "todo_app.py"])
    
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Clear all clipboard history?"):
            self.history = []
            self.save_history()
            self.refresh_history_display()
            messagebox.showinfo("Success", "✅ History cleared!")

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
