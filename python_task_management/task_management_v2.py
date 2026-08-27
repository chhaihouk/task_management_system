#TASK MANAGEMENT SYSTEM - VERSION 2
import tkinter as tk #Import tkinter so we can create the graphical user interface (GUI)
from tkinter import messagebox #Import messagebox so the program can show pop-up messages and errors
from datetime import datetime #Import datetime so we can check whether the user entered a valid date
from unicodedata import name
#TASK CLASS
class Task: #Create a class called Task to represent one individual task
    def __init__(self, name, priority, due_date, completed=False): #This function runs whenever a new Task object is created
        self.name = name #Store the task name inside the Task object
        self.priority = priority #Store the priority of the task inside the Task object
        self.due_date = due_date #Store the due date of the task inside the Task object
        self.completed = completed #Store whether the task is completed #New tasks are not completed by default
#TASK MANAGER CLASS
#Create a class called TaskManager.
class TaskManager: #This class controls the tasks and the main task functions
    def __init__(self): #This function runs when the TaskManager is created
        self.tasks = [] #Create an empty list to store all Task objects
        self.load_tasks() #Load any tasks that were previously saved in the text file
    #ADD TASK
    def add_task(self): #This function adds a new task to the task list
        #Get the task name from the name input box.
        name = name_entry.get().strip() #strip() removes unnecessary spaces from the beginning/end
        priority = priority_var.get() #Get the priority selected by the user
        due_date = date_entry.get().strip() #Get the due date entered by the user
        valid_priorities = ["High", "Medium", "Low"] #Store the priority options allowed by the program
        #Validate task name.
        if name == "":
            messagebox.showerror("Error","Task name cannot be empty.")
            return
        #Check that the task name is long enough.
        if len(name) < 3:
            messagebox.showerror("Error","Task name must be at least 3 characters long.")
            return
        #VALIDATE PRIORITY
        #Check that the selected priority is valid.
        if priority not in valid_priorities:
            messagebox.showerror("Error","Please select High, Medium, or Low priority.")
            return
        #VALIDATE DATE
        #Validate the due date.
        try:
            valid_date = datetime.strptime(due_date, "%d/%m/%Y") #Convert the entered text into a real date
        except ValueError:
            #Tell the user if the date is invalid.
            messagebox.showerror("Error","Please enter a valid date using DD/MM/YYYY.")
            return
        #Check that the due date is not in the past.
        if valid_date < datetime.now():
            messagebox.showerror("Error","The due date cannot be in the past.")
            return
        #CREATE THE TASK
        #Create a new Task object using the information entered.
        self.tasks.append(Task(name, priority, due_date)) #The task is automatically set as not completed
        self.save_tasks() #Save the updated task list to the text file
        name_entry.delete(0, tk.END) #Clear the task name input box
        date_entry.delete(0, tk.END) #Clear the due date input box
        priority_var.set("Medium") #Reset the priority back to Medium
        self.view_tasks() #Refresh the task list so the new task appears
        messagebox.showinfo("Success","Task added successfully!") #Tell the user that the task was successfully added
    #VIEW TASKS
    def view_tasks(self):
        task_list.delete(0, tk.END) #Clear the current task list before displaying it again
        #Check if there are no tasks.
        if not self.tasks:
            task_list.insert(tk.END,"No tasks available.")
            return
        for number, task in enumerate(self.tasks, 1): #Go through each task and give it a number
            #Decide which status should be displayed.
            if task.completed:
                status = "Completed"
            else:
                status = "Not Completed"
            #Create a clear display line for the task.
            task_text = (
                f"{number}. {task.name} | "
                f"Priority: {task.priority} | "
                f"Due: {task.due_date} | "
                f"Status: {status}"
            )
            task_list.insert(tk.END,task_text) #Add the task to the Listbox
     #COMPLETE TASK
    def complete_task(self):
            selected = task_list.curselection() #Get the task selected by the user
            #Check if the user selected a task.
            if not selected:
                messagebox.showerror("Error","Please select a task.")
                return
            task = self.tasks[selected[0]] #Get the selected Task object from the list
            #Check if the task is already completed.
            if task.completed:
                messagebox.showinfo("Information","This task is already completed.")
                return
            task.completed = True #Mark the task as completed
            self.save_tasks() #Save the updated task list
            self.view_tasks() #Refresh the task list
            #Tell the user the task was completed.
            messagebox.showinfo("Success","Task marked as completed!")
    #DELETE TASK
    def delete_task(self):
        selected = task_list.curselection() #Get the task selected by the user
        #Check if the user selected a task.
        if not selected:
            messagebox.showerror("Error","Please select a task to delete.")
            return
        task_index = selected[0] #Store the position of the selected task
        task = self.tasks[task_index] # Get the selected Task object
        confirm = messagebox.askyesno("Delete Task",f"Are you sure you want to delete '{task.name}'?") #Ask the user to confirm the deletion
        #Only delete the task if the user chooses Yes.
        if confirm:
            self.tasks.pop(task_index) #Remove the selected task from the task list
            self.save_tasks() #Save the updated task list
            self.view_tasks() #Refresh the task list
            #Tell the user the task was deleted.
            messagebox.showinfo("Success","Task deleted successfully.")
    #SAVE TASKS
    def save_tasks(self):
        #Try to save all tasks to the text file.
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks: #Go through each task in the task list
                    completed = "1" if task.completed else "0" #Convert the completed status into 1 or 0
                    #Write the task information to the file.
                    file.write(
                        f"{task.name}|"
                        f"{task.priority}|"
                        f"{task.due_date}|"
                        f"{completed}\n"
                    )
        except OSError:
            #Show an error if the file cannot be saved.
            messagebox.showerror("Save Error","The tasks could not be saved.")
    #LOAD TASKS
    def load_tasks(self):
        #Try to open the file containing saved tasks.
        try:
            with open("tasks.txt", "r") as file:
                for line in file: #Read each saved task one line at a time
                    parts = line.strip().split("|") #Remove extra spaces and split the data
                    if len(parts) != 4: #Check that the saved data has four parts
                        continue
                    name, priority, due_date, completed = parts #Store each part of the saved task
                    if priority not in ["High", "Medium", "Low"]: #Check that the saved priority is valid
                        continue
                    if completed not in ["0", "1"]: #Check that the completion value is valid
                        continue
                    self.tasks.append(Task(name,priority,due_date,completed == "1")) #Create the Task object and add it to the list
        except FileNotFoundError:
            #No saved task file exists yet.
            pass
        except OSError:
            messagebox.showerror("Load Error","The saved tasks could not be loaded.") #Tell the user if the task file cannot be opened
#TKINTER GUI
window = tk.Tk() #Create the main Tkinter window
window.title("Task Management System - Version 2") #Set the title shown at the top of the window
window.geometry("850x550") #Set the starting size of the window
window.resizable(True, True) #Allow the window to be resized by the user
window.minsize(700, 500) #Set a minimum size so the GUI does not become too small
#TITLE
#Create a large title label for the program.
tk.Label(
    window,
    text="TASK MANAGEMENT SYSTEM", #Text displayed by the label
    font=("Arial", 20, "bold") #Set the font to Arial, size 20, and bold
).pack(pady=15) #Add the label to the window with 15 pixels of vertical spacing
#INPUT FRAME
input_frame = tk.Frame(window) #Create a frame to hold the input fields
input_frame.pack() #Place the input frame inside the main window
#TASK NAME
tk.Label(input_frame,text="Task Name:").grid(row=0,column=0,padx=5,pady=5) #Create a label telling the user what the first input is for
name_entry = tk.Entry(input_frame,width=30) #Create a text box where the user can enter a task name
name_entry.grid(row=0,column=1,padx=5) #Place the task name text box beside its label
tk.Label(input_frame,text="(At least 3 characters)").grid(row=0,column=2,padx=5) #Add a small instruction showing the user what to enter
#PRIORITY
tk.Label(input_frame,text="Priority:").grid(row=1,column=0,padx=5,pady=5) #Create a label for the priority selection
priority_var = tk.StringVar(value="Medium") #Create a StringVar to store the selected priority #The default priority is Medium
tk.OptionMenu(input_frame,priority_var,"High","Medium","Low").grid(row=1,column=1) #Create a dropdown menu containing the three priority options #Place the dropdown menu beside the priority label
#DUE DATE
tk.Label(input_frame,text="Due Date:").grid(row=2,column=0,padx=5,pady=5) #Create a label for the due date input
date_entry = tk.Entry(input_frame,width=30) #Create a text box where the user enters the due date
date_entry.grid(row=2,column=1,padx=5) #Place the date input box beside its label
tk.Label(input_frame,text="Example: 25/08/2026").grid(row=2,column=2,padx=5) #Show an example of the required date format
tk.Label(input_frame,text="Example: 25/08/2026").grid(row=2,column=2,padx=5) #Tell the user which date format to use
#TASK LIST
tk.Label(window,text="Your Tasks",font=("Arial", 14, "bold")).pack(pady=(5, 0)) #Create a label above the task list
task_list_frame = tk.Frame(window) #Create a frame to hold the task list and scrollbar
task_list_frame.pack(pady=10) #Place the frame inside the main window 
task_list = tk.Listbox(task_list_frame, #Create a Listbox to display all of the tasks
    width=100, #Set the width of the Listbox
    height=14, #Set the number of visible rows
    font=("Arial", 11), #Make the task text easier to read
    selectbackground="lightblue", #Make the selected task easier to see
    selectforeground="black" #Make the selected task text easy to read
)
task_list.pack(side=tk.LEFT) #Place the Listbox on the left side of the frame
task_scrollbar = tk.Scrollbar(task_list_frame,command=task_list.yview) #Create a scrollbar for the task list #Make the scrollbar move the Listbox vertically
task_scrollbar.pack(side=tk.RIGHT,fill=tk.Y) #Place the scrollbar beside the Listbox
task_list.config(yscrollcommand=task_scrollbar.set) #Connect the Listbox to the scrollbar
#BUTTONS
tk.Label(window,text="Task Actions",font=("Arial", 14, "bold")).pack(pady=(0, 5)) #Create a label above the buttons
button_frame = tk.Frame(window) #Create a frame to hold all of the buttons
button_frame.pack() #Place the button frame inside the main window
# Create the TaskManager object.
task_manager = TaskManager() #This also loads any previously saved tasks
#ADD TASK BUTTON
tk.Button(button_frame,text="Add Task",width=15,command=task_manager.add_task).grid(row=0,column=0,padx=8,pady=5) #Create the Add Task button
#REFRESH BUTTON
tk.Button(button_frame,text="Refresh",width=15,command=task_manager.view_tasks).grid(row=0,column=1,padx=8,pady=5) #Create the Refresh button
#COMPLETE BUTTON
tk.Button(button_frame,text="Complete",width=15,command=task_manager.complete_task).grid(row=0,column=2,padx=8,pady=5) #Create the Complete button
#DELETE BUTTON
tk.Button(button_frame,text="Delete",width=15,command=task_manager.delete_task).grid(row=0,column=3,padx=8,pady=5) #Create the Delete button
#DISPLAY SAVED TASKS
task_manager.view_tasks() #Display any tasks that were loaded from tasks.txt
name_entry.focus() #Automatically place the cursor inside the task name input
#RUN PROGRAM
#Start Tkinter's event loop
window.mainloop() #This keeps the GUI open and waits for user actions