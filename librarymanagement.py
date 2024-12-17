import os
import datetime

def load_books(filename):
    books = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                book_id, title, author, quantity = line.strip().split("|")
                books.append({
                    "book_id": int(book_id),
                    "title": title,
                    "author": author,
                    "quantity": int(quantity)
                })
    return books

def save_books(filename, books):
    with open(filename, "w") as f:
        for book in books:
            f.write(f"{book['book_id']}|{book['title']}|{book['author']}|{book['quantity']}\n")

def load_users(filename):
    users = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                user_id, username, password, role, borrowed_books = parts[0], parts[1], parts[2], parts[3], parts[4]
                borrowed_books = [int(book_id) for book_id in borrowed_books.split(",") if book_id]
                users.append({
                    "user_id": int(user_id),
                    "username": username,
                    "password": password,
                    "role": role,
                    "borrowed_books": borrowed_books
                })
    return users

def save_users(filename, users):
    with open(filename, "w") as f:
        for user in users:
            borrowed_books = ",".join(map(str, user["borrowed_books"]))
            f.write(f"{user['user_id']}|{user['username']}|{user['password']}|{user['role']}|{borrowed_books}\n")

def add_book(books, book_id, title, author, quantity):
    books.append({"book_id": book_id, "title": title, "author": author, "quantity": quantity})

def remove_book(books, book_id):
    return [book for book in books if book["book_id"] != book_id]

def search_books(books, title=None, author=None):
    return [
        book for book in books
        if (title and title.lower() in book["title"].lower()) or (author and author.lower() in book["author"].lower())
    ]

def register_user(users, user_id, username, password, role="member"):
    users.append({"user_id": user_id, "username": username, "password": password, "role": role, "borrowed_books": []})

def authenticate_user(users, username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def borrow_book(books, users, user, book_id):
    for book in books:
        if book["book_id"] == book_id and book["quantity"] > 0:
            user["borrowed_books"].append(book_id)
            book["quantity"] -= 1
            return True
    return False

def return_book(books, users, user, book_id):
    if book_id in user["borrowed_books"]:
        user["borrowed_books"].remove(book_id)
        for book in books:
            if book["book_id"] == book_id:
                book["quantity"] += 1
                return True
    return False

def reserve_book(reservations, user, book_id):
    if book_id not in reservations:
        reservations[book_id] = []
    reservations[book_id].append(user["user_id"])
    return True

def process_reservations(reservations, book_id):
    if book_id in reservations and reservations[book_id]:
        return reservations[book_id].pop(0)
    return None

def calculate_fine(borrow_date, due_days=14, daily_fine=1):
    today = datetime.date.today()
    borrow_date = datetime.datetime.strptime(borrow_date, "%Y-%m-%d").date()
    overdue_days = (today - borrow_date).days - due_days
    return max(0, overdue_days * daily_fine)

def view_user_statistics(users, books):
    print("\nUser Statistics:")
    for user in users:
        print(f"User: {user['username']} (Role: {user['role']})")
        print(f"  Borrowed Books: {len(user['borrowed_books'])}")
        for book_id in user["borrowed_books"]:
            for book in books:
                if book["book_id"] == book_id:
                    print(f"    - {book['title']} (ID: {book_id})")

def most_borrowed_books(users, books):
    borrow_counts = {book["book_id"]: 0 for book in books}
    for user in users:
        for book_id in user["borrowed_books"]:
            borrow_counts[book_id] += 1

    sorted_books = sorted(borrow_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nMost Borrowed Books:")
    for book_id, count in sorted_books[:5]:
        for book in books:
            if book["book_id"] == book_id:
                print(f"{book['title']} by {book['author']} - Borrowed {count} times")

def admin_remove_user(users, user_id):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            print(f"User ID {user_id} removed successfully.")
            return True
    print(f"User ID {user_id} not found.")
    return False

def clear_fines():
    print("Cleared all fines for the library system.")

def get_overdue_books(user):
    return user["borrowed_books"]

def generate_report(books, users):
    print("Library Report:")
    print(f"Total Books: {len(books)}")
    print(f"Total Users: {len(users)}")
    print("Books in Inventory:")
    for book in books:
        print(f"{book['title']} by {book['author']} (ID: {book['book_id']}) - {book['quantity']} available")
    print("Users List:")
    for user in users:
        print(f"User {user['username']} ({user['role']})")
        for book_id in user["borrowed_books"]:
            print(f"  Borrowed Book ID: {book_id}")

def main():
    books_file = "books.txt"
    users_file = "users.txt"

    books = load_books(books_file)
    users = load_users(users_file)
    reservations = {}

    if not users:
        register_user(users, 1, "admin", "admin123", role="admin")
        register_user(users, 2, "john_doe", "password123")

    if not books:
        add_book(books, 101, "The Tiger King", "F. Scott Fitzgerald", 5)
        add_book(books, 102, "1984", "George Orwell", 3)

    print("Welcome to the Library Management System!")
    print("Created by Naitik Udaywal and Assisted by Krishna Singh")

    username = input("Enter username: ")
    password = input("Enter password: ")
    user = authenticate_user(users, username, password)

    if not user:
        print("Invalid username or password.")
        return

    print(f"Welcome, {user['username']}!")

    while True:
        print("\n1. Search Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Reserve Book")
        print("5. View Overdue Books & Fines")
        print("6. View User Statistics")
        print("7. Most Borrowed Books")
        print("8. Remove User (Admin Only)")
        print("9. Clear Fines (Admin Only)")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter title to search: ")
            author = input("Enter author to search: ")
            results = search_books(books, title=title, author=author)
            if results:
                for book in results:
                    print(f"Found: {book['title']} by {book['author']} (ID: {book['book_id']})")
            else:
                print("No books found.")

        elif choice == "2":
            book_id = int(input("Enter Book ID to borrow: "))
            borrow_date = datetime.date.today().strftime("%Y-%m-%d")
            if borrow_book(books, users, user, book_id):
                print(f"You've borrowed the book successfully on {borrow_date}.")
            else:
                print("Book unavailable or doesn't exist.")

        elif choice == "3":
            book_id = int(input("Enter Book ID to return: "))
            if return_book(books, users, user, book_id):
                print("Book returned successfully.")
                next_user = process_reservations(reservations, book_id)
                if next_user:
                    print(f"Notification: User ID {next_user} can now borrow the book.")
            else:
                print("Error in returning book.")

        elif choice == "4":
            book_id = int(input("Enter Book ID to reserve: "))
            if reserve_book(reservations, user, book_id):
                print("Book reserved successfully.")
            else:
                print("Error in reserving book.")

        elif choice == "5":
            overdue_ids = get_overdue_books(user)
            if overdue_ids:
                total_fine = 0
                print("Overdue Books and Fines:")
                for book_id in overdue_ids:
                    for book in books:
                        if book["book_id"] == book_id:
                            fine = calculate_fine("2023-12-01")  # Example borrow date
                            total_fine += fine
                            print(f"{book['title']} by {book['author']} - Fine: ${fine}")
                print(f"Total Fine: ${total_fine}")
            else:
                print("No overdue books.")

        elif choice == "6":
            view_user_statistics(users, books)

        elif choice == "7":
            most_borrowed_books(users, books)

        elif choice == "8" and user["role"] == "admin":
            user_id = int(input("Enter User ID to remove: "))
            admin_remove_user(users, user_id)

        elif choice == "9" and user["role"] == "admin":
            clear_fines()

        elif choice == "10":
            save_books(books_file, books)
            save_users(users_file, users)
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
