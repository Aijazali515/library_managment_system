import os
import modules.book_manager as bm
import modules.member_manager as mm
import modules.report_manager as rm
from utils import ensure_data_dir_exists # Import the function to create data dir


def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Displays the main menu of the Library Management System."""
    clear_screen()
    print("=" * 40)
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Display All Books")
    print("2. Display Available Books")
    print("3. Display All Members")
    print("4. Search Books")
    print("5. Borrow a Book")
    print("6. Return a Book")
    print("7. View Member's Borrowed Books")
    print("8. View Overdue Books")
    print("9. Library Report")
    print("10. Add New Book")
    print("11. Register New Member")
    print("0. Exit")
    print("=" * 40)

def main():
    """Main function to run the Library Management System."""
    ensure_data_dir_exists() # Ensure data directory exists on startup
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-11): ").strip()

        if choice == '1':
            bm.display_all_books()
        elif choice == '2':
            bm.display_available_books()
        elif choice == '3':
            mm.display_all_members()
        elif choice == '4':
            bm.search_books()
        elif choice == '5':
            bm.borrow_a_book()
        elif choice == '6':
            bm.return_a_book()
        elif choice == '7':
            mm.view_member_borrowed_books()
        elif choice == '8':
            bm.view_overdue_books()
        elif choice == '9':
            rm.generate_library_report()
        elif choice == '10':
            bm.add_new_book()
        elif choice == '11':
            mm.register_new_member()
        elif choice == '0':
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 11.")
        
        input("\nPress Enter to continue...") # Pause for user to read output

if __name__ == "__main__":
    main()

