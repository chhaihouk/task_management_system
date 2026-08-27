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
    # Create the GUI.
    def create_widgets(self):
        title = tk.Label(self.window,text="TASK MANAGEMENT SYSTEM",font=("Arial", 24, "bold"),bg="#0F172A",fg="#38BDF8") #Create the main title
        title.pack(pady=(15, 5)) #Place the title
        subtitle = tk.Label(self.window,text="Plan, organise and track your tasks",font=("Arial", 11),bg="#0F172A",fg="#CBD5E1") #Create the subtitle
        subtitle.pack(pady=(0, 15)) #Place the subtitle
        input_frame = tk.LabelFrame(self.window,text="Task Information",font=("Arial", 11, "bold"),padx=15,pady=10,bg="#1E293B",fg="#38BDF8") #Create task information frame
        input_frame.pack(fill="x",padx=20,pady=5) #Place task information frame
        tk.Label(input_frame,text="Task Name:",font=("Arial", 10, "bold"),bg="#1E293B",fg="#F8FAFC").grid(row=0,column=0,padx=5,pady=8,sticky="w") #Create task name label
        self.name_entry = tk.Entry(input_frame,width=35,font=("Arial", 10),bg="#F8FAFC",fg="#0F172A",insertbackground="#0F172A",relief="flat") #Create task name entry
        self.name_entry.grid(row=0,column=1,padx=5,pady=8) #Place task name entry
        tk.Label(input_frame,text="Priority:",font=("Arial", 10, "bold"),bg="#1E293B",fg="#F8FAFC").grid(row=0,column=2,padx=5,pady=8) #Create priority label
        self.priority_var = tk.StringVar(value="Medium") #Create priority variable
        self.priority_menu = ttk.Combobox(input_frame,textvariable=self.priority_var,values=["High", "Medium", "Low"],state="readonly",width=15) #Create priority dropdown
        self.priority_menu.grid(row=0,column=3,padx=5,pady=8) #Place priority dropdown
        tk.Label(input_frame,text="Due Date:",font=("Arial", 10, "bold"),bg="#1E293B",fg="#F8FAFC").grid(row=1,column=0,padx=5,pady=8,sticky="w") #Create due date label
        # DateEntry provides a calendar for easier date selection.
        self.date_entry = DateEntry(input_frame,width=32,date_pattern="dd/mm/yyyy",font=("Arial", 10),background="#2563EB",foreground="white",borderwidth=1) #Create the date picker
        self.date_entry.grid(row=1,column=1,padx=5,pady=8) #Place the date picker
        tk.Label(input_frame,text="Use the calendar",font=("Arial", 9),bg="#1E293B",fg="#94A3B8").grid(row=1,column=2,padx=5,pady=8) #Create date instructions
        button_frame = tk.Frame(self.window,bg="#0F172A") #Create button frame
        button_frame.pack(pady=12) #Place button frame
        tk.Button(button_frame,text="Add Task",width=14,command=self.add_task,bg="#2563EB",fg="white",activebackground="#1D4ED8",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").grid(row=0,column=0,padx=5) #Create Add Task button
        tk.Button(button_frame,text="Edit Task",width=14,command=self.edit_task,bg="#0EA5E9",fg="white",activebackground="#0284C7",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").grid(row=0,column=1,padx=5) #Create Edit Task button
        tk.Button(button_frame,text="Complete",width=14,command=self.complete_task,bg="#10B981",fg="white",activebackground="#059669",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").grid(row=0,column=2,padx=5) #Create Complete button
        tk.Button(button_frame,text="Delete",width=14,command=self.delete_task,bg="#EF4444",fg="white",activebackground="#DC2626",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").grid(row=0,column=3,padx=5) #Create Delete button
        tk.Button(button_frame,text="Clear Fields",width=14,command=self.clear_fields,bg="#475569",fg="white",activebackground="#334155",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").grid(row=0,column=4,padx=5) #Create Clear button
        filter_frame = tk.LabelFrame(self.window,text="Search and Filter",font=("Arial", 11, "bold"),padx=10,pady=8,bg="#1E293B",fg="#38BDF8") #Create filter frame
        filter_frame.pack(fill="x",padx=20,pady=5) #Place filter frame
        tk.Label(filter_frame,text="Search:",bg="#1E293B",fg="#F8FAFC").grid(row=0,column=0,padx=5) #Create search label
        self.search_var = tk.StringVar() #Create search variable
        self.search_entry = tk.Entry(filter_frame,textvariable=self.search_var,width=25,bg="#F8FAFC",fg="#0F172A",insertbackground="#0F172A",relief="flat") #Create search entry
        self.search_entry.grid(row=0,column=1,padx=5) #Place search entry
        tk.Label(filter_frame,text="Priority:",bg="#1E293B",fg="#F8FAFC").grid(row=0,column=2,padx=5) #Create priority filter label
        self.filter_priority_var = tk.StringVar(value="All") #Create priority filter variable
        self.filter_priority = ttk.Combobox(filter_frame,textvariable=self.filter_priority_var,values=["All", "High", "Medium", "Low"],state="readonly",width=12) #Create priority filter
        self.filter_priority.grid(row=0,column=3,padx=5) #Place priority filter
        tk.Label(filter_frame,text="Status:",bg="#1E293B",fg="#F8FAFC").grid(row=0,column=4,padx=5) #Create status label
        self.filter_status_var = tk.StringVar(value="All") #Create status variable
        self.filter_status = ttk.Combobox(filter_frame,textvariable=self.filter_status_var,values=["All","Completed","Not Completed"],state="readonly",width=15) #Create status filter
        self.filter_status.grid(row=0,column=5,padx=5) #Place status filter
        tk.Label(filter_frame,text="Sort:",bg="#1E293B",fg="#F8FAFC").grid(row=0,column=6,padx=5) #Create sort label
        self.sort_var = tk.StringVar(value="Default") #Create sort variable
        self.sort_menu = ttk.Combobox(filter_frame,textvariable=self.sort_var,values=["Default","Priority","Due Date","Task Name"],state="readonly",width=15) #Create sort dropdown
        self.sort_menu.grid(row=0,column=7,padx=5) #Place sort dropdown
        tk.Button(filter_frame,text="Apply",width=10,command=self.refresh_tasks,bg="#2563EB",fg="white",activebackground="#1D4ED8",relief="flat",font=("Arial", 9, "bold"),cursor="hand2").grid(row=0,column=8,padx=5) #Create Apply button
        tk.Button(filter_frame,text="Clear",width=10,command=self.clear_filters,bg="#475569",fg="white",activebackground="#334155",relief="flat",font=("Arial", 9, "bold"),cursor="hand2").grid(row=0,column=9,padx=5) #Create Clear button
        table_frame = tk.Frame(self.window,bg="#0F172A") #Create table frame
        table_frame.pack(fill="both",expand=True,padx=20,pady=10) #Place table frame
        self.task_table = ttk.Treeview(table_frame,columns=("number","name","priority","due_date","status"),show="headings",selectmode="browse") #Create task table
        self.task_table.heading("number",text="#") #Set number heading
        self.task_table.heading("name",text="Task Name") #Set name heading
        self.task_table.heading("priority",text="Priority") #Set priority heading
        self.task_table.heading("due_date",text="Due Date") #Set date heading
        self.task_table.heading("status",text="Status") #Set status heading
        self.task_table.column("number",width=50,anchor="center") #Set number width
        self.task_table.column("name",width=350) #Set name width
        self.task_table.column("priority",width=120,anchor="center") #Set priority width
        self.task_table.column("due_date",width=130,anchor="center") #Set date width
        self.task_table.column("status",width=150,anchor="center") #Set status width
        self.task_table.tag_configure("even",background="#1E293B",foreground="#F8FAFC") #Set even row colour
        self.task_table.tag_configure("odd",background="#243247",foreground="#F8FAFC") #Set odd row colour
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical",command=self.task_table.yview) #Create scrollbar
        self.task_table.configure(yscrollcommand=scrollbar.set) #Connect scrollbar to table
        self.task_table.pack(side="left",fill="both",expand=True) #Place table
        scrollbar.pack(side="right",fill="y") #Place scrollbar
        self.task_table.bind("<Double-1>",self.edit_task) #Allow double-click editing
        self.task_count_label = tk.Label(self.window,text="Tasks: 0",font=("Arial", 10, "bold"),bg="#0F172A",fg="#94A3B8") #Create task counter
        self.task_count_label.pack(pady=(0, 10)) #Place task counter
    # GET SELECTED TASK
    def get_selected_index(self):
        selected = self.task_table.selection() #Get selected row
        if not selected: #Check if a row was selected
            return -1
        values = self.task_table.item(selected[0],"values") #Get row information
        if not values: #Check if row has information
            return -1
        task_name = values[1] #Get task name
        priority = values[2] #Get priority
        due_date = values[3] #Get due date
        for index, task in enumerate(self.manager.tasks):
            if (
                task.name == task_name
                and task.priority == priority
                and task.due_date == due_date
            ): #Find matching task
                return index
        return -1 #Return -1 if no task was found
    # ADD TASK
    def add_task(self):
        name = self.name_entry.get().strip() #Get task name
        priority = self.priority_var.get() #Get priority
        due_date = self.date_entry.get() #Get selected date
        success, message = self.manager.add_task(name,priority,due_date) #Add the task
        if success:
            self.clear_fields() #Clear input fields
            self.refresh_tasks() #Refresh the table
            messagebox.showinfo("Success",message) #Show success message
        else:
            messagebox.showerror("Invalid Task",message) #Show validation error
    # EDIT TASK
    def edit_task(self, event=None):
        index = self.get_selected_index() #Get selected task
        if index == -1:
            messagebox.showerror("Error","Please select a task to edit.") #Show error
            return #Stop the function
        task = self.manager.tasks[index] #Get selected task
        self.name_entry.delete(0,tk.END) #Clear task name
        self.name_entry.insert(0,task.name) #Insert existing task name
        self.priority_var.set(task.priority) #Set existing priority
        self.date_entry.set_date(datetime.strptime(task.due_date,"%d/%m/%Y")) #Set existing date
        edit_window = tk.Toplevel(self.window) #Create edit popup
        edit_window.title("Edit Task") #Set popup title
        edit_window.geometry("350x180") #Set popup size
        edit_window.resizable(False,False) #Prevent resizing
        edit_window.configure(bg="#0F172A") #Set popup colour
        tk.Label(edit_window,text="Edit the task using the fields above.",font=("Arial", 10),bg="#0F172A",fg="#F8FAFC").pack(pady=20) #Create popup message
        tk.Button(edit_window,text="Save Changes",width=15,command=lambda: self.save_edit(index,edit_window),bg="#10B981",fg="white",activebackground="#059669",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").pack(pady=5) #Create save button
        tk.Button(edit_window,text="Cancel",width=15,command=edit_window.destroy,bg="#475569",fg="white",activebackground="#334155",relief="flat",font=("Arial", 10, "bold"),cursor="hand2").pack(pady=5) #Create cancel button
    # SAVE EDIT
    def save_edit(self, index, edit_window):
        name = self.name_entry.get().strip() #Get updated name
        priority = self.priority_var.get() #Get updated priority
        due_date = self.date_entry.get() #Get updated date
        success, message = self.manager.edit_task(index,name,priority,due_date) #Save the changes
        if success:
            edit_window.destroy() #Close popup
            self.clear_fields() #Clear fields
            self.refresh_tasks() #Refresh task table
            messagebox.showinfo("Success",message) #Show success message
        else:
            messagebox.showerror("Invalid Task",message) #Show validation error
    # COMPLETE TASK
    def complete_task(self):
        index = self.get_selected_index() #Get selected task
        if index == -1:
            messagebox.showerror("Error","Please select a task to complete.") #Show error
            return #Stop the function
        success, message = self.manager.complete_task(index) #Complete the task
        if success:
            self.refresh_tasks() #Refresh the table
            messagebox.showinfo("Success",message) #Show success message
        else:
            messagebox.showinfo("Information",message) #Show information message
    # DELETE TASK
    def delete_task(self):
        index = self.get_selected_index() #Get selected task
        if index == -1:
            messagebox.showerror("Error","Please select a task to delete.") #Show error
            return #Stop the function
        task_name = self.manager.tasks[index].name #Get task name
        confirm = messagebox.askyesno("Delete Task",f"Are you sure you want to delete '{task_name}'?") #Ask for deletion confirmation
        if confirm:
            success, message = self.manager.delete_task(index) #Delete the task
            if success:
                self.clear_fields() #Clear input fields
                self.refresh_tasks() #Refresh the table
                messagebox.showinfo("Success",message) #Show success message
    # REFRESH TASKS
    def refresh_tasks(self):
        search_text = self.search_var.get().strip().lower() #Get search text
        priority_filter = self.filter_priority_var.get() #Get priority filter
        status_filter = self.filter_status_var.get() #Get status filter
        filtered_tasks = list(self.manager.tasks) #Start with all tasks
        if search_text:
            filtered_tasks = [
                task
                for task in filtered_tasks
                if search_text in task.name.lower()
            ] #Filter by search text
        if priority_filter != "All":
            filtered_tasks = [
                task
                for task in filtered_tasks
                if task.priority == priority_filter
            ] #Filter by priority
        if status_filter == "Completed":
            filtered_tasks = [
                task
                for task in filtered_tasks
                if task.completed
            ] #Show completed tasks
        elif status_filter == "Not Completed":
            filtered_tasks = [
                task
                for task in filtered_tasks
                if not task.completed
            ] #Show incomplete tasks
        filtered_tasks = self.sort_tasks(filtered_tasks) #Sort filtered tasks
        self.displayed_tasks = filtered_tasks #Store displayed tasks
        for item in self.task_table.get_children():
            self.task_table.delete(item) #Remove old rows
        for number, task in enumerate(filtered_tasks,1):
            status = ("Completed"if task.completed else "Not Completed") #Set task status
            row_tag = ("even"if number % 2 == 0 else "odd") #Choose alternating row colour
            self.task_table.insert("",tk.END,values=(number,task.name,task.priority,task.due_date,status),tags=(row_tag,)) #Add task to table
        self.task_count_label.config(text=(f"Showing {len(filtered_tasks)} "f"of {len(self.manager.tasks)} tasks")) #Update task counter
    # SORT TASKS
    def sort_tasks(self, tasks):
        sort_option = self.sort_var.get() #Get selected sort option
        if sort_option == "Task Name":
            return sorted(tasks,key=lambda task: task.name.lower()) #Sort alphabetically
        if sort_option == "Priority":
            priority_order = {"High": 1,"Medium": 2,"Low": 3} #Create priority order
            return sorted(tasks,key=lambda task:priority_order.get(task.priority,4)) #Sort by priority
        if sort_option == "Due Date":
            return sorted(tasks,key=lambda task:datetime.strptime(task.due_date,"%d/%m/%Y")) #Sort by due date
        return tasks #Keep original order
    # CLEAR FIELDS
    def clear_fields(self):
        self.name_entry.delete(0, tk.END) #Remove the task name
        self.priority_var.set("Medium") #Reset the priority
        self.date_entry.set_date(date.today()) #Reset the date picker
        self.name_entry.focus() #Put the cursor back into the task name field
    # CLEAR FILTERS
    def clear_filters(self):
        self.search_var.set("") #Clear the search box
        self.filter_priority_var.set("All") #Reset the priority filter
        self.filter_status_var.set("All") #Reset the status filter
        self.sort_var.set("Default") #Reset the sorting option
        self.refresh_tasks() #Display all tasks again