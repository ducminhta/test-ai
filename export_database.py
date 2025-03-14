import sqlite3
from datetime import datetime

def export_database():
    conn = sqlite3.connect('facility_management.db')
    cursor = conn.cursor()
    
    with open('facility_management_export.txt', 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("FACILITY MANAGEMENT DATABASE EXPORT\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        # Export Rooms
        f.write("ROOMS\n")
        f.write("-" * 80 + "\n")
        cursor.execute('''
            SELECT room_id, room_number, room_name, floor, capacity, created_at
            FROM rooms
            ORDER BY floor, room_number
        ''')
        rooms = cursor.fetchall()
        for room in rooms:
            f.write(f"Room ID: {room[0]}\n")
            f.write(f"Room Number: {room[1]}\n")
            f.write(f"Name: {room[2]}\n")
            f.write(f"Floor: {room[3]}\n")
            f.write(f"Capacity: {room[4]} people\n")
            f.write(f"Created: {room[5]}\n")
            f.write("-" * 40 + "\n")

        # Export People
        f.write("\nPEOPLE\n")
        f.write("-" * 80 + "\n")
        cursor.execute('''
            SELECT person_id, full_name, email, phone, role, created_at
            FROM people
            ORDER BY full_name
        ''')
        people = cursor.fetchall()
        for person in people:
            f.write(f"Person ID: {person[0]}\n")
            f.write(f"Name: {person[1]}\n")
            f.write(f"Email: {person[2]}\n")
            f.write(f"Phone: {person[3]}\n")
            f.write(f"Role: {person[4]}\n")
            f.write(f"Created: {person[5]}\n")
            f.write("-" * 40 + "\n")

        # Export Tasks
        f.write("\nTASKS\n")
        f.write("-" * 80 + "\n")
        cursor.execute('''
            SELECT t.task_id, r.room_number, r.room_name, p.full_name, 
                   t.description, t.progress, t.status, 
                   t.start_date, t.due_date, t.created_at
            FROM tasks t
            JOIN rooms r ON t.room_id = r.room_id
            JOIN people p ON t.person_id = p.person_id
            ORDER BY t.status, t.due_date
        ''')
        tasks = cursor.fetchall()
        for task in tasks:
            f.write(f"Task ID: {task[0]}\n")
            f.write(f"Room: {task[1]} - {task[2]}\n")
            f.write(f"Assigned to: {task[3]}\n")
            f.write(f"Description: {task[4]}\n")
            f.write(f"Progress: {task[5]}%\n")
            f.write(f"Status: {task[6]}\n")
            f.write(f"Start Date: {task[7]}\n")
            f.write(f"Due Date: {task[8]}\n")
            f.write(f"Created: {task[9]}\n")
            f.write("-" * 40 + "\n")

        # Write summary
        f.write("\nSUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Rooms: {len(rooms)}\n")
        f.write(f"Total People: {len(people)}\n")
        f.write(f"Total Tasks: {len(tasks)}\n")
        
        # Task status breakdown
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM tasks 
            GROUP BY status
        ''')
        status_counts = cursor.fetchall()
        f.write("\nTask Status Breakdown:\n")
        for status, count in status_counts:
            f.write(f"- {status}: {count} tasks\n")

    conn.close()
    print("Database has been exported to 'facility_management_export.txt'")

if __name__ == '__main__':
    export_database() 