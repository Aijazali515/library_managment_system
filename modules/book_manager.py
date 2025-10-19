import datetime
from utils import load_data, save_data, generate_id, BOOKS_FILE, MEMBERS_FILE

BOOK_FIELDNAMES = ['id', 'title', 'author', 'isbn', 'quantity', 'available']

def _get_books():
    """Helper to load books data."""
    return load_data(BOOKS_FILE)

def _save_books(books):
    """Helper to save books data."""
    save_data(BOOKS_FILE, books, BOOK_FIELDNAMES)

def add_new_book():
    """Adds a new book to the system."""
    books = _get_books()
    print("\n" + "="*40)
    print("           ADD NEW BOOK")
    print("="*40)
    
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()
    
    while True:
        try:
            quantity = int(input("Enter quantity: ").strip())
            if quantity < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid quantity. Please enter a non-negative number.")

    book_id = generate_id(books)
    new_book = {
        'id': book_id,
        'title': title,
        'author': author,
        'isbn': isbn,
        'quantity': str(quantity), # Store as string for CSV consistency
        'available': str(quantity) # Store as string
    }
    books.append(new_book)
    _save_books(books)
    print(f"\nBook '{title}' added successfully with ID: {book_id}.")
    print("="*40)

def display_all_books():
    """Displays all books in the library."""
    books = _get_books()
    print("\n" + "="*60)
    print("               ALL BOOKS IN LIBRARY")
    print("="*60)
    if not books:
        print("No books in the library.")
        return

    print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Qty':<5} {'Avail':<5}")
    print("-" * 60)
    for book in books:
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['isbn']:<15} {book['quantity']:<5} {book['available']:<5}")
    print("="*60)

def display_available_books():
    """Displays only the available books."""
    books = _get_books()
    print("\n" + "="*60)
    print("             AVAILABLE BOOKS IN LIBRARY")
    print("="*60)
    available_books = [b for b in books if int(b['available']) > 0]
    if not available_books:
        print("No books currently available.")
        return

    print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Avail':<5}")
    print("-" * 60)
    for book in available_books:
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['isbn']:<15} {book['available']:<5}")
    print("="*60)

def search_books():
    """Searches for books by title or author."""
    books = _get_books()
    print("\n" + "="*40)
    print("             SEARCH BOOKS")
    print("="*40)
    search_term = input("Enter title or author to search: ").strip().lower()
    
    found_books = [
        book for book in books 
        if search_term in book['title'].lower() or search_term in book['author'].lower()
    ]

    if not found_books:
        print(f"No books found matching '{search_term}'.")
        return

    print(f"\nBooks matching '{search_term}':")
    print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Qty':<5} {'Avail':<5}")
    print("-" * 60)
    for book in found_books:
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['isbn']:<15} {book['quantity']:<5} {book['available']:<5}")
    print("="*60)

def borrow_a_book():
    """Handles borrowing a book."""
    books = _get_books()
    members = load_data(MEMBERS_FILE)

    print("\n" + "="*40)
    print("             BORROW A BOOK")
    print("="*40)

    if not books:
        print("No books in the library to borrow.")
        return
    if not members:
        print("No registered members to borrow books.")
        return

    member_id = input("Enter Member ID: ").strip()
    member = next((m for m in members if m['id'] == member_id), None)

    if not member:
        print(f"Member with ID '{member_id}' not found.")
        return

    book_id = input("Enter Book ID: ").strip()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        print(f"Book with ID '{book_id}' not found.")
        return

    if int(book['available']) <= 0:
        print(f"Book '{book['title']}' is currently out of stock.")
        return
    
    # Update book availability
    book['available'] = str(int(book['available']) - 1)

    # Update member's borrowed books
    if 'borrowed_books' not in member:
        member['borrowed_books'] = []
    else:
        # Convert string representation of list back to list
        # This is a bit hacky for CSV, better to have a separate borrowing log
        # For simplicity, we'll assume it's a string representation of a list of book_id:borrow_date
        if isinstance(member['borrowed_books'], str) and member['borrowed_books']:
            member['borrowed_books'] = eval(member['borrowed_books'])
        elif not member['borrowed_books']:
             member['borrowed_books'] = []

    borrow_date = datetime.date.today().isoformat()
    member['borrowed_books'].append(f"{book_id}:{borrow_date}")
    
    # Convert list back to string for CSV storage
    member['borrowed_books'] = str(member['borrowed_books'])
    
    _save_books(books)
    save_data(MEMBERS_FILE, members, ['id', 'name', 'contact', 'borrowed_books']) # Ensure all member fields are saved

    print(f"\nBook '{book['title']}' borrowed by '{member['name']}' successfully.")
    print("New available quantity: ", book['available'])
    print("="*40)


def return_a_book():
    """Handles returning a book."""
    books = _get_books()
    members = load_data(MEMBERS_FILE)

    print("\n" + "="*40)
    print("             RETURN A BOOK")
    print("="*40)

    if not books:
        print("No books in the library.")
        return
    if not members:
        print("No registered members.")
        return

    member_id = input("Enter Member ID: ").strip()
    member = next((m for m in members if m['id'] == member_id), None)

    if not member:
        print(f"Member with ID '{member_id}' not found.")
        return
    
    # Handle the 'borrowed_books' string representation
    borrowed_books_list = []
    if 'borrowed_books' in member and isinstance(member['borrowed_books'], str) and member['borrowed_books']:
        try:
            borrowed_books_list = eval(member['borrowed_books'])
        except (SyntaxError, NameError):
            print("Error: Could not parse member's borrowed books data.")
            member['borrowed_books'] = [] # Reset to empty list if parsing fails
            borrowed_books_list = []

    if not borrowed_books_list:
        print(f"Member '{member['name']}' has no borrowed books.")
        return

    print("\n" + "="*40)
    print(f"Borrowed books by {member['name']} (ID: {member_id}):")
    
    display_member_borrowed_books(member_id)

    book_id_to_return = input("Enter Book ID to return: ").strip()
    
    book_entry_to_remove = None
    for entry in borrowed_books_list:
        if entry.startswith(f"{book_id_to_return}:"):
            book_entry_to_remove = entry
            break

    if not book_entry_to_remove:
        print(f"Book with ID '{book_id_to_return}' was not found in {member['name']}'s borrowed list.")
        return

    book = next((b for b in books if b['id'] == book_id_to_remove), None)

    if not book:
        print(f"Book with ID '{book_id_to_return}' not found in library inventory. (Data inconsistency)")
        return
    
    # Remove from member's list
    borrowed_books_list.remove(book_entry_to_remove)
    member['borrowed_books'] = str(borrowed_books_list) # Save back as string

    # Increase book availability
    book['available'] = str(int(book['available']) + 1)
    
    _save_books(books)
    save_data(MEMBERS_FILE, members, ['id', 'name', 'contact', 'borrowed_books']) # Ensure all member fields are saved

    print(f"\nBook '{book['title']}' returned by '{member['name']}' successfully.")
    print("New available quantity: ", book['available'])
    print("="*40)

def view_overdue_books():
    """Displays books that are overdue (e.g., borrowed more than 14 days ago)."""
    books = _get_books()
    members = load_data(MEMBERS_FILE)
    
    print("\n" + "="*60)
    print("                OVERDUE BOOKS REPORT")
    print("="*60)

    overdue_found = False
    today = datetime.date.today()
    borrow_duration_limit = datetime.timedelta(days=14) # Example: 14 days limit

    print(f"{'Member ID':<10} {'Member Name':<20} {'Book Title':<30} {'Borrowed Date':<15} {'Overdue By (days)':<20}")
    print("-" * 100)

    for member in members:
        borrowed_books_list = []
        if 'borrowed_books' in member and isinstance(member['borrowed_books'], str) and member['borrowed_books']:
            try:
                borrowed_books_list = eval(member['borrowed_books'])
            except (SyntaxError, NameError):
                pass # Skip if data is malformed

        for entry in borrowed_books_list:
            try:
                book_id, borrow_date_str = entry.split(':')
                borrow_date = datetime.date.fromisoformat(borrow_date_str)
                
                if today - borrow_date > borrow_duration_limit:
                    book = next((b for b in books if b['id'] == book_id), None)
                    if book:
                        overdue_by_days = (today - borrow_date - borrow_duration_limit).days
                        print(f"{member['id']:<10} {member['name']:<20} {book['title']:<30} {borrow_date_str:<15} {overdue_by_days:<20}")
                        overdue_found = True
            except (ValueError, IndexError):
                # Handle malformed entry in borrowed_books
                pass

    if not overdue_found:
        print("No overdue books found.")
    print("="*100)

def display_member_borrowed_books(member_id):
    """Internal function to display a specific member's borrowed books."""
    books = _get_books()
    members = load_data(MEMBERS_FILE)

    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        print(f"Member with ID '{member_id}' not found.")
        return

    borrowed_books_list = []
    if 'borrowed_books' in member and isinstance(member['borrowed_books'], str) and member['borrowed_books']:
        try:
            borrowed_books_list = eval(member['borrowed_books'])
        except (SyntaxError, NameError):
            print("Error: Could not parse member's borrowed books data.")
            return

    if not borrowed_books_list:
        print(f"Member '{member['name']}' has no books currently borrowed.")
        return

    print(f"{'Book ID':<10} {'Title':<30} {'Author':<20} {'Borrowed Date':<15}")
    print("-" * 75)
    
    for entry in borrowed_books_list:
        try:
            book_id, borrow_date_str = entry.split(':')
            book = next((b for b in books if b['id'] == book_id), None)
            if book:
                print(f"{book['id']:<10} {book['title']:<30} {book['author']:<20} {borrow_date_str:<15}")
        except (ValueError, IndexError):
            # Skip malformed entries
            pass
    print("-" * 75)

