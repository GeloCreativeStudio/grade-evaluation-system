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

    # Create tables
    cursor.execute("""
    CREATE TABLE students (
        student_number TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        mobile_number TEXT,
        email_address TEXT,
        password TEXT NOT NULL,
        year_level TEXT DEFAULT '1',
        semester TEXT DEFAULT '1',
        college TEXT DEFAULT '',
        program TEXT DEFAULT '',
        school_year TEXT DEFAULT '',
        enrollment_status TEXT DEFAULT 'Enrolled'
    )
    """)

    cursor.execute("""
    CREATE TABLE registrars (
        registrar_number TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        course_number TEXT,
        subject_name TEXT,
        units INTEGER,
        rating TEXT,
        final_grade REAL,
        status TEXT,
        year_level TEXT,
        semester TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_number)
    )
    """)

    # Insert default admin registrar
    cursor.execute("""
    INSERT INTO registrars (registrar_number, name, password)
    VALUES ('admin', 'System Administrator', 'admin123')
    """)

    # Insert sample student account
    cursor.execute("""
    INSERT INTO students (student_number, name, mobile_number, email_address, password)
    VALUES ('student', 'Sample Student', '09123456789', 'student@eecp.edu.ph', 'student123')
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
