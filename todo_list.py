import sqlite3

add_on = True

# Connect to the SQLite database
connection = sqlite3.connect('todo_list.db')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()
print("Connected to the database successfully!")

# Add Features (One at a Time)
def add_todo_list():
    name = input("Name: ")
    description = input("Description: ")
    due_date = input("Duedate(YYYY-MM-DD): ")
    status = "Incomplete"
    list_query = """
INSERT INTO todo_list (name, description, due_date, status)
VALUES (?, ?, ?, ?);
"""
    list = (name, description, due_date, status)
    cursor.execute(list_query, list)
    connection.commit()

# View All Lists
def view_todo_lists():
    select_query = "SELECT * FROM todo_list;"
    cursor.execute(select_query)
    todos = cursor.fetchall()
    print("Current lists in the database:")
    for todo in todos:
        print(todo)    
    if not todos:
        print("No lists found in the database.")

# Update List Status
def mark_complete(list_id):
    cursor.execute("UPDATE todo_list SET status = 'Complete' WHERE id = ?", (list_id,))
    connection.commit()

# Delete a list
def delete_list(list_id):
    cursor.execute("DELETE FROM todo_list WHERE id = ?", (list_id,))
    connection.commit()

# Clear all lists
def clear_lists():
    cursor.execute("DELETE FROM todo_list")
    # Reset id to 1
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='todo_list'")
    connection.commit()

# Get status
def get_status():
    status_option = int(input("\n1.Incomplete\n2.Complete\n==> "))
    return 'Incomplete' if status_option == 1 else 'Complete' if status_option == 2 else None

# Filter lists by due date or status
def filter_lists():
    try:
        filter_option = int(input("\nSort list by\n1. Due date\n2. Status\n3. Due date and Status\n==> "))
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
    todos = cursor.fetchall()
    print("\nCurrent lists in the database:")
    for todo in todos:
        print(todo)
    if not todos:
        print("No lists found in the database.")

while add_on:
    print("\n===========================")
    print("Hello, how can I help you?")
    print("===========================\n")
    try:
        option = int(input("1. Add List\n2. View Lists\n3. Mark List as Complete\n4. Delete List\n5. Exit\n==> "))
        if option == 1:
            add_todo_list()
            view_todo_lists()
        elif option == 2:
            view_todo_lists()
            filter_lists()
        elif option == 3:
            list_id = input("Which id did you finish? ")
            mark_complete(list_id)
            view_todo_lists()
        elif option == 4:
            sub_option = input("Do you want to clear all lists?(y/n) ")
            if sub_option == 'y':
                clear_lists()
            elif sub_option == 'n':
                list_id = input("Which id do you want to delete? ")
                delete_list(list_id)
            view_todo_lists()
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