# TASK MANAGEMENT SYSTEM - VERSION 2
# Import tkinter so we can create the graphical user interface (GUI).
import tkinter as tk

# Import messagebox so the program can show pop-up messages and errors.
from tkinter import messagebox

# Import datetime so we can check whether the user entered a valid date.
from datetime import datetime
from unicodedata import name

# TASK CLASS

# Create a class called Task to represent one individual task.
class Task:

    # This function runs whenever a new Task object is created.
    def __init__(self, name, priority, due_date, completed=False):

        # Store the task name inside the Task object.
        self.name = name

        # Store the priority of the task inside the Task object.
        self.priority = priority

        # Store the due date of the task inside the Task object.
        self.due_date = due_date

        # Store whether the task is completed.
        # New tasks are not completed by default.
        self.completed = completed

# TASK MANAGER CLASS

# Create a class called TaskManager.
# This class controls the tasks and the main task functions.
class TaskManager:

    # This function runs when the TaskManager is created.
    def __init__(self):

        # Create an empty list to store all Task objects.
        self.tasks = []

        # Load any tasks that were previously saved in the text file.
        self.load_tasks()

    # ADD TASK

    # This function adds a new task to the task list.
    def add_task(self):

        # Get the task name from the name input box.
        # strip() removes unnecessary spaces from the beginning/end.
        name = name_entry.get().strip()

        # Get the priority selected by the user.
        priority = priority_var.get()

        # Get the due date entered by the user.
        due_date = date_entry.get().strip()

        # Store the priority options allowed by the program.
        valid_priorities = ["High", "Medium", "Low"]

        # Validate task name.
        if name == "":
            messagebox.showerror(
                "Error",
                "Task name cannot be empty."
            )
            return

        # Check that the task name is long enough.
        if len(name) < 3:
            messagebox.showerror(
                "Error",
                "Task name must be at least 3 characters long."
            )
            return

        # VALIDATE PRIORITY

        # Check that the selected priority is valid.
        if priority not in valid_priorities:
            messagebox.showerror(
                "Error",
                "Please select High, Medium, or Low priority."
            )
            return
        # VALIDATE DATE

        # Validate the due date.
        try:
            # Convert the entered text into a real date.
            valid_date = datetime.strptime(due_date, "%d/%m/%Y")

        except ValueError:
            # Tell the user if the date is invalid.
            messagebox.showerror(
                "Error",
                "Please enter a valid date using DD/MM/YYYY."
            )
            return
        # Check that the due date is not in the past.
        if valid_date < datetime.now():
            messagebox.showerror(
        "Error",
        "The due date cannot be in the past."
        )
            return
        # CREATE THE TASK

        # Create a new Task object using the information entered.
        # The task is automatically set as not completed.
        self.tasks.append(
            Task(name, priority, due_date)
        )


        # Save the updated task list to the text file.
        self.save_tasks()


        # Clear the task name input box.
        name_entry.delete(0, tk.END)

        # Clear the due date input box.
        date_entry.delete(0, tk.END)

        # Reset the priority back to Medium.
        priority_var.set("Medium")


        # Refresh the task list so the new task appears.
        self.view_tasks()


        # Tell the user that the task was successfully added.
        messagebox.showinfo(
            "Success",
            "Task added successfully!"
        )

    # VIEW TASKS
    def view_tasks(self):
        # Clear the current task list before displaying it again.
        task_list.delete(0, tk.END)

        # Check if there are no tasks.
        if not self.tasks:
            task_list.insert(
                tk.END,
                "No tasks available."
            )
            return

        # Go through each task and give it a number.
        for number, task in enumerate(self.tasks, 1):

            # Decide which status should be displayed.
            if task.completed:
                status = "Completed"
            else:
                status = "Not Completed"

            # Create a clear display line for the task.
            task_text = (
                f"{number}. {task.name} | "
                f"Priority: {task.priority} | "
                f"Due: {task.due_date} | "
                f"Status: {status}"
            )

            # Add the task to the Listbox.
            task_list.insert(
                tk.END,
                task_text
            )

     # COMPLETE TASK
    def complete_task(self):
            # Get the task selected by the user.
            selected = task_list.curselection()

            # Check if the user selected a task.
            if not selected:
                messagebox.showerror(
                    "Error",
                    "Please select a task."
                )
                return

            # Get the selected Task object from the list.
            task = self.tasks[selected[0]]

            # Check if the task is already completed.
            if task.completed:
                messagebox.showinfo(
                    "Information",
                    "This task is already completed."
                )
                return

            # Mark the task as completed.
            task.completed = True

            # Save the updated task list.
            self.save_tasks()

            # Refresh the task list.
            self.view_tasks()

            # Tell the user the task was completed.
            messagebox.showinfo(
                "Success",
                "Task marked as completed!"
            )

    # DELETE TASK
    def delete_task(self):
        # Get the task selected by the user.
        selected = task_list.curselection()

        # Check if the user selected a task.
        if not selected:
            messagebox.showerror(
                "Error",
                "Please select a task to delete."
            )
            return

        # Store the position of the selected task.
        task_index = selected[0]

        # Get the selected Task object.
        task = self.tasks[task_index]

        # Ask the user to confirm the deletion.
        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete '{task.name}'?"
        )

        # Only delete the task if the user chooses Yes.
        if confirm:
            # Remove the selected task from the task list.
            self.tasks.pop(task_index)

            # Save the updated task list.
            self.save_tasks()

            # Refresh the task list.
            self.view_tasks()

            # Tell the user the task was deleted.
            messagebox.showinfo(
                "Success",
                "Task deleted successfully."
            )

    # SAVE TASKS
    def save_tasks(self):
        # Try to save all tasks to the text file.
        try:
            with open("tasks.txt", "w") as file:

                # Go through each task in the task list.
                for task in self.tasks:

                    # Convert the completed status into 1 or 0.
                    completed = "1" if task.completed else "0"

                    # Write the task information to the file.
                    file.write(
                        f"{task.name}|"
                        f"{task.priority}|"
                        f"{task.due_date}|"
                        f"{completed}\n"
                    )

        except OSError:
            # Show an error if the file cannot be saved.
            messagebox.showerror(
                "Save Error",
                "The tasks could not be saved."
            )
    # LOAD TASKS
    def load_tasks(self):
        # Try to open the file containing saved tasks.
        try:
            with open("tasks.txt", "r") as file:

                # Read each saved task one line at a time.
                for line in file:

                    # Remove extra spaces and split the data.
                    parts = line.strip().split("|")

                    # Check that the saved data has four parts.
                    if len(parts) != 4:
                        continue

                    # Store each part of the saved task.
                    name, priority, due_date, completed = parts

                    # Check that the saved priority is valid.
                    if priority not in ["High", "Medium", "Low"]:
                        continue

                    # Check that the completion value is valid.
                    if completed not in ["0", "1"]:
                        continue

                    # Create the Task object and add it to the list.
                    self.tasks.append(
                        Task(
                            name,
                            priority,
                            due_date,
                            completed == "1"
                        )
                    )

        except FileNotFoundError:
            # No saved task file exists yet.
            pass
        except OSError:
            # Tell the user if the task file cannot be opened.
            messagebox.showerror(
                "Load Error",
                "The saved tasks could not be loaded."
            )
# TKINTER GUI

# Create the main Tkinter window.
window = tk.Tk()


# Set the title shown at the top of the window.
window.title("Task Management System - Version 2")


# Set the size of the window to 850 pixels wide and 550 pixels high.
window.geometry("850x550")


# TITLE

# Create a large title label for the program.
tk.Label(
    window,

    # Text displayed by the label.
    text="TASK MANAGEMENT SYSTEM",

    # Set the font to Arial, size 20, and bold.
    font=("Arial", 20, "bold")

# Add the label to the window with 15 pixels of vertical spacing.
).pack(pady=15)


# INPUT FRAME


# Create a frame to hold the input fields.
input_frame = tk.Frame(window)


# Place the input frame inside the main window.
input_frame.pack()


# TASK NAME

# Create a label telling the user what the first input is for.
tk.Label(
    input_frame,
    text="Task Name:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

# Create a text box where the user can enter a task name.
name_entry = tk.Entry(
    input_frame,
    width=30
)

# Place the task name text box beside its label.
name_entry.grid(
    row=0,
    column=1,
    padx=5
)

# Add a small instruction showing the user what to enter.
tk.Label(
    input_frame,
    text="(At least 3 characters)"
).grid(
    row=0,
    column=2,
    padx=5
)
# PRIORITY

# Create a label for the priority selection.
tk.Label(
    input_frame,
    text="Priority:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


# Create a StringVar to store the selected priority.
# The default priority is Medium.
priority_var = tk.StringVar(value="Medium")


# Create a dropdown menu containing the three priority options.
tk.OptionMenu(
    input_frame,
    priority_var,
    "High",
    "Medium",
    "Low"

# Place the dropdown menu beside the priority label.
).grid(
    row=1,
    column=1
)

# DUE DATE

# Create a label for the due date input.
tk.Label(
    input_frame,
    text="Due Date:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

# Create a text box where the user enters the due date.
date_entry = tk.Entry(
    input_frame,
    width=30
)

# Place the date input box beside its label.
date_entry.grid(
    row=2,
    column=1,
    padx=5
)

# Tell the user which date format to use.
tk.Label(
    input_frame,
    text="(DD/MM/YYYY)"
).grid(
    row=2,
    column=2,
    padx=5
)
# TASK LIST

# Create a label above the task list.
tk.Label(
    window,
    text="Your Tasks",
    font=("Arial", 14, "bold")
).pack(pady=(5, 0))

# Create a Listbox to display all of the tasks.
task_list = tk.Listbox(
    window,

    # Set the width of the Listbox.
    width=100,

    # Set the number of visible rows.
    height=12
)

# Place the Listbox in the main window.
task_list.pack(pady=15)

# BUTTONS

# Create a label above the buttons.
tk.Label(
    window,
    text="Task Actions",
    font=("Arial", 14, "bold")
).pack(pady=(0, 5))

# Create a frame to hold all of the buttons.
button_frame = tk.Frame(window)

# Place the button frame inside the main window.
button_frame.pack()


# Create the TaskManager object.
# This also loads any previously saved tasks.
task_manager = TaskManager()


# ADD TASK BUTTON

# Create the Add Task button.
tk.Button(
    button_frame,
    text="Add Task",
    width=15,
    command=task_manager.add_task
).grid(
    row=0,
    column=0,
    padx=8,
    pady=5
)


# REFRESH BUTTON

# Create the Refresh button.
tk.Button(
    button_frame,
    text="Refresh",
    width=15,
    command=task_manager.view_tasks
).grid(
    row=0,
    column=1,
    padx=8,
    pady=5
)


# COMPLETE BUTTON

# Create the Complete button.
tk.Button(
    button_frame,
    text="Complete",
    width=15,
    command=task_manager.complete_task
).grid(
    row=0,
    column=2,
    padx=8,
    pady=5
)


# DELETE BUTTON

# Create the Delete button.
tk.Button(
    button_frame,
    text="Delete",
    width=15,
    command=task_manager.delete_task
).grid(
    row=0,
    column=3,
    padx=8,
    pady=5
)
# ADD TASK BUTTON

# Create the Add Task button.
tk.Button(
    button_frame,

    # Text displayed on the button.
    text="Add Task",

    # Set the width of the button.
    width=15,

    # Run task_manager.add_task() when clicked.
    command=task_manager.add_task

# Put the button in row 0, column 0.
).grid(
    row=0,
    column=0,
    padx=5
)


# REFRESH BUTTON

# Create the Refresh button.
tk.Button(
    button_frame,
    text="Refresh",
    width=15,

    # Run view_tasks() when the button is clicked.
    command=task_manager.view_tasks

# Put the button in row 0, column 1.
).grid(
    row=0,
    column=1,
    padx=5
)


# COMPLETE BUTTON

# Create the Complete button.
tk.Button(
    button_frame,
    text="Complete",
    width=15,

    # Run complete_task() when the button is clicked.
    command=task_manager.complete_task

# Put the button in row 0, column 2.
).grid(
    row=0,
    column=2,
    padx=5
)


# DELETE BUTTON

# Create the Delete button.
tk.Button(
    button_frame,
    text="Delete",
    width=15,

    # Run delete_task() when the button is clicked.
    command=task_manager.delete_task

# Put the button in row 0, column 3.
).grid(
    row=0,
    column=3,
    padx=5
)


# DISPLAY SAVED TASKS

# Display any tasks that were loaded from tasks.txt.
task_manager.view_tasks()

# RUN PROGRAM

# Start Tkinter's event loop.
# This keeps the GUI open and waits for user actions.
window.mainloop()