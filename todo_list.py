import sqlite3

add_on = True

# Connect to the SQLite database
connection = sqlite3.connect('todo_list.db')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()
print("Connected to the database successfully!")

# Add Features (One at a Time)
def add_task():
    name = input("Name: ")
    description = input("Description: ")
    due_date = input("Duedate(YYYY-MM-DD): ")
    status = "Incomplete"
    task_query = """
INSERT INTO todo_list (name, description, due_date, status)
VALUES (?, ?, ?, ?);
"""
    task = (name, description, due_date, status)
    cursor.execute(task_query, task)
    connection.commit()

# View All tasks
def view_tasks():
    select_query = "SELECT * FROM todo_list;"
    cursor.execute(select_query)
    tasks = cursor.fetchall()
    print("Current tasks in the database:")
    for task in tasks:
        print(task)    
    if not tasks:
        print("No tasks found in the database.")

# Update task Status
def mark_complete(task_id):
    cursor.execute("UPDATE todo_list SET status = 'Complete' WHERE id = ?", (task_id,))
    connection.commit()

# Delete a list
def delete_task(task_id):
    cursor.execute("DELETE FROM todo_list WHERE id = ?", (task_id,))
    connection.commit()

# Clear all tasks
def clear_tasks():
    cursor.execute("DELETE FROM todo_list")
    # Reset id to 1
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='todo_list'")
    connection.commit()

# Get status
def get_status():
    status_option = int(input("\n1.Incomplete\n2.Complete\n==> "))
    return 'Incomplete' if status_option == 1 else 'Complete' if status_option == 2 else None

# Filter lists by due date or status
def filter_tasks():
    try:
        filter_option = int(input("\nSort tasks by\n1. Due date\n2. Status\n3. Due date and Status\n==> "))
        if filter_option == 1:
            cursor.execute("SELECT * FROM todo_list ORDER BY due_date")
        elif filter_option == 2:
            status_value = get_status()
            cursor.execute("SELECT * FROM todo_list WHERE status=?", (status_value, ))
        elif filter_option == 3:
            status_value = get_status()
            cursor.execute("SELECT * FROM todo_list WHERE status=? ORDER BY due_date", (status_value, ))
        else:
            print("Please try again.")
    except ValueError:
        print("\nInvalid input! Please enter a number.")
    tasks = cursor.fetchall()
    print("\nCurrent tasks in the database:")
    for task in tasks:
        print(task)
    if not tasks:
        print("No tasks found in the database.")

while add_on:
    print("\n===========================")
    print("Hello, how can I help you?")
    print("===========================\n")
    try:
        option = int(input("1. Add Task\n2. View Tasks\n3. Mark Task as Complete\n4. Delete Task\n5. Exit\n==> "))
        if option == 1:
            add_task()
            view_tasks()
        elif option == 2:
            view_tasks()
            filter_tasks()
        elif option == 3:
            task_id = input("Which id did you finish? ")
            mark_complete(task_id)
            view_tasks()
        elif option == 4:
            sub_option = input("Do you want to clear all lists?(y/n) ")
            if sub_option == 'y':
                clear_tasks()
            elif sub_option == 'n':
                task_id = input("Which id do you want to delete? ")
                delete_task(task_id)
            view_tasks()
        elif option == 5:
            print("\n===================")
            print("Thank you for using.")
            print("===================\n")
            add_on = False
        else:
            print("\nPlease re-select one of the options.")
    except ValueError:
        print("\nInvalid input! Please enter a number.")

connection.close()
print("Database connection closed!")