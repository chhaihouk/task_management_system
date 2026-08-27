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