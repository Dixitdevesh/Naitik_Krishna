import os
import datetime

library_file = 'library.txt'
user_file = 'users.txt'
borrowed_file = 'borrowed.txt'
fine_rate = 5  # Fine rate per day for late returns

def initialize_files():
    if not os.path.exists(library_file):
        with open(library_file, 'w') as f:
            f.write('ID,Title,Author,Category,Status\n')
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            f.write('Username,Password\n')
    if not os.path.exists(borrowed_file):
        with open(borrowed_file, 'w') as f:
            f.write('BookID,Username,BorrowDate,DueDate\n')

def register_user():
    username = input('Enter new username: ')
    password = input('Enter new password: ')
    with open(user_file, 'a') as f:
        f.write(f'{username},{password}\n')
    print('User registered successfully!')

def login_user():
    username = input('Enter username: ')
    password = input('Enter password: ')
    with open(user_file, 'r') as f:
        users = f.readlines()
    for user in users:
        u, p = user.strip().split(',')
        if u == username and p == password:
            print('Login successful!')
            return username
    print('Invalid credentials.')
    return None

def display_books():
    with open(library_file, 'r') as f:
        books = f.readlines()
    for book in books:
        print(book.strip())

def add_book():
    book_id = input('Enter Book ID: ')
    title = input('Enter Book Title: ')
    author = input('Enter Book Author: ')
    category = input('Enter Book Category: ')
    status = 'Available'
    with open(library_file, 'a') as f:
        f.write(f'{book_id},{title},{author},{category},{status}\n')
    print('Book added successfully!')

def remove_book():
    book_id = input('Enter Book ID to remove: ')
    with open(library_file, 'r') as f:
        lines = f.readlines()
    with open(library_file, 'w') as f:
        for line in lines:
            if not line.startswith(book_id + ','):
                f.write(line)
    print('Book removed successfully!')

def borrow_book(username):
    book_id = input('Enter Book ID to borrow: ')
    with open(library_file, 'r') as f:
        lines = f.readlines()
    updated = False
    with open(library_file, 'w') as f:
        for line in lines:
            parts = line.strip().split(',')
            if parts[0] == book_id and parts[4] == 'Available':
                parts[4] = 'Borrowed'
                line = ','.join(parts) + '\n'
                borrow_date = datetime.date.today()
                due_date = borrow_date + datetime.timedelta(days=14)
                with open(borrowed_file, 'a') as bf:
                    bf.write(f'{book_id},{username},{borrow_date},{due_date}\n')
                updated = True
            f.write(line)
    if updated:
        print(f'Book borrowed successfully! Due date: {due_date}')
    else:
        print('Book is not available or does not exist.')

def return_book(username):
    book_id = input('Enter Book ID to return: ')
    with open(borrowed_file, 'r') as f:
        borrow_records = f.readlines()
    with open(borrowed_file, 'w') as f:
        returned = False
        for record in borrow_records:
            parts = record.strip().split(',')
            if parts[0] == book_id and parts[1] == username:
                borrow_date = datetime.datetime.strptime(parts[2], '%Y-%m-%d').date()
                due_date = datetime.datetime.strptime(parts[3], '%Y-%m-%d').date()
                return_date = datetime.date.today()
                if return_date > due_date:
                    late_days = (return_date - due_date).days
                    fine = late_days * fine_rate
                    print(f'Late return! Fine: ${fine}')
                else:
                    print('Book returned on time.')
                returned = True
            else:
                f.write(record)
    if returned:
        with open(library_file, 'r') as lf:
            lines = lf.readlines()
        with open(library_file, 'w') as lf:
            for line in lines:
                parts = line.strip().split(',')
                if parts[0] == book_id:
                    parts[4] = 'Available'
                    line = ','.join(parts) + '\n'
                lf.write(line)
        print('Book returned successfully!')
    else:
        print('No borrowed record found for this book.')

def search_book():
    keyword = input('Enter keyword to search (ID, Title, Author, or Category): ').lower()
    with open(library_file, 'r') as f:
        lines = f.readlines()
    found = False
    for line in lines:
        if keyword in line.lower():
            print(line.strip())
            found = True
    if not found:
        print('No book found with that keyword.')

def view_borrowed_books(username):
    with open(borrowed_file, 'r') as f:
        records = f.readlines()
    print(f'Borrowed books by {username}:')
    found = False
    for record in records:
        parts = record.strip().split(',')
        if parts[1] == username:
            print(f'Book ID: {parts[0]}, Borrow Date: {parts[2]}, Due Date: {parts[3]}')
            found = True
    if not found:
        print('No borrowed books.')

def view_fines(username):
    with open(borrowed_file, 'r') as f:
        records = f.readlines()
    total_fine = 0
    for record in records:
        parts = record.strip().split(',')
        if parts[1] == username:
            due_date = datetime.datetime.strptime(parts[3], '%Y-%m-%d').date()
            return_date = datetime.date.today()
            if return_date > due_date:
                late_days = (return_date - due_date).days
                total_fine += late_days * fine_rate
    if total_fine > 0:
        print(f'Total fine: ${total_fine}')
    else:
        print('No fines due.')

def main():
    initialize_files()
    user = None
    while True:
        print('\nLibrary Management System')
        print('1. Register')
        print('2. Login')
        print('3. Exit')
        choice = input('Enter choice: ')
        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                while True:
                    print(f'\nWelcome, {user}!')
                    print('1. Display Books')
                    print('2. Add Book')
                    print('3. Remove Book')
                    print('4. Borrow Book')
                    print('5. Return Book')
                    print('6. Search Book')
                    print('7. View Borrowed Books')
                    print('8. View Fines')
                    print('9. Logout')
                    sub_choice = input('Enter choice: ')
                    if sub_choice == '1':
                        display_books()
                    elif sub_choice == '2':
                        add_book()
                    elif sub_choice == '3':
                        remove_book()
                    elif sub_choice == '4':
                        borrow_book(user)
                    elif sub_choice == '5':
                        return_book(user)
                    elif sub_choice == '6':
                        search_book()
                    elif sub_choice == '7':
                        view_borrowed_books(user)
                    elif sub_choice == '8':
                        view_fines(user)
                    elif sub_choice == '9':
                        user = None
                        break
                    else:
                        print('Invalid choice.')
        elif choice == '3':
            print('Goodbye!')
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()
            
