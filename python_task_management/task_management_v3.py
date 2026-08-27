# TASK MANAGEMENT SYSTEM - VERSION 3
import tkinter as tk #Import tkinter to create the main graphical user interface (GUI)
from tkinter import ttk, messagebox #Import ttk for improved Tkinter widgets and messagebox for pop-up messages
from datetime import datetime, date #Import datetime and date to validate and work with task due dates
import hashlib #Import hashlib to securely hash the user's password before storing it
import os #Import os to check whether files exist and handle file operations
from tkcalendar import DateEntry #Import DateEntry to provide a calendar date picker for selecting due dates