"""
Initialize the database for the Grade Evaluation System.
"""

import sqlite3
import os
from datetime import datetime

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

    # Create tables
    cursor.execute("""
    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        mobile_number TEXT,
        email_address TEXT,
        password TEXT NOT NULL,
        year_level TEXT DEFAULT '1',
        semester TEXT DEFAULT '1',
        college TEXT DEFAULT 'EECP',
        program TEXT DEFAULT 'BSIT',
        school_year TEXT DEFAULT '2024-2025',
        enrollment_status TEXT DEFAULT 'Enrolled'
    )
    """)

    cursor.execute("""
    CREATE TABLE registrars (
        registrar_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        subject TEXT,
        units INTEGER,
        rating TEXT,
        final_grade REAL,
        status TEXT,
        year_level TEXT,
        semester TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    """)

    # Insert default admin registrar
    cursor.execute("""
    INSERT INTO registrars (registrar_id, name, password)
    VALUES 
        ('REG001', 'System Administrator', 'admin123'),
        ('REG002', 'Angelo Manalo', 'admin123')
    """)

    # Insert sample student accounts
    cursor.execute("""
    INSERT INTO students (
        student_id, name, mobile_number, 
        email_address, password, year_level, 
        semester, college, program, 
        school_year, enrollment_status
    ) VALUES 
        ('202410769', 'Angelo Manalo', '09925528110',
         '202410769@eecp.edu.ph', 'student123', '1',
         '1', 'EECP', 'BSIT',
         '2024-2025', 'Enrolled'),
        ('202400001', 'John Doe', '09123456789',
         'student@eecp.edu.ph', 'student123', '1',
         '1', 'EECP', 'BSIT',
         '2024-2025', 'Enrolled')
    """)

    # Insert sample grades
    cursor.execute("""
    INSERT INTO grades (
        student_id, subject, units,
        rating, final_grade, status,
        year_level, semester
    ) VALUES 
        ('202410769', 'Introduction to Computing', 3,
         '1.00', 1.00, 'Passed', '1', '1'),
        ('202410769', 'Computer Programming 1', 3,
         '1.25', 1.25, 'Passed', '1', '1'),
        ('202410769', 'Computer Programming 2', 3,
         '1.50', 1.50, 'Passed', '1', '1')
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
