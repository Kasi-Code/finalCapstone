""" THAT WAS A DIAMOND CHALLENGE!!! 😭 """

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import copy, re, os
from datetime import datetime, date

# Functions created in different file: minimal code - easy for read
from functions import reg_user, selecting_task_num, selecting_username

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
user_data = [] 
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# print(user_data)

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
curr_user = ""
while not logged_in:

    print("LOGIN")
    curr_user = str(input("Username: ")).capitalize()
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        print(f"\nHello {curr_user}!")
        logged_in = True

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
  r - Registering a user
  a - Adding a task
  va - View all tasks
  vm - View my task
  gr - Generate report
  ds - Display statistics
  e - Exit
  : ''').lower()
    print()

    if menu == 'r':
        num_of_index = []
        while True: # <-- Added loop
            '''Add a new user to the user.txt file'''
            # - Request input of a new username
            new_username = str(input("New Username: ")).capitalize()

            new_username = reg_user(new_username) # <-- deployed function

            if new_username is False:
                print("\nI'm sorry, this name is taken! Please try agin.")
                break # <-- Break the loop to ask for username again

            # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print(f"\nNew user {new_username} added.")
                username_password[new_username] = new_password

                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                    break # <-- Need this

            # - Otherwise you present a relevant message.
            else:
                print("Passwords do no match")

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ").capitalize()
        print()
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("\nTask successfully added.")

    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            # Missing
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        # Display all tasks
        curr_user_task_list = []
        for t in task_list:
            if t['username'] == curr_user:
                if "%Y-%m-%d" in task_list:
                    disp_str = f"Task {len(curr_user_task_list) + 1}: \t\t {t['title']}\n"
                    disp_str += f"Assigned to: \t\t {t['username'].capitalize()}\n"
                    disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Completed: \t\t {'Yes' if t['completed'] else 'No'}\n" # <-- Missing
                    disp_str += f"Task Description: \n {t['description']}\n"
                    print(f"{disp_str}")
                    curr_user_task_list.append(t)
                else:
                    disp_str = f"Task {len(curr_user_task_list) + 1}: \t\t {t['title']}\n"
                    disp_str += f"Assigned to: \t\t {t['username'].capitalize()}\n"
                    disp_str += f"Date Assigned: \t\t {t['assigned_date']}\n"
                    disp_str += f"Due Date: \t\t {t['due_date']}\n"
                    disp_str += f"Completed: \t\t {'Yes' if t['completed'] else 'No'}\n"
                    disp_str += f"Task Description: \n {t['description']}\n"
                    print(f"{disp_str}")
                    curr_user_task_list.append(t)

        num_of_index = [i for i in range(1, len(curr_user_task_list) + 1)]

        while True:
            if not num_of_index:
                print("You have no task.")
                break
            else:
                print()
                specific_task = input('''Select one of the following options below:
    -1 - Return to the main menu
    tc - Mark the task as complete
    et - Edit the task
    : ''').lower()

                with open("tasks.txt", "r+") as task_file:
                    task_lines = task_file.readlines()

                    task_list_txt = []
                    task_components_txt = []
                    for line in task_lines:

                        all_t = {}

                        # Split by semicolon and manually add each component
                        task_components_txt = line.strip().split(";")
                        all_t['username'] = task_components_txt[0]
                        all_t['title'] = task_components_txt[1]
                        all_t['description'] = task_components_txt[2]
                        all_t['due_date'] = task_components_txt[3]
                        all_t['assigned_date'] = task_components_txt[4]
                        all_t['completed'] = bool(task_components_txt[5].strip() == 'Yes')

                        task_list_txt.append(all_t)

                selected_task = {}
                if specific_task == "-1":
                    break
                elif specific_task == "tc":
                    print("\nWhich task have you completed?")

                    task_num = selecting_task_num(num_of_index)
                    if task_num is False:
                        selected_task = False
                    else:
                        selected_task = curr_user_task_list[task_num - 1]

                    for t in task_list_txt:
                        if selected_task is False:
                            print("Task not found.\n")
                            break
                        elif (
                            selected_task["username"] == t["username"] 
                            and selected_task["title"] == t["title"] 
                            and t["completed"]
                        ):
                            print(f"Task {task_num} is already completed.")
                            break
                        elif (
                            selected_task["username"] == t["username"] 
                            and selected_task["title"] == t["title"] 
                            and not t["completed"]
                        ):
                            answer = input(
                                f"NOTE: You will not be able to edit this task once marked as completed!"
                                f"\n\nMark task {task_num} as complete? (Y / N): "
                            ).lower()
                            if answer == "y":
                                t['completed'] = True  # Update the task status in the list
                                print(f"\nTask {task_num} marked as complete.")
                                break
                            elif answer == "n":
                                print(f"\nTask {task_num} not marked as complete.")
                                break
                            else:
                                print("Invalid input. Please enter 'Y' or 'N'.")
                                break
                    else:
                        # The 'else' block will only be executed if the 'for' 
                        # loop completes without encountering a 'break'
                        print("Task not found.\n")
                        break

                    # After processing the changes, 
                    # write the updated list back to the tasks.txt file
                    with open("tasks.txt", "w") as task_file:
                        for t in task_list_txt:
                            task_file.write(
                                f"{t['username']};{t['title']};{t['description']};{t['due_date']};"
                                f"{t['assigned_date']};{'Yes' if t['completed'] else 'No'}\n"
                            )

                    # Refresh curr_user_task_list after marking a task as complete
                    task_list = [t for t in task_list_txt if t['username'] == curr_user]
                    num_of_index = [i for i in range(1, len(curr_user_task_list) + 1)]
                    # break

                elif specific_task == "et":

                    # Refresh curr_user_task_list for editing
                    curr_user_task_list = [t for t in task_list_txt if t['username'] == curr_user]
                    selected_edit_option = input('''\nEditing task...

    Select one of the following options below:
        -1 - Return to the main menu
        at - Assign task to different user
        dd - Change the due date
        : ''').lower()

                    if selected_edit_option == "-1":
                        break
                    elif selected_edit_option == "at":
                        selected_name_value = ""
                        print("\nWhich task would you like to reassigned the name?")

                        task_num = selecting_task_num(num_of_index)
                        if task_num is False:
                            selected_task = False
                        else:                              
                            selected_task = curr_user_task_list[task_num - 1]
                            if selected_task["completed"]:
                              print(
                                  f"Can't edit task {task_num} "
                                  f"because it's already completed."
                              )
                              selected_task = False
                            else:
                              selected_name = selecting_username(user_data)
                              selected_name_value = selected_name["name"]

                        for t in task_list_txt:
                            if selected_task is False:
                                break
                            elif (
                                selected_task["username"] == t["username"] 
                                and selected_task["title"] == t["title"]
                            ):
                                t["username"] = selected_name_value  # Update the task username in the list
                                print(f"\nTask {task_num} assigned to {selected_name_value}.")
                                break
                        else:
                            # The 'else' block will only be executed if the 'for' 
                            # loop completes without encountering a 'break'
                            print(f"Task {task_num} not found.")

                        # After processing the changes, write the updated 
                        # list back to the tasks.txt file
                        with open("tasks.txt", "w") as task_file:
                            for t in task_list_txt:
                                task_file.write(
                                    f"{t['username']};{t['title']};{t['description']};"
                                    f"{t['due_date']};{t['assigned_date']};"
                                    f"{'Yes' if t['completed'] else 'No'}\n"
                                )

                        # Refresh curr_user_task_list after marking a task as complete
                        task_list = [t for t in task_list_txt if t['username'] == curr_user]
                        num_of_index = [i for i in range(1, len(curr_user_task_list) + 1)]
                        # break

                    elif selected_edit_option == "dd":   
                        new_due_date = ""
                        print("\nWhich task would you like to change the due date?")

                        task_num = selecting_task_num(num_of_index)
                        if task_num is False:
                            selected_task = False
                        else:                              
                            selected_task = curr_user_task_list[task_num - 1]
                            if selected_task["completed"]:                              
                              print(f"Can't edit task {task_num} because it's already completed.")
                              selected_task = False
                            else:
                              selected_task = curr_user_task_list[task_num - 1]

                              while True:
                                try:
                                    new_due_date = input(f"Enter the new due date for task {task_num} (YYYY-MM-DD): ")
                                    due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                    break

                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")

                        for t in task_list_txt:
                            if selected_task is False:
                                break
                            elif (
                                selected_task["username"] == t["username"] 
                                and selected_task["title"] == t["title"]
                            ):
                                t["due_date"] = new_due_date                                
                                print(
                                    f"\nTask {task_num} due date" 
                                    f"chnaged to {new_due_date}.")
                                break
                        else:
                            # The 'else' block will only be executed if the 'for' 
                            # loop completes without encountering a 'break'
                            print(f"Task {task_num} not found.")

                        # After processing the changes, write the updated list 
                        # back to the tasks.txt file
                        with open("tasks.txt", "w") as task_file:
                            for t in task_list_txt:
                                task_file.write(
                                    f"{t['username']};{t['title']};{t['description']};"
                                    f"{t['due_date']};{t['assigned_date']};"
                                    f"{'Yes' if t['completed'] else 'No'}\n"
                                )

                        # Refresh curr_user_task_list after marking a task as complete
                        task_list = [t for t in task_list_txt if t['username'] == curr_user]
                        num_of_index = [i for i in range(1, len(curr_user_task_list) + 1)]
                        # break
                    else:
                        print()
                        print("Invalid option. Please enter a valid optons.")
                        break

                    # Refresh curr_user_task_list after marking a task as complete
                    task_list = [t for t in task_list_txt if t['username'] == curr_user]
                    num_of_index = [i for i in range(1, len(curr_user_task_list) + 1)]
                    # break

    elif menu == 'gr':
        # Update task_list to match the latest data
        with open("tasks.txt", "r") as task_file:
            task_data = task_file.read().split("\n")
            task_data = [t for t in task_data if t != ""]

        task_list = []
        for t_str in task_data:
            curr_t = {}

            task_components = t_str.split(";")
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
            curr_t['completed'] = True if task_components[5] == "Yes" else False

            task_list.append(curr_t)

        curr_user_num_task = 0
        for user in task_list:
            if curr_user == user["username"]:
                curr_user_num_task += 1

        curr_date = date.today()

        # For user_overview
        num_tasks = len(task_list)    
        num_tasks_completed = 0
        num_tasks_incomplete = 0
        overdue_tasks = 0
        uncompleted_and_overdue = 0

        # For user_overview
        num_users = len(username_password.keys())
        num_tasks_assigned_to_user = 0
        num_tasks_completed_by_user = 0

        for v in task_list:
            if v["completed"]:
                num_tasks_completed += 1

            if not v["completed"]:
                num_tasks_incomplete += 1

            due_date_datetime = v["due_date"]
            due_date = due_date_datetime.date() 
            if curr_date > due_date:
                overdue_tasks += 1

            if not v["completed"] and curr_date > due_date:
                uncompleted_and_overdue += 1

            if curr_user == v["username"] and v['title']:
                num_tasks_assigned_to_user += 1

            if curr_user == v["username"] and v["title"] and v["completed"]:
              num_tasks_completed_by_user += 1

      # For user_overview
        num_users = len(username_password.keys())
        percent_of_incomplete = (num_tasks_incomplete / num_tasks) * 100 
        percent_of_overdue = (overdue_tasks / num_tasks) * 100 

        # For user_overview
        if curr_user_num_task < 1:
            percentage_task_for_user = 0 
            percentage_completed_task_by_user = 0
            percentage_completed_task_by_user = 0 
        else:
            percentage_task_for_user = (num_tasks_assigned_to_user / num_tasks) * 100 
            percentage_completed_task_by_user = 0
            percentage_completed_task_by_user = (num_tasks_completed_by_user / num_tasks_assigned_to_user) * 100 

        task_overview_file = open("task_overview.txt", "w+")
        task_overview_file.write(f"""The Overview Report For Task: -

- {num_tasks} task(s) generated in total.
- {num_tasks_completed} task(s) completed in total.
- {num_tasks_incomplete} task(s) uncompleted in total.
- {uncompleted_and_overdue} task(s) uncompleted and overdue in total.
- {round(percent_of_incomplete)}% incomplete task(s) in total.
- {round(percent_of_overdue)}% overdue task(s) in total.

(Printed {curr_date})""")

        task_overview_file.close()

        user_overview_file = open("user_overview.txt", "w+")
        user_overview_file.write(f"""The Overview Report For {curr_user}: -

- {num_tasks_assigned_to_user} task(s) assigned to you in total.
- {round(percentage_task_for_user)}% of the task(s) assigned to you in total.
- {round(percentage_completed_task_by_user)}% of the task(s) you completed in total.

There are {num_users} user(s) registered in total.

(Printed {curr_date})""")

        user_overview_file.close()

        print(
            """<< >> Generated reports << >> 
            
Please find the files for
'user_overview' and 'task_overview' 
in the main folder."""
        )

    elif menu == 'ds' and curr_user == 'Admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'ds' and curr_user != 'Admin':
        print("Only Admin can select this option.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
