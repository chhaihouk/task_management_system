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