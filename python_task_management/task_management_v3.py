# TASK MANAGEMENT SYSTEM - VERSION 3
import tkinter as tk #Import tkinter to create the main graphical user interface (GUI)
from tkinter import ttk, messagebox #Import ttk for improved Tkinter widgets and messagebox for pop-up messages
from datetime import datetime, date #Import datetime and date to validate and work with task due dates
import hashlib #Import hashlib to securely hash the user's password before storing it
import os #Import os to check whether files exist and handle file operations
from tkcalendar import DateEntry #Import DateEntry to provide a calendar date picker for selecting due dates
# TASK CLASS
class Task:
    def __init__(self, name, priority, due_date, completed=False):
        self.name = name #Store the task name
        self.priority = priority #Store the task priority
        self.due_date = due_date #Store the task due date
        self.completed = completed #Store whether the task is completed
# TASK MANAGER CLASS
class TaskManager:
    def __init__(self):
        self.tasks = [] #Create an empty list for tasks
        self.load_tasks() #Load saved tasks
    # Validate the task name.
    def validate_name(self, name):
        if name == "": #Check if the name is empty
            return False, "Task name cannot be empty."
        if len(name) < 3: #Check if the name is too short
            return False, "Task name must be at least 3 characters long."
        return True, "" #Return valid
    # Validate the task priority.
    def validate_priority(self, priority):
        valid_priorities = ["High", "Medium", "Low"] #Create valid priorities
        if priority not in valid_priorities: #Check if priority is valid
            return False, "Please select High, Medium, or Low priority."
        return True, "" #Return valid
    # Validate the task date.
    def validate_date(self, due_date):
        try:
            entered_date = datetime.strptime(due_date,"%d/%m/%Y").date() #Convert the date into a date object
        except ValueError:
            return False, "Please select a valid date."
        if entered_date < date.today(): #Check if the date is in the past
            return False, "The due date cannot be in the past."
        return True, "" #Return valid
    # Validate all task information.
    def validate_task(self, name, priority, due_date):
        valid, message = self.validate_name(name) #Validate the name
        if not valid:
            return False, message
        valid, message = self.validate_priority(priority) #Validate priority
        if not valid:
            return False, message
        valid, message = self.validate_date(due_date) #Validate date
        if not valid:
            return False, message
        return True, "" #Return valid
    # Add a new task.
    def add_task(self, name, priority, due_date):
        valid, message = self.validate_task(name,priority,due_date) #Validate task information
        if not valid:
            return False, message
        new_task = Task(name,priority,due_date) #Create a new task
        self.tasks.append(new_task) #Add task to the list
        self.save_tasks() #Save the updated tasks
        return True, "Task added successfully."
    # Edit an existing task.
    def edit_task(self, index, name, priority, due_date):
        if index < 0 or index >= len(self.tasks): #Check the selected index
            return False, "Please select a valid task."
        valid, message = self.validate_task(name,priority,due_date) #Validate the new information
        if not valid:
            return False, message
        task = self.tasks[index] #Get the selected task
        task.name = name #Update the task name
        task.priority = priority #Update the priority
        task.due_date = due_date #Update the due date
        self.save_tasks() #Save the changes
        return True, "Task updated successfully."
    # Complete a task.
    def complete_task(self, index):
        if index < 0 or index >= len(self.tasks): #Check the selected index
            return False, "Please select a task."
        task = self.tasks[index] #Get the selected task
        if task.completed: #Check if it is already completed
            return False, "This task is already completed."
        task.completed = True #Mark the task as completed
        self.save_tasks() #Save the changes
        return True, "Task marked as completed."
    # Delete a task.
    def delete_task(self, index):
        if index < 0 or index >= len(self.tasks): #Check the selected index
            return False, "Please select a task."
        self.tasks.pop(index) #Remove the selected task
        self.save_tasks() #Save the changes
        return True, "Task deleted successfully."
    # Save all tasks.
    def save_tasks(self):
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks:
                    completed = "1" if task.completed else "0" #Convert status to 1 or 0
                    file.write(
                        f"{task.name}|"
                        f"{task.priority}|"
                        f"{task.due_date}|"
                        f"{completed}\n"
                    ) #Write task information
            return True
        except OSError:
            return False
    # Load saved tasks.
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    line = line.strip() #Remove extra whitespace
                    if not line: #Skip empty lines
                        continue
                    parts = line.split("|") #Split saved information
                    if len(parts) != 4: #Check the correct number of values
                        continue
                    name, priority, due_date, completed = parts
                    if priority not in ["High", "Medium", "Low"]: #Check priority
                        continue
                    if completed not in ["0", "1"]: #Check completion value
                        continue
                    if name.strip() == "": #Check task name
                        continue
                    self.tasks.append(
                        Task(
                            name,
                            priority,
                            due_date,
                            completed == "1"
                        )
                    ) #Create and store the saved task
        except FileNotFoundError:
            pass #Start with no tasks if the file does not exist
        except OSError:
            pass #Continue if the file cannot be opened
# LOGIN SYSTEM
class LoginWindow:
    def __init__(self, window):
        self.window = window #Store the login window
        self.logged_in = False #Track whether login succeeds
        self.window.title("Task Management System - Login") #Set window title
        self.window.geometry("430x330") #Set window size
        self.window.resizable(False, False) #Prevent resizing
        self.window.configure(bg="#0F172A") #Set background colour
        self.create_login_widgets() #Create login widgets
    # Create the login screen.
    def create_login_widgets(self):
        title = tk.Label(self.window,text="TASK MANAGEMENT SYSTEM",font=("Arial", 20, "bold"),bg="#0F172A",fg="#38BDF8") #Create the title
        title.pack(pady=(35, 5)) #Place the title
        subtitle = tk.Label(self.window,text="Private Task Manager",font=("Arial", 11),bg="#0F172A",fg="#CBD5E1") #Create the subtitle
        subtitle.pack(pady=(0, 20)) #Place the subtitle
        login_frame = tk.Frame(self.window,bg="#1E293B",padx=25,pady=20) #Create the login frame
        login_frame.pack(padx=30,fill="x") #Place the login frame
        tk.Label(login_frame,text="Password:",font=("Arial", 10, "bold"),bg="#1E293B",fg="#F8FAFC").pack(pady=(0, 5)) #Create password label
        self.password_entry = tk.Entry(login_frame,show="*",width=30,font=("Arial", 11),bg="#F8FAFC",fg="#0F172A",insertbackground="#0F172A",relief="flat") #Create password entry
        self.password_entry.pack(pady=5) #Place password entry
        self.status_label = tk.Label(login_frame,text="",font=("Arial", 9),bg="#1E293B",fg="#EF4444") #Create login status label
        self.status_label.pack(pady=5) #Place status label
        tk.Button(login_frame,text="Login",width=18,command=self.login,bg="#2563EB",fg="white",activebackground="#1D4ED8",activeforeground="white",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").pack(pady=5) #Create login button
        tk.Button(login_frame,text="Set / Change Password",width=18,command=self.set_password,bg="#475569",fg="white",activebackground="#334155",activeforeground="white",relief="flat",font=("Arial", 9, "bold"),cursor="hand2").pack(pady=5) #Create password setup button
        self.password_entry.focus() #Put the cursor into the password box
        self.window.bind("<Return>",lambda event: self.login()) #Allow Enter to login
    # Hash the password for safer storage.
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() #Return the password hash
        # Set or change the password.
    def set_password(self):
        password_window = tk.Toplevel(self.window) #Create password setup window
        password_window.title("Set Password") #Set popup title
        password_window.geometry("350x220") #Set popup size
        password_window.resizable(False, False) #Prevent resizing
        password_window.configure(bg="#0F172A") #Set popup colour
        tk.Label(password_window,text="Create a Password",font=("Arial", 15, "bold"),bg="#0F172A",fg="#38BDF8").pack(pady=15) #Create popup title
        tk.Label(password_window,text="Enter a password with at least 4 characters.",font=("Arial", 9),bg="#0F172A",fg="#CBD5E1").pack(pady=5) #Create password instructions
        new_password = tk.Entry(password_window,show="*",width=25,bg="#F8FAFC",fg="#0F172A",relief="flat") #Create new password entry
        new_password.pack(pady=8) #Place password entry
        confirm_password = tk.Entry(password_window,show="*",width=25,bg="#F8FAFC",fg="#0F172A",relief="flat") #Create confirmation entry
        confirm_password.pack(pady=8) #Place confirmation entry
        def save_password():
            password = new_password.get() #Get new password
            confirmation = confirm_password.get() #Get confirmation
            if len(password) < 4: #Check password length
                messagebox.showerror("Invalid Password","Password must be at least 4 characters long.")
                return
            if password != confirmation: #Check passwords match
                messagebox.showerror("Password Error","The passwords do not match.")
                return
            try:
                with open("password.txt", "w") as file:
                    file.write(self.hash_password(password)) #Save the password hash
                messagebox.showinfo("Success","Password saved successfully.") #Tell the user the password was saved
                password_window.destroy() #Close setup window
            except OSError:
                messagebox.showerror("Error","Unable to save the password.") #Tell the user the password could not be saved
        tk.Button(password_window,text="Save Password",width=15,command=save_password,bg="#10B981",fg="white",activebackground="#059669",relief="flat",font=("Arial", 9, "bold"),cursor="hand2").pack(pady=10) #Create save password button
    # Check the entered password.
    def login(self):
        password = self.password_entry.get() #Get entered password
        if not os.path.exists("password.txt"): #Check if a password exists
            self.status_label.config(text="Please set a password first.") #Tell the user to set a password
            return
        try:
            with open("password.txt", "r") as file:
                saved_password = file.read().strip() #Read saved hash
        except OSError:
            self.status_label.config(text="Unable to access password file.")
            return
        entered_password = self.hash_password(password) #Hash the entered password
        if entered_password == saved_password: #Compare password hashes
            self.logged_in = True #Allow access
            self.window.destroy() #Close login window
        else:
            self.status_label.config(text="Incorrect password.") #Display login error
# MAIN APPLICATION CLASS
class TaskManagementApp:
    def __init__(self, window):
        self.window = window #Store the main window
        self.manager = TaskManager() #Create the task manager
        self.displayed_tasks = [] #Store currently displayed tasks
        self.setup_window() #Set up the window
        self.create_widgets() #Create GUI widgets
        self.refresh_tasks() #Display tasks
        self.name_entry.focus() #Focus the task name field
    # Configure the main window.
    def setup_window(self):
        self.window.title("Task Management System - Version 3") #Set the window title
        self.window.geometry("1050x700") #Set the starting window size
        self.window.minsize(900,600) #Set the minimum window size
        self.window.resizable(True,True) #Allow resizing
        self.window.configure(bg="#0F172A") #Set the background colour
        style = ttk.Style() #Create a ttk style
        style.theme_use("clam") #Use the Clam theme
        style.configure("Treeview",background="#1E293B",foreground="#F8FAFC",fieldbackground="#1E293B",rowheight=32,font=("Arial", 10)) #Style the task table
        style.configure("Treeview.Heading",background="#2563EB",foreground="white",font=("Arial", 10, "bold")) #Style table headings
        style.map("Treeview",background=[("selected", "#0EA5E9")],foreground=[("selected", "white")]) #Style selected rows
        style.configure("TCombobox",fieldbackground="#F8FAFC",background="#F8FAFC",foreground="#0F172A",padding=5) #Style dropdown menus
        style.configure("Vertical.TScrollbar",background="#334155",troughcolor="#0F172A",arrowcolor="white") #Style scrollbar