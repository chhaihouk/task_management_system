# TASK MANAGEMENT SYSTEM - VERSION 2
# Import tkinter so we can create the graphical user interface (GUI).
import tkinter as tk

# Import messagebox so the program can show pop-up messages and errors.
from tkinter import messagebox

# Import datetime so we can check whether the user entered a valid date.
from datetime import datetime

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

        # VALIDATE TASK NAME
        # Check if the user left the task name empty.
        if name == "":

            # Display an error message if no task name was entered.
            messagebox.showerror(
                "Error",
                "Task name cannot be empty."
            )

            # Stop the function so the invalid task is not added.
            return

        # VALIDATE PRIORITY


        # Check whether the selected priority is valid.
        if priority not in ["High", "Medium", "Low"]:

            # Display an error message if the priority is invalid.
            messagebox.showerror(
                "Error",
                "Please select a valid priority."
            )

            # Stop the function.
            return

        # VALIDATE DATE

        # Try to convert the entered date into a real date.
        try:

            # Check that the date follows the DD/MM/YYYY format.
            datetime.strptime(due_date, "%d/%m/%Y")

        # If the date cannot be converted, ValueError is produced.
        except ValueError:

            # Tell the user that the date format is incorrect.
            messagebox.showerror(
                "Error",
                "Enter the date as DD/MM/YYYY."
            )

            # Stop the function so an invalid date is not saved.
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

    # This function displays all tasks in the Listbox.
    def view_tasks(self):

        # Remove everything currently displayed in the task list.
        task_list.delete(0, tk.END)


        # Check whether there are no tasks.
        if not self.tasks:

            # Display a message telling the user there are no tasks.
            task_list.insert(
                tk.END,
                "No tasks available."
            )

            # Stop the function.
            return


        # Loop through every task in the task list.
        # enumerate() gives each task a number starting from 1.
        for number, task in enumerate(self.tasks, 1):

            # Decide which status text should be displayed.
            # If completed is True, show "Completed".
            # Otherwise show "Not Completed".
            status = "Completed" if task.completed else "Not Completed"


            # Add the task information to the Listbox.
            task_list.insert(
                tk.END,

                # Display the task number and name.
                f"{number}. {task.name} | "

                # Display the task priority.
                f"Priority: {task.priority} | "

                # Display the task due date.
                f"Due: {task.due_date} | "

                # Display whether the task is completed.
                f"Status: {status}"
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

    # This function deletes a selected task.
    def delete_task(self):

        # Find which task the user has selected.
        selected = task_list.curselection()


        # Check whether no task has been selected.
        if not selected:

            # Display an error message.
            messagebox.showerror(
                "Error",
                "Please select a task."
            )

            # Stop the function.
            return


        # Get the Task object that the user selected.
        task = self.tasks[selected[0]]


        # Ask the user to confirm before deleting the task.
        if messagebox.askyesno(
            "Delete Task",
            f"Delete '{task.name}'?"
        ):

            # Remove the selected task from the task list.
            self.tasks.pop(selected[0])

            # Save the updated task list.
            self.save_tasks()

            # Refresh the Listbox so the deleted task disappears.
            self.view_tasks()


    # SAVE TASKS

    # This function saves all tasks to a text file.
    def save_tasks(self):

        # Open the tasks.txt file in write mode.
        # "w" replaces the old file contents with the updated tasks.
        with open("tasks.txt", "w") as file:


            # Loop through every Task object in the list.
            for task in self.tasks:

                # Convert True/False into 1/0.
                # 1 means completed and 0 means not completed.
                completed = "1" if task.completed else "0"


                # Write the task information into the file.
                # The | symbol separates each piece of information.
                file.write(
                    f"{task.name}|"
                    f"{task.priority}|"
                    f"{task.due_date}|"
                    f"{completed}\n"
                )

    # LOAD TASKS

    # This function loads previously saved tasks from the text file.
    def load_tasks(self):

        # Try to open the saved task file.
        try:

            # Open tasks.txt in read mode.
            # "r" means the program can read information from the file.
            with open("tasks.txt", "r") as file:


                # Read the file one line at a time.
                for line in file:

                    # Remove extra spaces/newlines and split the line
                    # into separate pieces using the | symbol.
                    parts = line.strip().split("|")


                    # Check that the line contains exactly four pieces.
                    if len(parts) == 4:

                        # Store each piece of information in a variable.
                        name, priority, due_date, completed = parts


                        # Create a Task object using the saved information.
                        self.tasks.append(
                            Task(
                                name,
                                priority,
                                due_date,

                                # Convert "1" back to True.
                                # Anything else becomes False.
                                completed == "1"
                            )
                        )


        # If tasks.txt does not exist yet, FileNotFoundError occurs.
        except FileNotFoundError:

            # Do nothing because there are no saved tasks yet.
            pass

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
    column=1
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
    column=1
)

# TASK LIST

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