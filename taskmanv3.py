# This program is a task management system that allows users and admin to create and interact with tasks.
# The program reads user and task information from 'user.txt' and 'tasks.txt' files.
# Users can register a another user, add a task, view all the tasks in the system, and view and complete / edit/ 
# update / reassign tasks assigned to them.
# additionally the admin user can generate 2 external summary reports (task_overview.txt & user_overview) and 
# read them back in to display the reports on screen va display statitics. 
# The program also includes a login system to ensure only valid users have access to the system and that only those
# actions that their profile and conditions allow are available in the menu options.

#=========================================================
# Functions
#=========================================================
# Writes the task list to "tasks.txt".
def write_tasks_to_file():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for task in task_list:
            # Convert each task dictionary to a semicolon-separated string for writing to the file
            str_attrs = [
                task['task_number'],
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        # Write the task list to the file, with each task on a separate line
        task_file.write("\n".join(task_list_to_write))

# Updates tasks list, based on user input
def update_task(task_list):

    # Check if the user has any incomplete tasks
    incomplete_tasks = [task for task in task_list if task['username'] == curr_user and not task['completed']]
    if not incomplete_tasks:
        any_key_proceed_2 = input("\nYou don't have any incomplete tasks! None of your tasks are editable, enter any key to return to main menu : ")
        main_menu(curr_user)
        return
    any_key_proceed_3 = input("\nEnter any key to see a list of tasks that you can update or -1 to return to main menu: ")
    if any_key_proceed_3 == "-1":
        main_menu(curr_user)
        return
    
    else:  
        # Call view_mine() function to display the list of tasks that can be updated
        view_mine(False)
        while True:
            # Ask the user to enter the task number to open it, or -1 to return to main menu
            task_num = input("\nEnter task number to open it or '-1' to return to main menu: ")
            if task_num == '-1':
                main_menu(curr_user)
                return
            else:
                # Search for the task in the list by task number, username and completion status
                task = next((task for task in task_list if (task['task_number'] == task_num and task['username'] == curr_user and task['completed'] == False)), None)
                if task is None:
                    print("\nTask number not recognised, please enter a task number from the tasks displayed")
                    view_mine(False)
                    continue
                else:
                    # If the task is found, prompt to choose action. After each action write the tasks.txt file, advises user of update
                    # then returns to top of the function or user can exit. User gets advised if errors occur.
                    print(f"\nTask {task_num} opened")
                    while True:
                        action = input("\nYou can complete a task(c), edit a task(e), or return to main menu(-1): ").lower()
                        if action == 'c':
                            task['completed'] = True
                            print(f"\nTask {task_num} marked as completed.")
                            write_tasks_to_file()
                            update_task(task_list)
                            return
                        elif action == 'e':
                            while True:
                                # If the user chooses to edit the task, ask them to choose a sub-action
                                sub_action = input("\nYou can reassign a task(r), update the due date(u) or exit(-1): ").lower()
                                if sub_action == 'r':
                                    reassigned = input("\nEnter the username of the new assignee: ").lower()
                                    # checks if the new assignee exists
                                    if reassigned in username_password:
                                        task['username'] = reassigned
                                        print(f"\nTask {task_num} has been reassigned to {reassigned}.")
                                        write_tasks_to_file() 
                                        update_task(task_list)
                                        return
                                    else: print("\nUser doesn't exit, please try again.") 
                                    continue   
                                elif sub_action == 'u': 
                                    while True:
                                        new_due_date_str = input("\nEnter the new due date of the task (YYYY-MM-DD): ")
                                        try:
                                            new_due_date = datetime.strptime(new_due_date_str, DATETIME_STRING_FORMAT)  # converts the user input to a datetime object
                                            if new_due_date >= datetime.now() - timedelta(days=1):  # checks if the new due date is either today or a future date
                                                task['due_date'] = new_due_date 
                                                print(f"\nTask {task_num} due date updated to {new_due_date_str}.")  
                                                write_tasks_to_file() 
                                                update_task(task_list)
                                                return
                                            else:
                                                print("\nDue date must be either today or a future date, please try again.") 
                                        except ValueError:
                                            print("\nInvalid datetime format!! Please try again.")  # prints an error message if the user input is not in the correct format

                                elif sub_action == '-1':  
                                    main_menu(curr_user)  
                                    return

                                else:
                                    print("\nOption not recognised, choose from the options below :") 
                                    continue  # continues the while loop to ask for valid user input again

                        elif action == '-1':  
                            main_menu(curr_user)
                            return

                        else:
                            print("\nOption not recognised, choose from the options below")  
                            continue  # continues the while loop to ask for valid user input again
                    
# authenticates user
def login(curr_user, curr_pass):
    logged_in = False
    if curr_user not in username_password.keys():
        print("\nUser does not exist!!")
    elif username_password[curr_user] != curr_pass:
        print("\nWrong password!!")
    # if user exists and password is correct log them in
    else:
        print("\nLogin Successful!")
        logged_in = True
    return logged_in

# adds a new task to the task list
def add_task():
    # user is prompted to input task details
    while True:
        task_username = input("Name of person assigned to task (-1 to return to main menu): ").lower()
        
        # Check if the user wants to return to main menu
        if task_username == '-1':
            break
        
        # Check if the user exists in the system
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue

        # Generate a unique task number using the current date and time
        task_number = str(datetime.today()).replace(":","")
        task_number = task_number.replace("-","")
        task_number = task_number.replace(" ","")
        task_number = task_number[2:14]

        task_title = input("Title of Task (-1 to return to main menu): ")
        
        # Check if the user wants to return to main menu
        if task_title == '-1':
            break
        
        if len(task_title) > 25:
            print("Must be 25 characters or less. Please try again.")
            continue

        task_description = input("Description of Task (-1 to return to main menu): ")
        
        # Check if the user wants to return to main menu
        if task_description == '-1':
            break

        # Get the due date of the task from the user, and convert it to a datetime
        while True:
            task_due_date = input("Due date of task (YYYY-MM-DD) (-1 to return to main menu): ")
            
            # Check if the user wants to return to main menu
            if task_due_date == '-1':
                break
            
            try:
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Check if the user wants to return to main menu
        if task_due_date == '-1':
            break

        # Set the assigned date of the task to the current date
        curr_date = date.today()
        
        # Create a new task dictionary with the user-provided information
        new_task = {
            "task_number" : str(task_number),
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
        # Add the new task to the task list, and writes the updated task list to a file
        task_list.append(new_task)
        write_tasks_to_file() 
        break

# allows user to navigate the system
def main_menu(curr_user):

    while True:
        print("\n---- Main Menu ----\n")
        
        # Determines the current user's profile
        if curr_user == "admin":
            curr_user_profile = "admin"
        else:
            curr_user_profile = "all"
        
        # Create a list of menu options
        menu_list = [
            ["r", " - Registering a user", "all"],
            ["a", " - Adding a task", "all"],
            ["va", "- View all tasks", "all"],
            ["vm", "- View my task", "all"],
            ["ds", "- Display statistics", "admin"],
            ["gr", "- Generate reports", "admin"],
            ["e", " - Exit", "all"]
        ]
        
        # Display the menu options based on the current user's profile
        for option in menu_list:
            if curr_user_profile == "admin":
                print(option[0], option[1])
            elif option[2] == curr_user_profile:
                print(option[0], option[1])
        
        # Prompt the user to select an option
        menu_opt = input("\nPlease select an option: ").lower()
        
        # Handle the user's input based on the selected option
        if menu_opt == "e":
            break
        elif menu_opt == "a":
            add_task()
        elif menu_opt == "r":
            reg_user()

        elif menu_opt == "va":
            view_all()
            any_key_proceed_5 = input("\n\n\t> Enter any key to return to main menu : ")

        elif menu_opt == "vm":
            view_mine()   
            update_task(task_list)
            break

        elif menu_opt == "ds" and curr_user_profile == "admin":
                if not os.path.exists('task_overview.txt') or not os.path.exists('user_overview.txt'):
                    generate_reports()
                    display_stats()
                else:    
                    display_stats()
                any_key_proceed_6 = input("\n\n\t> Enter any key to return to main menu : ")
        elif menu_opt == "ds" and curr_user_profile != "admin":
            print("sorry only for admins! Please select from the options displayed below :")
        elif menu_opt == "gr" and curr_user_profile == "admin":
            generate_reports()  
        elif menu_opt == "gr" and curr_user_profile != "admin":
            print("sorry only for admins! Please select from the options displayed below :")
        else:
            print("\n\t> Input error, please select from the list to try again.\n")
            continue
   
# creates a new user
def reg_user():
    while True:
        # Ask user for new username and check if the username already exists in the "user.txt" file
        new_username = input("New Username (or enter -1 to return to main menu): ").lower()
        if new_username == '-1':
            break # Exit the loop and return to main menu if -1 is entered
        elif len(new_username) > 25:
            print("\nMust be 25 characters or less. Please try again.\n")
            continue
        else:
            with open("user.txt", "r") as in_file:
                for line in in_file:
                    username, _ = line.strip().split(';')
                    if new_username == username:
                        print("\nUsername already exists, please try again :\n")
                        break
                else: # If username doesn't already exist
                    # Get password, confirm it, write username and password to "user.txt", then print success message 
                    new_password = input("New Password: ")
                    confirm_password = input("Confirm Password: ")
                    if new_password == confirm_password:
                        print("New user added")
                        with open("user.txt", "a") as out_file:
                            out_file.write(f"\n{new_username};{new_password}")
                            out_file.seek(0)
                            username_password[new_username] = new_password # add new user to dictionary
                        break # Exit the loop if successful
                    # If the passwords don't match, print an error message
                    else:
                        print("\nPasswords do not match. Please try again.\n")
                        continue

# displays the task list in a table format, for user friendly viewing
def view_tasks(menu, curr_user=None, status=None):
    if curr_user ==None:
        print("\n\t> Displaying tasks for all users")
    else:
        print("\n\t> Displaying your tasks (user :\t{})\n".format(curr_user))
    if menu == "va" or menu == "vm":
        print("\n\n{:<15} {:<25} {:<25} {:<12} {:<11} {:<5} {:<33}".format(
            "Task Number", "Task", "Assigned To", "Assigned", "Due", "Done", "Task Description"))
        print("=" * 132)    # header underline
        for task in task_list:
            if (curr_user is None or task['username'] == curr_user) and (status is None or task['completed'] == status):
                # Split task description into multiple lines if it exceeds 33 characters
                desc_lines = [task['description'][lines:lines+33] for lines in range(0, len(task['description']), 33)]
                # Join the lines into a single string with newlines
                desc_str = "\n\t\t\t\t\t\t\t\t\t\t\t\t   ".join(desc_lines)
                # Convert completed value to "yes" or "no"
                completed_str = "yes" if task['completed'] else "no"
                disp_str = "{:<15} {:<25} {:<25} {:<12} {:<11} {:^5} {:<33}".format(
                    task['task_number'], task['title'], task['username'], 
                    task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    task['due_date'].strftime(DATETIME_STRING_FORMAT), 
                    completed_str, desc_str)
                print(disp_str)

# reads in and prints 2 reports task_overview.txt and user_overview.txt
def display_stats():
    with open("task_overview.txt", "r") as task_file:
        lines = task_file.readlines()
        print("".join(lines[:-1]))
        #print("\n" + task_file.read()-1)   # removes report run date, as code repeats below, so it would written twice otherwise. 
    with open("user_overview.txt", "r") as user_file:
        lines = user_file.readlines()
        print("\n")
        print("".join(lines[:]))

# creates /overwrites 2 reports : task_overview.txt and user_overview.txt
def generate_reports():
    global_task = overview_aggregates(d_date_f = 'due_date', d_date_v = dummy_date)
    user_count = len(username_password)
    underline = 130 * "="
    report_run = (str(datetime.now())[0:19])
    spacer = 17 * " "
    with open("task_overview.txt", "w") as file: 
        file.write ("\n> Task Summary - totals for Task Manager system below : \n\n\n")
        
        # creates task table header and combines with body in task_summary function
        file.write("{:<25} {:^10} {:>10} {:<17} {:^8} {:>34} {:^8}\n{}\n".format("", "generated","completed", " not completed(nc)", "nc %", "not completed & overdue(nco)  ", "nco %", underline))
        file.write(task_summary())
        file.write(underline)

        file.write("\n\nreport run : {}".format(report_run)) # user note, gives report creation date & time
        file.close
  
    with open("user_overview.txt", "w") as file: 
        file.write("\n> User Summary - There are {} users registered in this system.\n{}The system has generated and tracked {} tasks to date.\n{}Tasks have been assigned to users as per the table below : \n\n".format(user_count, spacer, global_task, spacer))
        
        # creates user table header 
        file.write("{:<25} {:^8} {:^10} {:>10} {:<17} {:^8} {:^34} {:<8}\n{}\n".format("users", "assigned(a)"," a %" ,"completed", " not completed(nc)", "nc %", "not completed & overdue(nco)  ", "nco %", underline))
        
        # creates user table body and numbers each user
        loop = 0
        for user in username_password:
            loop = loop + 1
            file.write("{}. ".format(loop) + (user_summary(user)))
        file.write(underline)
        file.write("\n\nreport run : {}".format(report_run))    # user note, gives report creation date & time
        file.close
    any_key_to_proceed_7 = input("\n> 2 reports task_overview.txt and user_overview.txt, have been updated and saved! Enter any key to continue : " ) 

# utilised by def user_summary() and def task_summary to loop over aggregate calculations
def overview_aggregates(compd_F = None, compd_v = None, d_date_f = None, d_date_v=None, username=None):
    count = 0
    for sublist in task_list:
        if (not compd_F or sublist[compd_F] == compd_v) and (not d_date_f or sublist[d_date_f] < d_date_v):
            if username and sublist['username'] != username:
                continue
            count = count + 1
    return count

# creates the body of user summary table output, used in generate reports function. uses def overview_aggregates for calculations
def user_summary(user):
    # Work around for divide by zero errors. sub_value used to avoid the error
    sub_value_u = "0.00" 
    global_task = overview_aggregates(d_date_f = 'due_date', d_date_v = dummy_date)
    # calculates aggregrated amounts except those affected by divide by zero error 
    tasks_completed = overview_aggregates('completed',True, 'due_date', dummy_date, user)
    tasks_not_completed = overview_aggregates('completed',False, 'due_date', dummy_date, user)
    total_tasks = tasks_not_completed + tasks_completed
    tasks_overdue = (overview_aggregates('completed', False,'due_date', datetime.now(), user))
    
    if total_tasks == 0:
        output ="{:<25} {:^10} {:>8} {:^10} {:^17} {:>8} {:^32} {:>8}\n".format(user, total_tasks, sub_value_u + " %", tasks_completed, tasks_not_completed, sub_value_u  + " %", tasks_overdue, sub_value_u  + " %" )
    
    # regular processing 
    else: 
        percent_not_completed = (tasks_not_completed / total_tasks) * 100
        format_percent_not_completed = "{:.2f}".format(percent_not_completed)
        percent_overdue = (tasks_overdue / total_tasks) * 100
        format_percent_overdue = "{:.2f}".format(percent_overdue)  
        percent_assigned = (total_tasks / global_task) * 100
        format_percent_assigned = "{:.2f}".format(percent_assigned) 
        output ="{:<25} {:^10} {:>8} {:^10} {:^17} {:>8} {:^32} {:>8}\n".format(user, total_tasks, format_percent_assigned +" %" ,tasks_completed, tasks_not_completed, format_percent_not_completed  + " %", tasks_overdue, format_percent_overdue  + " %")
    return(output)

# creates the body of task summary table output, used in generate reports function. uses def overview_aggregates for calculations
def task_summary():
    # Work around for divide by zero errors. sub_value_t used to avoid the error
    sub_value_t = "0" 
    # calculates aggregrated amounts except those affected by divide by zero error
    tasks_completed = overview_aggregates('completed',True, 'due_date', dummy_date)
    tasks_not_completed = overview_aggregates('completed',False, 'due_date', dummy_date)
    total_tasks = tasks_not_completed + tasks_completed
    tasks_overdue = (overview_aggregates('completed', False,'due_date', datetime.now()))
    
    if total_tasks == 0:
        output ="{:<25} {:^10} {:^10} {:^17} {:<8}% {:^32} {:<8}%\n".format("Task Totals : ", total_tasks, tasks_completed, tasks_not_completed, sub_value_t, tasks_overdue, sub_value_t )    
    
    # regular process
    else: 
        percent_not_completed = (tasks_not_completed / total_tasks) * 100
        format_percent_not_completed = "{:.2f}".format(percent_not_completed)
        percent_overdue = (tasks_overdue / total_tasks) * 100
        format_percent_overdue = "{:.2f}".format(percent_overdue)   
        output ="{:<28} {:^10} {:^10} {:^17} {:<8}% {:^32} {:<8}%\n".format("Task Totals : ", total_tasks, tasks_completed, tasks_not_completed, format_percent_not_completed, tasks_overdue, format_percent_overdue )

    return(output)

# left in as per requirements. Calls view_tasks.
def view_mine(comp_status=None):
    view_tasks("vm", curr_user,status = comp_status)

# left in as per requirements. Calls view_tasks.
def view_all():
    #print("\n\t> Displaying all tasks")
    view_tasks("va")

#=========================================================
# Programme Resources - Global variables & Essential Files 
#=========================================================
# Import necessary modules
import os
from datetime import datetime, date, timedelta

# Set a dummy date to get all tasks
dummy_date = datetime.now() + timedelta(days=365*1000)

# date format string for datetime objects
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt file if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Read task data from tasks.txt and create a list of task dictionaries
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [task for task in task_data if task != ""]

    task_list = []
    for item, task_str in enumerate(task_data):
        curr_task = {}

        # Split task data by semicolon and add each component to the current task dictionary
        task_components = task_str.split(";")
        curr_task['task_number'] = task_components[0]
        curr_task['username'] = task_components[1]
        curr_task['title'] = task_components[2]
        curr_task['description'] = task_components[3]
        curr_task['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_task['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
        curr_task['completed'] = True if task_components[6] == "Yes" else False

        task_list.append(curr_task)

# Create user.txt file with default account if it doesn't exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read user data from user.txt and create a dictionary
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
        
#==================================================
# Program start
#==================================================
logged_in = False


# Prompt the user to login until they provide valid credentials
while not logged_in:
    print("\nLOGIN")

    # Prompt the user for their username and password, then display main menu.
    curr_user = "admin"#input("Username: ").lower()
    curr_pass = "password"#input("Please supply your Password (case sensitive): ")
    logged_in = login(curr_user, curr_pass)
    if logged_in:
        main_menu(curr_user)
        logged_in = True

    # If the user is not logged in, prompt them to try again or exit
    else:
        question = input("\nPress any key to try again or type e to exit : ").lower()
        if question == 'e':
            break
        else:
            continue
print("\n > End\n")
#====================================================
# Programme End
#==================================================== 
