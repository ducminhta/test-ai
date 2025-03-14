import sqlite3
from datetime import datetime

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('facility_management.db')
    cursor = conn.cursor()

    # Create rooms table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT NOT NULL,
        room_name TEXT,
        floor INTEGER,
        capacity INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create people table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        person_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create tasks table (for progress tracking)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        person_id INTEGER,
        description TEXT NOT NULL,
        progress INTEGER DEFAULT 0,  -- Progress in percentage (0-100)
        status TEXT DEFAULT 'pending',  -- pending, in_progress, completed
        start_date TIMESTAMP,
        due_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (room_id) REFERENCES rooms (room_id),
        FOREIGN KEY (person_id) REFERENCES people (person_id)
    )
    ''')

    # Insert some sample data
    # Sample rooms
    cursor.execute('''
    INSERT INTO rooms (room_number, room_name, floor, capacity)
    VALUES 
        ('101', 'Conference Room A', 1, 20),
        ('201', 'Meeting Room B', 2, 10),
        ('301', 'Workshop Space', 3, 30)
    ''')

    # Sample people
    cursor.execute('''
    INSERT INTO people (full_name, email, phone, role)
    VALUES 
        ('John Doe', 'john.doe@example.com', '123-456-7890', 'Facility Manager'),
        ('Jane Smith', 'jane.smith@example.com', '123-456-7891', 'Maintenance Supervisor'),
        ('Bob Wilson', 'bob.wilson@example.com', '123-456-7892', 'Room Coordinator')
    ''')

    # Sample tasks
    cursor.execute('''
    INSERT INTO tasks (room_id, person_id, description, progress, status, start_date, due_date)
    VALUES 
        (1, 1, 'Install new projector', 75, 'in_progress', datetime('now'), datetime('now', '+7 days')),
        (2, 2, 'Fix air conditioning', 100, 'completed', datetime('now', '-3 days'), datetime('now')),
        (3, 3, 'Set up workshop equipment', 0, 'pending', datetime('now', '+1 day'), datetime('now', '+14 days'))
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database created successfully with sample data!") 