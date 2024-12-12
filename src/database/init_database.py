"""
Initialize the database for the Grade Evaluation System.
"""

import sqlite3
import os

def init_db():
    """Initialize the database with tables and sample data."""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Connect to database in data directory
    db_path = os.path.join(data_dir, 'eecp_gesys.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS grades")
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("DROP TABLE IF EXISTS registrars")

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            email_address TEXT NOT NULL,
            password TEXT NOT NULL,
            year_level TEXT,
            semester TEXT,
            college TEXT,
            program TEXT,
            school_year TEXT,
            enrollment_status TEXT
        )
    ''')

    # Create registrars table
    cursor.execute("""
        CREATE TABLE registrars (
            registrar_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create grades table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            units INTEGER NOT NULL,
            rating REAL NOT NULL,
            final_grade TEXT NOT NULL,
            status TEXT NOT NULL,
            year_level INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')

    # Insert sample data
    # Sample registrars
    cursor.execute('''
        INSERT OR REPLACE INTO registrars 
        (registrar_id, name, password)
        VALUES 
        ('REG001', 'ADMIN', 'admin123')
    ''')

    # Insert sample student data
    cursor.execute('''
        INSERT OR REPLACE INTO students 
        (student_id, name, mobile_number, email_address, password, 
         year_level, semester, college, program, school_year, enrollment_status)
        VALUES 
        ('202410769', 'MANALO, ANGELO LOPEZ', '09123456789', 
         'angelo.manalo@student.dlsu.edu.ph', 'password123', 
         '1', '1', 'COMPUTER STUDIES', 'BSCSAI', '2024-2025', 'Enrolled')
    ''')

    # Insert sample grades
    cursor.execute('''
        INSERT OR REPLACE INTO grades 
        (student_id, subject, units, rating, final_grade, status, year_level, semester)
        VALUES 
        ('202410769', 'Programming 1', 3, 1.25, '1.25', 'Passed', 1, 1),
        ('202410769', 'Mathematics 1', 3, 1.50, '1.50', 'Passed', 1, 1),
        ('202410769', 'Data Structures', 3, 1.75, '1.75', 'Passed', 1, 1)
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
