# TASK MANAGEMENT SYSTEM - VERSION 1
# TASK CLASS
# This class represents one individual task
class Task:
    def __init__(self, name, priority, due_date): #Store the name of the task
        self.name = name #Store the priority of the task
        self.priority = priority #Store the due date of the task
        self.due_date = due_date #Every new task starts as not completed
        self.completed = False

# TASK MANAGER CLASS
class TaskManager: #This class manages all of the tasks
    def __init__(self):
        self.tasks = [] #Create an empty list to store Task objects
    # ADD TASK
    def add_task(self):
        task_name = input("Enter the task name: ") #Ask the user to enter the task name
        priority = input("Enter priority (High/Medium/Low): ") #Ask the user to enter the priority
        due_date = input("Enter due date (e.g. 15/08/2026): ") #Ask the user to enter the due date
        new_task = Task(task_name, priority, due_date) #Create a new Task object
        self.tasks.append(new_task) #Add the new Task object to the task list
        print("\nTask added successfully!\n") #Tell the user that the task was added
    # VIEW TASKS
    def view_tasks(self):

        if len(self.tasks) == 0: #Check if there are no tasks
            print("\nThere are no tasks to display.\n") #Tell the user there are no tasks
            return #Stop the function

        print("\n========== YOUR TASKS ==========") #Print the heading

        for number, task in enumerate(self.tasks, start=1): #Loop through every task

            if task.completed: #Check whether the task has been completed
                status = "Completed" #Set the status to Completed

            else:
                status = "Not Completed" #Set the status to Not Completed

            print(f"\nTask {number}: {task.name}") #Display the task number and name
            print(f"Priority: {task.priority}") #Display the priority
            print(f"Due Date: {task.due_date}") #Display the due date
            print(f"Status: {status}") #Display the completion status
            print("\n================================\n") #Print a line at the bottom
    # COMPLETE TASK
    def complete_task(self):
        if len(self.tasks) == 0: #Check if there are any tasks
            print("\nThere are no tasks to complete.\n") #Tell the user there are no tasks
            return #Stop the function
        self.view_tasks() #Display the current tasks
        choice = input("Enter the task number to complete: ") #Ask the user which task they want to complete
        if choice.isdigit(): #Check whether the input is a number
            task_number = int(choice) #Convert the input to an integer
            if 1 <= task_number <= len(self.tasks): #Check whether the task number is valid
                selected_task = self.tasks[task_number - 1] #Get the selected Task object
                selected_task.completed = True #Change its completed status to True
                print("\nTask marked as completed!\n") #Tell the user the task was completed
            else:
                print("\nInvalid task number.\n") #Tell the user the number is invalid
        else:
            print("\nPlease enter a valid number.\n") #Tell the user they need to enter a number

    # DELETE TASK
    def delete_task(self):
        if len(self.tasks) == 0: #Check if there are any tasks
            print("\nThere are no tasks to delete.\n") #Tell the user there are no tasks
            return #Stop the function
        self.view_tasks() #Display the tasks
        choice = input("Enter the task number to delete: ") #Ask the user which task they want to delete
        if choice.isdigit(): #Check whether the input is a number
            task_number = int(choice) #Convert the input to an integer
            if 1 <= task_number <= len(self.tasks): #Check whether the task number is valid
                removed_task = self.tasks.pop(task_number - 1) #Remove the selected task
                print(f"\n'{removed_task.name}' was deleted.\n") #Tell the user which task was deleted
            else:
                print("\nInvalid task number.\n") #Tell the user the number is invalid
        else:
            print("\nPlease enter a valid number.\n") #Tell the user to enter a valid number

# MAIN PROGRAM
task_manager = TaskManager() #Create a TaskManager object

running = True #This variable controls whether the program keeps running

while running: #Continue running while running is True.

    # Display the main menu.
    print("================================")
    print("     TASK MANAGEMENT SYSTEM")
    print("================================")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("================================")

    choice = input("Enter your choice: ") #Ask the user to choose an option
    if choice == "1": #Check if the user selected option 1
        task_manager.add_task() #Call the add_task method
    elif choice == "2": #Check if the user selected option 2
        task_manager.view_tasks() #Call the view_tasks method
    elif choice == "3": # Check if the user selected option 3.
        task_manager.complete_task() #Call the complete_task method
    elif choice == "4": #Check if the user selected option 4
        task_manager.delete_task() #Call the delete_task method
    elif choice == "5": #Check if the user selected option 5
        running = False #Stop the program
        print("\nThank you for using the Task Management System!") #Tell the user the program is closing
    else: #If the user enters anything else
        print("\nInvalid choice. Please select 1-5.\n") #Tell the user their choice is invalid