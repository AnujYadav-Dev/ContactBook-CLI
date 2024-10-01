import sqlite3

# Create and connect to the SQLite database
db_connection = sqlite3.connect('contact_book_terminal.db')
db_cursor = db_connection.cursor()

# Create a table if it doesn't exist
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
''')
db_connection.commit()

# Function to add a new contact
def add_new_contact():
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email (optional): ").strip()
    address = input("Enter Address (optional): ").strip()
    
    if name and phone:
        db_cursor.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)',
                          (name, phone, email, address))
        db_connection.commit()
        print("\nContact added successfully!")
    else:
        print("\nError: Name and Phone are required fields.")

# Function to display all contacts
def display_all_contacts():
    db_cursor.execute('SELECT id, name, phone, email, address FROM contacts')
    contacts = db_cursor.fetchall()
    
    if contacts:
        print("\nList of Contacts:")
        print("{:<5} {:<20} {:<15} {:<30} {:<30}".format("ID", "Name", "Phone", "Email", "Address"))
        print("-" * 100)
        for contact in contacts:
            print("{:<5} {:<20} {:<15} {:<30} {:<30}".format(contact[0], contact[1], contact[2], contact[3], contact[4]))
    else:
        print("\nNo contacts found.")

# Function to search for a contact by name or phone number
def search_contact():
    search_term = input("Enter name or phone number to search: ").strip()
    
    if search_term:
        db_cursor.execute('SELECT id, name, phone, email, address FROM contacts WHERE name LIKE ? OR phone LIKE ?', 
                          ('%' + search_term + '%', '%' + search_term + '%'))
        results = db_cursor.fetchall()
        
        if results:
            print("\nSearch Results:")
            print("{:<5} {:<20} {:<15} {:<30} {:<30}".format("ID", "Name", "Phone", "Email", "Address"))
            print("-" * 100)
            for contact in results:
                print("{:<5} {:<20} {:<15} {:<30} {:<30}".format(contact[0], contact[1], contact[2], contact[3], contact[4]))
        else:
            print("\nNo contacts found with that search term.")
    else:
        print("\nError: Search term cannot be empty.")

# Function to update a contact
def update_contact():
    try:
        contact_id = int(input("Enter the Contact ID to update: ").strip())
        db_cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        contact = db_cursor.fetchone()
        
        if contact:
            print("\nLeave fields blank if you do not want to change them.")
            new_name = input(f"Enter new name [{contact[1]}]: ").strip() or contact[1]
            new_phone = input(f"Enter new phone [{contact[2]}]: ").strip() or contact[2]
            new_email = input(f"Enter new email [{contact[3]}]: ").strip() or contact[3]
            new_address = input(f"Enter new address [{contact[4]}]: ").strip() or contact[4]
            
            db_cursor.execute('''
                UPDATE contacts SET name=?, phone=?, email=?, address=?
                WHERE id=?
            ''', (new_name, new_phone, new_email, new_address, contact_id))
            db_connection.commit()
            print("\nContact updated successfully!")
        else:
            print("\nError: Contact not found.")
    except ValueError:
        print("\nError: Please enter a valid Contact ID.")

# Function to delete a contact
def delete_contact():
    try:
        contact_id = int(input("Enter the Contact ID to delete: ").strip())
        db_cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        contact = db_cursor.fetchone()
        
        if contact:
            confirmation = input(f"Are you sure you want to delete contact '{contact[1]}'? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                db_cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
                db_connection.commit()
                print("\nContact deleted successfully!")
            else:
                print("\nDeletion cancelled.")
        else:
            print("\nError: Contact not found.")
    except ValueError:
        print("\nError: Please enter a valid Contact ID.")

# Function to display the menu
def display_menu():
    print("\n--- Contact Book Menu ---")
    print("1. Add New Contact")
    print("2. View All Contacts")
    print("3. Search Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

# Main loop to run the program
def run_contact_book():
    while True:
        display_menu()
        
        try:
            choice = int(input("\nChoose an option (1-6): ").strip())
            
            if choice == 1:
                add_new_contact()
            elif choice == 2:
                display_all_contacts()
            elif choice == 3:
                search_contact()
            elif choice == 4:
                update_contact()
            elif choice == 5:
                delete_contact()
            elif choice == 6:
                print("\nExiting Contact Book. Goodbye!")
                break
            else:
                print("\nInvalid option. Please choose a number between 1 and 6.")
        
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

# Start the Contact Book application
run_contact_book()

# Close the database connection when the program exits
db_connection.close()
