from utils import load_data, BOOKS_FILE, MEMBERS_FILE
import datetime

def generate_library_report():
    """Generates a comprehensive library report."""
    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)

    print("\n" + "="*80)
    print("                       LIBRARY REPORT")
    print("="*80)

    # --- Book Summary ---
    total_books = len(books)
    total_quantity = sum(int(b.get('quantity', '0')) for b in books)
    total_available = sum(int(b.get('available', '0')) for b in books)
    total_borrowed = total_quantity - total_available

    print("\n--- Book Summary ---")
    print(f"Total Unique Books: {total_books}")
    print(f"Total Book Copies: {total_quantity}")
    print(f"Total Available Books: {total_available}")
    print(f"Total Books Currently Borrowed: {total_borrowed}")
    print("-" * 80)

    # --- Member Summary ---
    total_members = len(members)
    members_with_borrowed_books = 0
    total_books_borrowed_across_members = 0
    
    for member in members:
        borrowed_books_list = []
        if 'borrowed_books' in member and isinstance(member['borrowed_books'], str) and member['borrowed_books']:
            try:
                borrowed_books_list = eval(member['borrowed_books'])
                if borrowed_books_list:
                    members_with_borrowed_books += 1
                    total_books_borrowed_across_members += len(borrowed_books_list)
            except (SyntaxError, NameError):
                pass

    print("\n--- Member Summary ---")
    print(f"Total Registered Members: {total_members}")
    print(f"Members with Books Currently Borrowed: {members_with_borrowed_books}")
    print(f"Total Books Borrowed (counting multiple books per member): {total_books_borrowed_across_members}")
    print("-" * 80)

    # --- Overdue Books (Detailed) ---
    print("\n--- Overdue Books ---")
    overdue_found = False
    today = datetime.date.today()
    borrow_duration_limit = datetime.timedelta(days=14) 

    overdue_books_list = []

    for member in members:
        borrowed_books_list = []
        if 'borrowed_books' in member and isinstance(member['borrowed_books'], str) and member['borrowed_books']:
            try:
                borrowed_books_list = eval(member['borrowed_books'])
            except (SyntaxError, NameError):
                pass 

        for entry in borrowed_books_list:
            try:
                book_id, borrow_date_str = entry.split(':')
                borrow_date = datetime.date.fromisoformat(borrow_date_str)
                
                if today - borrow_date > borrow_duration_limit:
                    book = next((b for b in books if b['id'] == book_id), None)
                    if book:
                        overdue_by_days = (today - borrow_date - borrow_duration_limit).days
                        overdue_books_list.append({
                            'member_id': member['id'],
                            'member_name': member['name'],
                            'book_title': book['title'],
                            'borrowed_date': borrow_date_str,
                            'overdue_by_days': overdue_by_days
                        })
                        overdue_found = True
            except (ValueError, IndexError):
                pass

    if overdue_found:
        print(f"{'Member ID':<10} {'Member Name':<20} {'Book Title':<30} {'Borrowed Date':<15} {'Overdue By (days)':<20}")
        print("-" * 100)
        for overdue_book in overdue_books_list:
            print(f"{overdue_book['member_id']:<10} {overdue_book['member_name']:<20} {overdue_book['book_title']:<30} {overdue_book['borrowed_date']:<15} {overdue_book['overdue_by_days']:<20}")
    else:
        print("No overdue books found.")
    print("="*80)

