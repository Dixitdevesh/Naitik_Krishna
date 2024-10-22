import csv

LIBRARY_NAME = "City Library"
BOOKS_FILE = 'books.csv'

def add_book():
    book_id = input("Enter book ID: ")
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    genre = input("Enter genre: ")
    quantity = int(input("Enter quantity: "))
    
    with open(BOOKS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([book_id, title, author, genre, quantity])
    print(f"Book '{title}' added successfully.")

def view_books():
    try:
        with open(BOOKS_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            print("\n{:<10} {:<50} {:<30} {:<20} {:<10}".format('ID', 'Title', 'Author', 'Genre', 'Quantity'))
            print("=" * 120)
            for row in reader:
                print("{:<10} {:<50} {:<30} {:<20} {:<10}".format(
                    row['ID'], row['Title'], row['Author'], row['Genre'], row['Quantity']
                ))
            print("=" * 120)
    except FileNotFoundError:
        print("Books file not found. Please add books directly in the CSV file.")

def update_book():
    book_id = input("Enter book ID to update: ")
    found = False

    try:
        with open(BOOKS_FILE, mode='r') as file:
            reader = list(csv.DictReader(file))
        
        for row in reader:
            if row['ID'] == book_id:
                found = True
                row['Title'] = input(f"Enter new title (current: {row['Title']}): ") or row['Title']
                row['Author'] = input(f"Enter new author (current: {row['Author']}): ") or row['Author']
                row['Genre'] = input(f"Enter new genre (current: {row['Genre']}): ") or row['Genre']
                row['Quantity'] = input(f"Enter new quantity (current: {row['Quantity']}): ") or row['Quantity']
        
        if found:
            with open(BOOKS_FILE, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(reader)
            print("Book updated successfully.")
        else:
            print("Book not found.")
    except FileNotFoundError:
        print("Books file not found. Please add books directly in the CSV file.")

def delete_book():
    book_id = input("Enter book ID to delete: ")
    found = False

    try:
        with open(BOOKS_FILE, mode='r') as file:
            reader = list(csv.DictReader(file))

        for row in reader:
            if row['ID'] == book_id:
                found = True
                reader.remove(row)
                print("Book deleted successfully.")
        
        if found:
            with open(BOOKS_FILE, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(reader)
        else:
            print("Book not found.")
    except FileNotFoundError:
        print("Books file not found. Please add books directly in the CSV file.")

def borrow_book():
    book_id = input("Enter book ID to borrow: ")
    found = False

    try:
        with open(BOOKS_FILE, mode='r') as file:
            reader = list(csv.DictReader(file))
        
        for row in reader:
            if row['ID'] == book_id:
                found = True
                if int(row['Quantity']) > 0:
                    row['Quantity'] = int(row['Quantity']) - 1
                    print(f"You have borrowed '{row['Title']}'.")
                else:
                    print("Sorry, this book is currently unavailable.")

        if found:
            with open(BOOKS_FILE, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(reader)
        else:
            print("Book not found.")
    except FileNotFoundError:
        print("Books file not found. Please add books directly in the CSV file.")

def main():
    while True:
        print("\nWelcome to", LIBRARY_NAME)
        print("1. Add Book")
        print("2. View Books")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Borrow Book")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            borrow_book()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
