import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("To Do List with Status")
root.geometry("700x600+400+100")
root.resizable(False, False)

# Color Palette
bg_color = "#2c3e50"  # Dark Blue background
frame_bg = "#34495e"  # Frame background
button_bg = "#1abc9c"  # Teal Button
button_hover_bg = "#16a085"  # Darker Teal on hover
text_color = "#ecf0f1"  # Light text color
entry_bg = "#ecf0f1"  # Light entry box background
entry_fg = "#2c3e50"  # Dark text for entry

# Task list, now includes task description and status
task_list = []

# Function to load tasks from file
# Function to load tasks from file
def openTaskFile():
    try:
        with open("Task.txt", "r") as taskfile:
            tasks = taskfile.readlines()
        for task in tasks:
            if task.strip():
                # Split by '|' to get task and status, assign default status if not found
                parts = task.strip().split('|')
                if len(parts) == 2:
                    task_description, task_status = parts
                else:
                    task_description = parts[0]
                    task_status = "Ongoing"  # Default status if no status is present

                task_list.append({"task": task_description, "status": task_status})
                listbox.insert(tk.END, f"{task_description} ({task_status})")
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open("Task.txt", "w") as taskfile:
            pass


# Function to save tasks to file
def saveTasks():
    with open("Task.txt", "w") as taskfile:
        for task_dict in task_list:
            taskfile.write(f'{task_dict["task"]}|{task_dict["status"]}\n')

# Function to add a task
def addTask():
    task = task_entry.get().strip()
    if task != "":
        status = status_var.get()
        task_dict = {"task": task, "status": status}
        task_list.append(task_dict)
        listbox.insert(tk.END, f"{task} ({status})")
        task_entry.delete(0, tk.END)  # Clear entry box
        saveTasks()  # Save the updated list to file
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to delete a selected task
def deleteTask():
    try:
        selected_task_index = listbox.curselection()[0]
        task_list.pop(selected_task_index)
        listbox.delete(selected_task_index)
        saveTasks()  # Save the updated list to file
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Function to edit the status of the selected task
def editTaskStatus():
    try:
        selected_task_index = listbox.curselection()[0]
        new_status = status_var.get()
        task_list[selected_task_index]["status"] = new_status
        listbox.delete(selected_task_index)
        listbox.insert(selected_task_index, f'{task_list[selected_task_index]["task"]} ({new_status})')
        saveTasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Hover effect for buttons
def on_enter(event, button):
    button['bg'] = button_hover_bg

def on_leave(event, button):
    button['bg'] = button_bg

# Create and place the frames and widgets
root.configure(bg=bg_color)

# Top heading
heading = tk.Label(root, text="To Do List with Status", font="arial 24 bold", fg=text_color, bg=bg_color)
heading.pack(pady=20)

# Main frame for task entry
frame = tk.Frame(root, width=400, height=50, bg=frame_bg)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=18, font="arial 20", bd=0, bg=entry_bg, fg=entry_fg)
task_entry.grid(row=0, column=0, padx=10, pady=10)
task_entry.focus()

# Status Dropdown
status_var = tk.StringVar(value="Ongoing")
status_dropdown = tk.OptionMenu(frame, status_var, "Ongoing", "Finished")
status_dropdown.config(font="arial 15", bg=button_bg, fg="white", bd=0)
status_dropdown.grid(row=0, column=1, padx=10)

# Add Button
add_button = tk.Button(frame, text="ADD", font="arial 20 bold", width=6, bg=button_bg, fg="#fff", bd=0, command=addTask)
add_button.grid(row=0, column=2, padx=10)
add_button.bind("<Enter>", lambda event, btn=add_button: on_enter(event, btn))
add_button.bind("<Leave>", lambda event, btn=add_button: on_leave(event, btn))

# Frame for task list and scrollbar
frame1 = tk.Frame(root, bd=3, width=700, height=280, bg=frame_bg)
frame1.pack(pady=10)

listbox = tk.Listbox(frame1, font=('arial', 12), width=40, height=10, bg=entry_bg, fg=entry_fg, selectbackground=button_bg, bd=0)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Delete task button
delete_button = tk.Button(root, text="DELETE", font="arial 20 bold", width=10, bg=button_bg, fg="#fff", bd=0, command=deleteTask)
delete_button.pack(pady=10)
delete_button.bind("<Enter>", lambda event, btn=delete_button: on_enter(event, btn))
delete_button.bind("<Leave>", lambda event, btn=delete_button: on_leave(event, btn))

# Edit status button
edit_button = tk.Button(root, text="EDIT STATUS", font="arial 20 bold", width=15, bg=button_bg, fg="#fff", bd=0, command=editTaskStatus)
edit_button.pack(pady=10)
edit_button.bind("<Enter>", lambda event, btn=edit_button: on_enter(event, btn))
edit_button.bind("<Leave>", lambda event, btn=edit_button: on_leave(event, btn))

# Load tasks when the program starts
openTaskFile()

root.mainloop()
