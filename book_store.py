# Capstone Project L2T13
import sqlite3

db = sqlite3.connect('ebookstore') # Open db
cursor = db.cursor()  # Get a cursor object


def view(selection):
    '''Iterates through the cursor object from a SQL query to display the output of a book info '''

    for item in selection:
        print(f"ID: {item[0]}, TITLE: {item[1]}, AUTHOR: {item[2]}, QTY: {item[3]}")
    return


def init_db():
    ''' Initialises the book table. If it already exists then exception is caught and moves on'''

    initial_data = [[3001, "A Tale of Two Cities", "Charles Dickens", 30],
                    [3002, "Harry Potter and the Philospher's Stone", "J.K. Rowling", 40],
                    [3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25],
                    [3004, "The Lord of the Rings", "J.R.R. Tolkien", 37],
                    [3005, "Alice in Wonderland", "Lewis Carrol", 12]]
    
    try:
        cursor.execute('''CREATE TABLE book(
                       id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)'''
                       )
        for item in initial_data:
            insert_book(item) # Function call that inserts book info into the table
        db.commit()
    except Exception:
        db.rollback()

    return

def insert_book(book):
    ''' Takes in list variable with the book info and adds it into the table.
        TRY block used to catch duplicate book id entries'''
    
    try:
        cursor.execute('''INSERT INTO book(id, title, author, qty) values(?,?,?,?)''',
                       (book[0], book[1], book[2], book[3]))
        db.commit()
    except Exception as error:
        db.rollback()
        print(error)

    return

def enter_book():
    '''User inputs new book information then uses insert_book function to add it to the table'''

    while True:
        try: # To catch non integer values entered
            book_id = int(input("Enter book ID: "))
            break
        except ValueError: 
            print("Please enter a valid integer code.")

    book_title = input("Enter book Title: ")
    book_author = input("Enter book Author: ")

    while True:
        try: # To catch non integer values entered
            book_qty = int(input("Enter book quantity: "))
            break
        except ValueError: 
            print("Please enter a valid integer qty.")

    insert_book([book_id, book_title, book_author, book_qty])
    return

def print_menu():
    ''' Menu Options display and returns menu selection'''

    choice = input('''Bookstore Menu
    1. Enter book
    2. Update Book
    3. Delete book
    4. Search books
    5. View all items
    0. Exit
    Enter choice: ''')
    return choice


def update_book():
    '''Update a book by selecting its ID.
    Option given user of which field to update. Then updates field based on entered value'''

    while True:
        try: # Catch non integer value. Gets id of book to update
            book_id = int(input("Enter book id to update: "))
            break
        except ValueError:
            print("Enter a valid book id")

    # Update Menu Selection
    print('''Select field to update: 
        1. Book id
        2. Book title
        3. Book author
        4. Book quantity''')
    
    while True: # For valid menu option
        book_field = input("Enter option: ")
        if book_field in ["1", "2", "3", "4"]:
            break
        else:
            print("Not a valid option, please try again")

    if book_field == "1": # Change a book ID
        while True:
            try: # To catch non integer value
                new_id = int(input("Enter new book id: "))
                break
            except ValueError:
                print("Error: Enter valid id type!")
        try:
            cursor.execute('''UPDATE book SET id = ? WHERE id = ?''', (new_id,book_id))
            db.commit()
        except Exception as error:
            db.rollback()
            print(error)

    elif book_field == "2": # Change book Title
        new_title = input("Enter new book title: ")
        try:
            cursor.execute('''UPDATE book SET title = ? WHERE id = ?''', (new_title,book_id))
            db.commit()
        except Exception as error:
            db.rollback()
            print(error)

    elif book_field == "3": # Change book Author
        new_author = input("Enter new book author: ")
        try:
            cursor.execute('''UPDATE book SET author = ? WHERE id = ?''', (new_author,book_id))
            db.commit()
        except Exception as error:
            db.rollback()
            print(error)

    elif book_field == "4": # Change book Quantity
        while True:
            try: # Catch non integer value
                new_qty = int(input("Enter new book quantity: "))
                break
            except ValueError:
                print("Error: Enter valid qty type!")
        try:
            cursor.execute('''UPDATE book SET qty = ? WHERE id = ?''', (new_qty,book_id))
            db.commit()
        except Exception as error:
            db.rollback()
            print(error)    

    return


def delete_book():
    ''' Deletes a record after selecting a book record by the id'''

    while True:
        try:
            book_id = int(input("Enter book id to delete: "))
            break
        except ValueError:
            print("Enter a valid book id")

    try:
        cursor.execute('''DELETE FROM book WHERE id=?''', (book_id,))
        db.commit()
    except Exception as error:
        print(error)

    return


def search_book():
    ''' Search for books based on the different field options'''

    # Search menu options
    print('''Select option to search by:
        1. Book id
        2. Book title
        3. Book author''')
    
    while True:
        book_field = input("Enter option: ")
        if book_field in ["1", "2", "3"]:
            break
        else:
            print("Not a valid option, please try again")

    if book_field == "1": # Searches for a book by id
        while True:
            try:
                new_id = int(input("Enter book id: "))
                break
            except ValueError:
                print("Error: Enter valid id type!")
        try:
            print(new_id)
            cursor.execute('''SELECT * FROM book WHERE id = ?''', (new_id,))
            view(cursor)
        except Exception as error:
                print(error)

    elif book_field == "2": # Searches for partial match in title. Force lowercase to compare.
        new_title = input("Enter book title or partial title: ")
        try:
            cursor.execute('''SELECT * FROM book WHERE LOWER(title) LIKE ?''', ('%'+new_title.lower()+'%',))
            view(cursor)
        except Exception as error:
            print(error)

    elif book_field == "3": # Searches for partial match in author. Force lowercase to compare.
        new_author = input("Enter book author search term: ")
        try:
           cursor.execute('''SELECT * FROM book WHERE LOWER(author) LIKE ?''', ('%'+new_author.lower()+'%',))
           view(cursor)
        except Exception as error:
            print(error) 

    return

def view_all():
    ''' Vvew entire table. Initially made to check whole table after changes made'''
    cursor.execute('''SELECT * FROM book''')
    view(cursor)

# MAIN PROGRAM
option = ""
init_db()
while option != "0":
    option = print_menu()
    if option == "1":
        enter_book()
    elif option == "2":
        update_book()
    elif option == "3":
        delete_book()
    elif option == "4":    
        search_book()
    elif option == "5":    
        view_all()
    else:
        print("Not a valid option. Please try another.")

db.close()



