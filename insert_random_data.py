import sqlite3
import random
from datetime import datetime, timedelta

# Lists for generating random data
room_types = ['Meeting Room', 'Office', 'Lab', 'Conference Hall', 'Break Room', 'Study Room', 'Training Room', 'Auditorium']
room_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega', 'Sigma', 'Phoenix', 'Dragon', 'Eagle', 'Lion']
first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Oliver', 'Isabella', 'William', 'Sophia', 'James', 
               'Charlotte', 'Benjamin', 'Mia', 'Lucas', 'Harper', 'Henry', 'Evelyn', 'Theodore', 'Elizabeth']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson']
roles = ['Facility Manager', 'Maintenance Supervisor', 'Room Coordinator', 'IT Specialist', 'Security Officer',
         'Cleaning Supervisor', 'Operations Manager', 'Administrative Assistant', 'Building Engineer']
task_descriptions = [
    'Regular maintenance check',
    'Deep cleaning required',
    'Update security system',
    'Replace light fixtures',
    'Install new equipment',
    'Paint walls',
    'Fix broken furniture',
    'Update room signage',
    'Install new blinds',
    'Check air conditioning',
    'Repair door lock',
    'Replace carpet',
    'Install new speakers',
    'Set up video conferencing',
    'Replace chairs',
    'Fix ceiling tiles',
    'Update room schedule display',
    'Install new whiteboard',
    'Check electrical outlets',
    'Clean air vents'
]

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def insert_random_data():
    conn = sqlite3.connect('facility_management.db')
    cursor = conn.cursor()

    # Clear existing sample data
    cursor.execute("DELETE FROM tasks")
    cursor.execute("DELETE FROM rooms")
    cursor.execute("DELETE FROM people")

    # Reset auto-increment counters
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('tasks', 'rooms', 'people')")

    # Insert random rooms (30 rooms)
    for floor in range(1, 6):  # 5 floors
        for room in range(1, 7):  # 6 rooms per floor
            room_number = f"{floor}0{room}"
            room_name = f"{random.choice(room_types)} {random.choice(room_names)}"
            capacity = random.randint(4, 50)
            cursor.execute('''
            INSERT INTO rooms (room_number, room_name, floor, capacity)
            VALUES (?, ?, ?, ?)
            ''', (room_number, room_name, floor, capacity))

    # Insert random people (20 people)
    for _ in range(20):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name.lower().replace(' ', '.')}@example.com"
        phone = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        role = random.choice(roles)
        try:
            cursor.execute('''
            INSERT INTO people (full_name, email, phone, role)
            VALUES (?, ?, ?, ?)
            ''', (full_name, email, phone, role))
        except sqlite3.IntegrityError:
            continue  # Skip if email already exists

    # Get all room_ids and person_ids for reference
    cursor.execute("SELECT room_id FROM rooms")
    room_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT person_id FROM people")
    person_ids = [row[0] for row in cursor.fetchall()]

    # Insert random tasks (50 tasks)
    start_date = datetime.now() - timedelta(days=30)  # Tasks starting from 30 days ago
    end_date = datetime.now() + timedelta(days=90)    # Tasks up to 90 days in the future

    for _ in range(50):
        room_id = random.choice(room_ids)
        person_id = random.choice(person_ids)
        description = random.choice(task_descriptions)
        progress = random.choice([0, 25, 50, 75, 100])
        status = random.choice(['pending', 'in_progress', 'completed'])
        
        task_start_date = generate_random_date(start_date, end_date)
        task_due_date = task_start_date + timedelta(days=random.randint(1, 30))

        cursor.execute('''
        INSERT INTO tasks (room_id, person_id, description, progress, status, start_date, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (room_id, person_id, description, progress, status, task_start_date, task_due_date))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_random_data()
    print("Random data has been successfully inserted into the database!") 