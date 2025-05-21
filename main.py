import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime, date

TASKS_FILE = "tasks.json"

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager App")
        self.tasks = []

        # Heading
        tk.Label(root, text="Task Manager App with Priority, Filter & Reminders",
                 font=("Helvetica", 14, "bold"), fg="blue").pack(pady=10)
  # Listbox
        self.task_listbox = tk.Listbox(root, width=75, height=12, font=("Helvetica", 11))
        self.task_listbox.pack(pady=10)

        # Dropdowns
        dropdown_frame = tk.Frame(root)
        dropdown_frame.pack()

        self.filter_var = tk.StringVar()
        self.sort_var = tk.StringVar()
        self.filter_var.set("All Categories")
        self.sort_var.set("Sort By")

        tk.Label(dropdown_frame, text="Filter:").grid(row=0, column=0, padx=5)
        self.filter_menu = ttk.Combobox(dropdown_frame, textvariable=self.filter_var, state="readonly")
        self.filter_menu.grid(row=0, column=1)

        tk.Label(dropdown_frame, text="Sort:").grid(row=0, column=2, padx=5)
        self.sort_menu = ttk.Combobox(dropdown_frame, textvariable=self.sort_var,
                                      values=["Due Date", "Priority"], state="readonly")
        self.sort_menu.grid(row=0, column=3)

        tk.Button(dropdown_frame, text="Apply", command=self.view_tasks).grid(row=0, column=4, padx=5)
 # Buttons
        tk.Button(root, text="Add Task", width=18, command=self.add_task).pack(pady=2)
        tk.Button(root, text="Update Task", width=18, command=self.update_task).pack(pady=2)
        tk.Button(root, text="Delete Task", width=18, command=self.delete_task).pack(pady=2)

        # Load & show
        self.load_tasks()
        self.view_tasks()
        self.show_today_reminders()

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if not title:
            return

        due = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
        category = simpledialog.askstring("Category", "Enter task category:")
        priority = simpledialog.askstring("Priority", "Enter priority (High, Medium, Low):", initialvalue="Medium")

        task = {
            "title": title,
            "due": due,
            "category": category,
            "priority": priority
        }

        self.tasks.append(task)
        self.save_tasks()
        self.update_filter_menu()
        self.view_tasks()

    def update_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to update.")
            return

        index = selected[0]
        current = self.filtered_tasks()[index]

        title = simpledialog.askstring("Update Task", "Edit title:", initialvalue=current["title"])
        due = simpledialog.askstring("Due Date", "Edit due date (YYYY-MM-DD):", initialvalue=current["due"])
        category = simpledialog.askstring("Category", "Edit category:", initialvalue=current["category"])
        priority = simpledialog.askstring("Priority", "Edit priority (High, Medium, Low):", initialvalue=current["priority"])

        current.update({"title": title, "due": due, "category": category, "priority": priority})
        self.save_tasks()
        self.update_filter_menu()
        self.view_tasks()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        index = selected[0]
        full_list = self.filtered_tasks()
        real_index = self.tasks.index(full_list[index])
        del self.tasks[real_index]

        self.save_tasks()
        self.update_filter_menu()
        self.view_tasks()

    def view_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks_to_display = self.filtered_tasks()

        if self.sort_var.get() == "Due Date":
            tasks_to_display.sort(key=lambda x: x.get("due", ""))
        elif self.sort_var.get() == "Priority":
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            tasks_to_display.sort(key=lambda x: priority_order.get(x.get("priority", "Medium"), 2))

        for i, task in enumerate(tasks_to_display, 1):
            task_display = f"{i}. {task['title']} | Due: {task['due']} | Cat: {task['category']} | Priority: {task['priority']}"
            self.task_listbox.insert(tk.END, task_display)

    def filtered_tasks(self):
        category_filter = self.filter_var.get()
        if category_filter == "All Categories":
            return self.tasks
        return [t for t in self.tasks if t['category'] == category_filter]

    def update_filter_menu(self):
        categories = list({t["category"] for t in self.tasks})
        self.filter_menu["values"] = ["All Categories"] + categories
        if self.filter_var.get() not in self.filter_menu["values"]:
            self.filter_var.set("All Categories")

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
        self.update_filter_menu()

    def show_today_reminders(self):
        today = date.today().strftime("%Y-%m-%d")
        today_tasks = [t for t in self.tasks if t.get("due") == today]

        if today_tasks:
            msg = "\n".join([f"- {t['title']} ({t['category']}, {t['priority']})" for t in today_tasks])
            messagebox.showinfo("Tasks Due Today", f"You have the following tasks due today:\n\n{msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()








