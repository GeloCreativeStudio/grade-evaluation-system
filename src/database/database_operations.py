"""
Database operations for the Grade Evaluation System.
"""

import sqlite3
import logging
import os
from ..utils.logger import logger

def get_db_connection():
    """Get a connection to the SQLite database."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'eecp_gesys.db')
    return sqlite3.connect(db_path)

def fetch_student_data():
    """Fetch all student data from the database."""
    logger.debug("Fetching all student data")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, name, mobile_number, email_address,
                   year_level, semester, college, program,
                   school_year, enrollment_status
            FROM students
        """)
        students = cursor.fetchall()
        logger.info(f"Successfully fetched {len(students)} students")
        return students
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching students: {e}")
        return []
    finally:
        conn.close()

def fetch_student_grades(student_id):
    """Fetch grades for a specific student."""
    logger.debug(f"Fetching grades for student: {student_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT subject, units, rating, final_grade, status,
                   year_level, semester
            FROM grades 
            WHERE student_id = ?
            ORDER BY year_level, semester, subject
        """, (student_id,))
        grades = cursor.fetchall()
        logger.info(f"Successfully fetched {len(grades)} grades for student: {student_id}")
        return grades
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching grades: {e}")
        return []
    finally:
        conn.close()

def update_grade(student_id, subject, units, rating, final_grade, status, year_level, semester):
    """Update or insert a grade for a student."""
    logger.debug(f"Updating grade for student {student_id}, subject {subject}")
    
    # Validate input data
    try:
        units = int(units)
        rating = float(rating)
        year_level = int(year_level)
        semester = int(semester)
        
        if units <= 0 or units > 6:
            logger.error("Invalid units value")
            return False
        if rating < 1.0 or rating > 5.0:
            logger.error("Invalid rating value")
            return False
        if year_level < 1 or year_level > 5:
            logger.error("Invalid year level")
            return False
        if semester < 1 or semester > 3:
            logger.error("Invalid semester")
            return False
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if grade exists
        cursor.execute("""
            SELECT id FROM grades 
            WHERE student_id = ? AND subject = ? AND year_level = ? AND semester = ?
        """, (student_id, subject, year_level, semester))
        
        exists = cursor.fetchone()
        
        if exists:
            # Update existing grade
            cursor.execute("""
                UPDATE grades 
                SET units = ?, rating = ?, final_grade = ?, status = ?
                WHERE student_id = ? AND subject = ? AND year_level = ? AND semester = ?
            """, (units, rating, final_grade, status, 
                  student_id, subject, year_level, semester))
            logger.info(f"Updated grade for student {student_id}, subject {subject}")
        else:
            # Insert new grade
            cursor.execute("""
                INSERT INTO grades (student_id, subject, units, rating, 
                                  final_grade, status, year_level, semester)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, subject, units, rating, final_grade, 
                  status, year_level, semester))
            logger.info(f"Inserted new grade for student {student_id}, subject {subject}")
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while updating grade: {e}")
        return False
    finally:
        conn.close()

def delete_grade(student_id, subject, year_level, semester):
    """Delete a grade for a student."""
    logger.debug(f"Deleting grade for student {student_id}, subject {subject}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM grades 
            WHERE student_id = ? AND subject = ? AND year_level = ? AND semester = ?
        """, (student_id, subject, year_level, semester))
        conn.commit()
        logger.info(f"Deleted grade for student {student_id}, subject {subject}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while deleting grade: {e}")
        return False
    finally:
        conn.close()

def search_students(query):
    """Search for students based on a query."""
    logger.debug(f"Searching for students with query: {query}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT student_id, name, course, mobile_number, email_address 
            FROM students
            WHERE student_id LIKE ? OR name LIKE ? 
            OR course LIKE ? OR mobile_number LIKE ? OR email_address LIKE ?
        """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} students matching query: {query}")
        return results
    except sqlite3.Error as e:
        logger.error(f"Database error while searching: {e}")
        return []
    finally:
        conn.close()

def fetch_user_credentials(student_number, password):
    """Verify student login credentials."""
    logger.debug(f"Attempting to fetch credentials for student: {student_number}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM students 
            WHERE student_id = ? AND password = ?
        """, (student_number, password))
        result = cursor.fetchone() is not None
        if result:
            logger.info(f"Successfully authenticated student: {student_number}")
        else:
            logger.warning(f"Failed login attempt for student: {student_number}")
        return result
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching credentials: {e}")
        return False
    finally:
        conn.close()

def fetch_user_credentials2(registrar_number, password):
    """Verify registrar login credentials."""
    logger.debug(f"Attempting to fetch credentials for registrar: {registrar_number}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM registrars 
            WHERE registrar_id = ? AND password = ?
        """, (registrar_number, password))
        result = cursor.fetchone() is not None
        if result:
            logger.info(f"Successfully authenticated registrar: {registrar_number}")
        else:
            logger.warning(f"Failed login attempt for registrar: {registrar_number}")
        return result
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching credentials: {e}")
        return False
    finally:
        conn.close()

def insert_user_data_st(student_number, name, mobile_number, email_address, password, 
                       year_level='1', semester='1', college='', program='', 
                       school_year='', enrollment_status='Enrolled'):
    """Insert a new student."""
    logger.debug(f"Inserting new student: {student_number}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students 
            (student_id, name, mobile_number, email_address, password,
             year_level, semester, college, program, school_year, enrollment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_number, name, mobile_number, email_address, password,
              year_level, semester, college, program, school_year, enrollment_status))
        conn.commit()
        logger.info(f"Successfully inserted student: {student_number}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while inserting student: {e}")
        return False
    finally:
        conn.close()

def update_student_data(student_id, name, mobile_number, email_address, 
                       year_level=None, semester=None, college=None, program=None, 
                       school_year=None, enrollment_status=None):
    """Update student information."""
    logger.debug(f"Updating student: {student_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students 
            SET name=?, mobile_number=?, email_address=?,
                year_level=?, semester=?, college=?, program=?,
                school_year=?, enrollment_status=?
            WHERE student_id=?
        """, (name, mobile_number, email_address,
              year_level, semester, college, program,
              school_year, enrollment_status, student_id))
        conn.commit()
        logger.info(f"Successfully updated student: {student_id}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while updating student: {e}")
        return False
    finally:
        conn.close()

def get_student_info(student_id):
    """Get detailed information about a student."""
    logger.debug(f"Fetching info for student: {student_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, name, mobile_number, email_address,
                   year_level, semester, college, program,
                   school_year, enrollment_status
            FROM students 
            WHERE student_id = ?
        """, (student_id,))
        student_info = cursor.fetchone()
        logger.info(f"Successfully fetched student info: {student_id}")
        return student_info
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching student info: {e}")
        return None
    finally:
        conn.close()

def delete_student(student_id):
    """Delete a student and their grades."""
    logger.debug(f"Attempting to delete student: {student_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Delete grades first (foreign key constraint)
        cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
        # Delete student
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        logger.info(f"Successfully deleted student: {student_id}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while deleting student: {e}")
        return False
    finally:
        conn.close()

def insert_user_dataR(registrar_id, name, password):
    """Insert a new registrar."""
    logger.debug(f"Attempting to insert new registrar: {registrar_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO registrars (registrar_id, name, password)
            VALUES (?, ?, ?)
        """, (registrar_id, name, password))
        conn.commit()
        logger.info(f"Successfully inserted registrar: {registrar_id}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error while inserting registrar: {e}")
        return False
    finally:
        conn.close()

def populate_treeview_from_db(treeview):
    """Populate treeview with student data from the database."""
    # Clear existing items
    for item in treeview.get_children():
        treeview.delete(item)
    
    try:
        # Fetch student data
        students = fetch_student_data()
        
        # Insert into treeview
        for student in students:
            student_id, name, mobile, email, year, term, college, program, school_year, status = student
            treeview.insert('', 'end', values=(
                student_id, name, mobile, email, 
                year, term, college, program,
                school_year, status
            ))
            
    except Exception as e:
        logger.error(f"Error populating treeview: {e}")
