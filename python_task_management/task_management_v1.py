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

class TaskManager:
    # This class manages all of the tasks.

    def __init__(self):
        # Create an empty list to store Task objects.
        self.tasks = []

    # ADD TASK

    def add_task(self):
        # Ask the user to enter the task name.
        task_name = input("Enter the task name: ")
        # Ask the user to enter the priority.
        priority = input("Enter priority (High/Medium/Low): ")

        # Ask the user to enter the due date.
        due_date = input("Enter due date (e.g. 15/08/2026): ")

        # Create a new Task object.
        new_task = Task(task_name, priority, due_date)

        # Add the new Task object to the task list.
        self.tasks.append(new_task)

        # Tell the user that the task was added.
        print("\nTask added successfully!\n")


    # VIEW TASKS

    def view_tasks(self):
        # Check if there are no tasks.
        if len(self.tasks) == 0:

            # Tell the user there are no tasks.
            print("\nThere are no tasks to display.\n")

            # Stop the function.
            return

        # Print the heading.
        print("\n========== YOUR TASKS ==========")

        # Loop through every task.
        for number, task in enumerate(self.tasks, start=1):

            # Check whether the task has been completed.
            if task.completed:

                # Set the status to Completed.
                status = "Completed"

            else:

                # Set the status to Not Completed.
                status = "Not Completed"

            # Display the task number and name.
            print(f"\nTask {number}: {task.name}")

            # Display the priority.
            print(f"Priority: {task.priority}")

            # Display the due date.
            print(f"Due Date: {task.due_date}")

            # Display the completion status.
            print(f"Status: {status}")

        # Print a line at the bottom.
        print("\n================================\n")


    # COMPLETE TASK

    def complete_task(self):
        # Check if there are any tasks.
        if len(self.tasks) == 0:

            # Tell the user there are no tasks.
            print("\nThere are no tasks to complete.\n")

            # Stop the function.
            return

        # Display the current tasks.
        self.view_tasks()

        # Ask the user which task they want to complete.
        choice = input("Enter the task number to complete: ")

        # Check whether the input is a number.
        if choice.isdigit():

            # Convert the input to an integer.
            task_number = int(choice)

            # Check whether the task number is valid.
            if 1 <= task_number <= len(self.tasks):

                # Get the selected Task object.
                selected_task = self.tasks[task_number - 1]

                # Change its completed status to True.
                selected_task.completed = True

                # Tell the user the task was completed.
                print("\nTask marked as completed!\n")

            else:

                # Tell the user the number is invalid.
                print("\nInvalid task number.\n")

        else:

            # Tell the user they need to enter a number.
            print("\nPlease enter a valid number.\n")


    # DELETE TASK

    def delete_task(self):
        # Check if there are any tasks.
        if len(self.tasks) == 0:

            # Tell the user there are no tasks.
            print("\nThere are no tasks to delete.\n")

            # Stop the function.
            return

        # Display the tasks.
        self.view_tasks()

        # Ask the user which task they want to delete.
        choice = input("Enter the task number to delete: ")

        # Check whether the input is a number.
        if choice.isdigit():

            # Convert the input to an integer.
            task_number = int(choice)

            # Check whether the task number is valid.
            if 1 <= task_number <= len(self.tasks):

                # Remove the selected task.
                removed_task = self.tasks.pop(task_number - 1)

                # Tell the user which task was deleted.
                print(f"\n'{removed_task.name}' was deleted.\n")

            else:

                # Tell the user the number is invalid.
                print("\nInvalid task number.\n")

        else:

            # Tell the user to enter a valid number.
            print("\nPlease enter a valid number.\n")


# MAIN PROGRAM

# Create a TaskManager object.
task_manager = TaskManager()

# This variable controls whether the program keeps running.
running = True


# Continue running while running is True.
while running:

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

    # Ask the user to choose an option.
    choice = input("Enter your choice: ")

    # Check if the user selected option 1.
    if choice == "1":

        # Call the add_task method.
        task_manager.add_task()

    # Check if the user selected option 2.
    elif choice == "2":

        # Call the view_tasks method.
        task_manager.view_tasks()

    # Check if the user selected option 3.
    elif choice == "3":
        # Call the complete_task method.
        task_manager.complete_task()

    # Check if the user selected option 4.
    elif choice == "4":

        # Call the delete_task method.
        task_manager.delete_task()

    # Check if the user selected option 5.
    elif choice == "5":

        # Stop the program.
        running = False

        # Tell the user the program is closing.
        print("\nThank you for using the Task Management System!")

    # If the user enters anything else.
    else:

        # Tell the user their choice is invalid.
        print("\nInvalid choice. Please select 1-5.\n")