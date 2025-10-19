from utils import load_data, save_data, generate_id, BOOKS_FILE, MEMBERS_FILE
import modules.book_manager as bm

MEMBER_FIELDNAMES = ['id', 'name', 'contact', 'borrowed_books'] # borrowed_books will store a string representation of a list

def _get_members():
    """Helper to load members data."""
    return load_data(MEMBERS_FILE)

def _save_members(members):
    """Helper to save members data."""
    save_data(MEMBERS_FILE, members, MEMBER_FIELDNAMES)

def register_new_member():
    """Registers a new member to the system."""
    members = _get_members()
    print("\n" + "="*40)
    print("          REGISTER NEW MEMBER")
    print("="*40)
    
    name = input("Enter member name: ").strip()
    contact = input("Enter contact information (e.g., email or phone): ").strip()
    
    member_id = generate_id(members)
    new_member = {
        'id': member_id,
        'name': name,
        'contact': contact,
        'borrowed_books': '[]' # Initialize as empty list string
    }
    members.append(new_member)
    _save_members(members)
    print(f"\nMember '{name}' registered successfully with ID: {member_id}.")
    print("="*40)

def display_all_members():
    """Displays all registered members."""
    members = _get_members()
    print("\n" + "="*70)
    print("                   ALL REGISTERED MEMBERS")
    print("="*70)
    if not members:
        print("No members registered yet.")
        return

    print(f"{'ID':<5} {'Name':<30} {'Contact':<25}")
    print("-" * 70)
    for member in members:
        print(f"{member['id']:<5} {member['name']:<30} {member['contact']:<25}")
    print("="*70)

def view_member_borrowed_books():
    """Allows viewing books borrowed by a specific member."""
    members = _get_members()
    print("\n" + "="*40)
    print("         VIEW MEMBER'S BORROWED BOOKS")
    print("="*40)

    if not members:
        print("No members registered yet.")
        return

    member_id = input("Enter Member ID: ").strip()
    bm.display_member_borrowed_books(member_id)
    print("="*40)

