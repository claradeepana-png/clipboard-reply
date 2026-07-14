import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import threading

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Todo List")
        self.root.geometry("350x500")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.resizable(False, False)
        
        # Colors (Dark theme)
        self.bg_color = "#1e1e2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#6366f1"
        self.done_color = "#4CAF50"
        self.delete_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        # Data file
        self.data_file = "todos.json"
        self.todos = []
        self.load_todos()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.accent_color)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="📝 Todo List", font=("Arial", 14, "bold"), 
                        bg=self.accent_color, fg=self.fg_color)
        title.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 11),
                                   bg="#2d2d44", fg=self.fg_color,
                                   relief=tk.FLAT, padx=10, pady=8)
        self.task_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_btn = tk.Button(input_frame, text="➕", command=self.add_task,
                           bg=self.accent_color, fg=self.fg_color,
                           font=("Arial", 10, "bold"),
                           relief=tk.FLAT, padx=10, cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Tasks list frame
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tasks_listbox = tk.Listbox(list_frame, 
                                       bg="#2d2d44", fg=self.fg_color,
                                       font=("Arial", 10),
                                       relief=tk.FLAT,
                                       yscrollcommand=scrollbar.set,
                                       activestyle='none')
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
        
        # Bind right-click
        self.tasks_listbox.bind("<Button-3>", self.show_context_menu)
        self.tasks_listbox.bind("<Double-1>", lambda e: self.toggle_task())
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        clear_btn = tk.Button(btn_frame, text="🗑️  Clear Done", command=self.clear_done,
                             bg="#3d3d54", fg=self.fg_color,
                             font=("Arial", 9),
                             relief=tk.FLAT, padx=10, cursor="hand2")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        delete_all_btn = tk.Button(btn_frame, text="🔴 Delete All", command=self.delete_all,
                                  bg=self.delete_color, fg=self.fg_color,
                                  font=("Arial", 9),
                                  relief=tk.FLAT, padx=10, cursor="hand2")
        delete_all_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_list,
                               bg=self.accent_color, fg=self.fg_color,
                               font=("Arial", 9),
                               relief=tk.FLAT, padx=10, cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh list
        self.refresh_list()
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task!")
            return
        
        task = {
            "id": datetime.now().timestamp(),
            "text": task_text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.todos.append(task)
        self.save_todos()
        self.task_entry.delete(0, tk.END)
        self.refresh_list()
    
    def toggle_task(self):
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Select a task first!")
            return
        
        index = selection[0]
        self.todos[index]["done"] = not self.todos[index]["done"]
        self.save_todos()
        self.refresh_list()
    
    def delete_task(self):
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Select a task to delete!")
            return
        
        index = selection[0]
        if messagebox.askyesno("Delete Task", f"Delete '{self.todos[index]['text']}'?"):
            self.todos.pop(index)
            self.save_todos()
            self.refresh_list()
    
    def clear_done(self):
        done_count = len([t for t in self.todos if t["done"]])
        if done_count == 0:
            messagebox.showinfo("No Done Tasks", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Clear Done Tasks", f"Delete {done_count} completed task(s)?"):
            self.todos = [t for t in self.todos if not t["done"]]
            self.save_todos()
            self.refresh_list()
    
    def delete_all(self):
        if not self.todos:
            messagebox.showinfo("Empty", "No tasks to delete!")
            return
        
        if messagebox.askyesno("Delete All", f"Delete all {len(self.todos)} tasks? This cannot be undone!"):
            self.todos = []
            self.save_todos()
            self.refresh_list()
    
    def refresh_list(self):
        self.tasks_listbox.delete(0, tk.END)
        
        if not self.todos:
            self.tasks_listbox.insert(tk.END, "✨ No tasks! Add one to get started!")
            self.tasks_listbox.itemconfig(0, {'bg': '#2d2d44', 'fg': '#888888'})
            return
        
        # Sort: incomplete first, then by creation time
        sorted_todos = sorted(self.todos, key=lambda x: (x["done"], x["created"]))
        
        for i, todo in enumerate(sorted_todos):
            if todo["done"]:
                text = f"✅ {todo['text']}"
                self.tasks_listbox.insert(tk.END, text)
                self.tasks_listbox.itemconfig(i, {'fg': '#888888'})
            else:
                text = f"⭕ {todo['text']}"
                self.tasks_listbox.insert(tk.END, text)
                self.tasks_listbox.itemconfig(i, {'fg': self.fg_color})
    
    def show_context_menu(self, event):
        selection = self.tasks_listbox.curselection()
        if not selection:
            return
        
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d44", fg=self.fg_color)
        menu.add_command(label="✅ Toggle Done", command=self.toggle_task)
        menu.add_command(label="🗑️  Delete", command=self.delete_task)
        menu.add_separator()
        menu.add_command(label="❌ Cancel", command=lambda: None)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def save_todos(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def load_todos(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.todos = json.load(f)
            except:
                self.todos = []
        else:
            self.todos = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
