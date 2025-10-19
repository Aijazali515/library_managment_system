import csv
import os

DATA_DIR = 'data'
BOOKS_FILE = os.path.join(DATA_DIR, 'books.csv')
MEMBERS_FILE = os.path.join(DATA_DIR, 'members.csv')

def ensure_data_dir_exists():
    """Ensures the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_data(file_path):
    """Loads data from a CSV file."""
    ensure_data_dir_exists()
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_data(file_path, data, fieldnames):
    """Saves data to a CSV file."""
    ensure_data_dir_exists()
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_id(data):
    """Generates a unique ID for new entries."""
    if not data:
        return "1"
    
    # Assuming IDs are numeric strings
    max_id = 0
    for item in data:
        try:
            current_id = int(item.get('id', '0'))
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            # Handle cases where 'id' might not be a valid integer
            pass
    return str(max_id + 1)

