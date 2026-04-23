import tkinter as tk
from tkinter import messagebox
from datetime import datetime

tasks = []

# add task
def add_task():
    subject = subject_entry.get()
    deadline = deadline_entry.get()
    priority = priority_var.get()

    if subject == "" or deadline == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
    except:
        messagebox.showerror("Error", "Use date format YYYY-MM-DD")
        return

    tasks.append({
        "subject": subject,
        "deadline": deadline_date,
        "priority": priority,
        "status": "Pending"
    })

    update_lists()
    clear_fields()


# update display
def update_lists():
    pending_list.delete(0, tk.END)
    completed_list.delete(0, tk.END)

    today = datetime.now()

    for task in tasks:
        text = f"{task['subject']} | {task['deadline'].date()} | {task['priority']}"

        if task["status"] == "Completed":
            completed_list.insert(tk.END, "✔ " + text)
        else:
            if task["deadline"] < today:
                pending_list.insert(tk.END, "⚠ OVERDUE: " + text)
            else:
                pending_list.insert(tk.END, text)


# mark complete
def mark_complete():
    try:
        index = pending_list.curselection()[0]
        count = 0

        for task in tasks:
            if task["status"] == "Pending":
                if count == index:
                    task["status"] = "Completed"
                    break
                count += 1

        update_lists()
    except:
        messagebox.showwarning("Error", "Select a pending task")


# delete task
def delete_task():
    try:
        index = pending_list.curselection()[0]
        count = 0

        for i, task in enumerate(tasks):
            if task["status"] == "Pending":
                if count == index:
                    tasks.pop(i)
                    break
                count += 1

        update_lists()
    except:
        messagebox.showwarning("Error", "Select a task to delete")


def clear_fields():
    subject_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)


# GUI
root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("650x450")

# INPUT SECTION
tk.Label(root, text="Subject").grid(row=0, column=0)
subject_entry = tk.Entry(root)
subject_entry.grid(row=0, column=1)

tk.Label(root, text="Deadline (YYYY-MM-DD)").grid(row=1, column=0)
deadline_entry = tk.Entry(root)
deadline_entry.grid(row=1, column=1)

tk.Label(root, text="Priority").grid(row=2, column=0)
priority_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, priority_var, "High", "Medium", "Low").grid(row=2, column=1)

# BUTTONS
tk.Button(root, text="Add Task", command=add_task).grid(row=3, column=0, pady=10)
tk.Button(root, text="Mark Completed", command=mark_complete).grid(row=3, column=1)
tk.Button(root, text="Delete Task", command=delete_task).grid(row=3, column=2)

# LISTS
tk.Label(root, text="Pending Tasks").grid(row=4, column=0)
pending_list = tk.Listbox(root, width=40, height=10)
pending_list.grid(row=5, column=0, columnspan=2)

tk.Label(root, text="Completed Tasks").grid(row=4, column=2)
completed_list = tk.Listbox(root, width=30, height=10)
completed_list.grid(row=5, column=2)

root.mainloop()