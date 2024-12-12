"""
Test script to verify all components of the Grade Evaluation System.
"""

import sqlite3
import os
from src.utils.logger import logger
from src.database.database_operations import (
    fetch_courses, fetch_user_credentials, fetch_user_credentials2,
    insert_user_data_st, insert_user_dataR, insert_grade, update_grade
)

def get_test_db_path():
    """Get the path to the test database."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'test_database.db')

def test_database_connection():
    """Test database connection and basic operations."""
    try:
        conn = sqlite3.connect(get_test_db_path())
        cursor = conn.cursor()
        
        # Test if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        expected_tables = {'students', 'registrars', 'courses', 'student'}
        actual_tables = {table[0] for table in tables}
        
        missing_tables = expected_tables - actual_tables
        if missing_tables:
            logger.error(f"Missing tables: {missing_tables}")
            return False
            
        logger.info("Database connection and tables verified")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_student_operations():
    """Test student-related database operations."""
    try:
        # Test student registration
        success = insert_user_data_st(
            name="Test Student",
            student_number="TEST-001",
            course="Bachelor of Science in Computer Engineering",
            mobile_number="1234567890",
            email_address="test@example.com",
            password="test123"
        )
        if not success:
            logger.error("Failed to insert test student")
            return False
            
        # Test student authentication
        result = fetch_user_credentials("TEST-001", "test123")
        if not result:
            logger.error("Failed to authenticate test student")
            return False
            
        logger.info("Student operations test passed")
        return True
    except Exception as e:
        logger.error(f"Student operations test failed: {e}")
        return False

def test_registrar_operations():
    """Test registrar-related database operations."""
    try:
        # Test registrar registration
        success = insert_user_dataR(
            registrar_number="TEST-REG-001",
            name="Test Registrar",
            password="test123"
        )
        if not success:
            logger.error("Failed to insert test registrar")
            return False
            
        # Test registrar authentication
        result = fetch_user_credentials2("TEST-REG-001", "test123")
        if not result:
            logger.error("Failed to authenticate test registrar")
            return False
            
        logger.info("Registrar operations test passed")
        return True
    except Exception as e:
        logger.error(f"Registrar operations test failed: {e}")
        return False

def test_grade_operations():
    """Test grade-related database operations."""
    try:
        # Test grade insertion
        success = insert_grade(
            course_number="TEST-101",
            subject_name="Test Subject",
            units=3,
            rating="A",
            final_grade="95",
            status="Pass"
        )
        if not success:
            logger.error("Failed to insert test grade")
            return False
            
        # Test grade update
        success = update_grade("TEST-101", "final_grade", "97")
        if not success:
            logger.error("Failed to update test grade")
            return False
            
        logger.info("Grade operations test passed")
        return True
    except Exception as e:
        logger.error(f"Grade operations test failed: {e}")
        return False

def test_course_operations():
    """Test course-related database operations."""
    try:
        courses = fetch_courses()
        if not courses:
            logger.error("Failed to fetch courses")
            return False
            
        logger.info(f"Successfully fetched {len(courses)} courses")
        return True
    except Exception as e:
        logger.error(f"Course operations test failed: {e}")
        return False

def run_all_tests():
    """Run all system tests."""
    logger.info("Starting system tests...")
    
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Student Operations", test_student_operations),
        ("Registrar Operations", test_registrar_operations),
        ("Grade Operations", test_grade_operations),
        ("Course Operations", test_course_operations)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        logger.info(f"Running {test_name} test...")
        try:
            if test_func():
                logger.info(f"{test_name} test passed")
            else:
                logger.error(f"{test_name} test failed")
                all_passed = False
        except Exception as e:
            logger.error(f"{test_name} test failed with error: {e}")
            all_passed = False
    
    if all_passed:
        logger.info("All tests passed successfully!")
    else:
        logger.error("Some tests failed. Check the logs for details.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
