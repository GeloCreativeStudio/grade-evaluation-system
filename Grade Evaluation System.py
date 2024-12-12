import sqlite3
import tkinter as tk
import ttkthemes
from tkinter import ttk, Frame, simpledialog, messagebox
from PIL import Image, ImageTk
import hashlib
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')
        try:
            result = func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            result = None
        finally:
            conn.close()
        return result
    return wrapper

@db_connection
def fetch_courses(conn):
    """Fetch all available courses from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

@db_connection
def fetch_user_credentials(conn, student_number, password):
    """Verify student credentials and return user data if valid."""
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute(
            'SELECT name, student_number FROM students WHERE student_number = ? AND password = ?',
            (student_number, hashed_password)
        )
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@db_connection
def fetch_user_credentials2(conn, registrar_number, password):
    """Verify registrar credentials and return user data if valid."""
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute(
            'SELECT * FROM registrars WHERE registrar_number = ? AND password = ?',
            (registrar_number, hashed_password)
        )
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@db_connection
def populate_treeview_from_db(conn, tree):
    """Fetch data from the database and populate the Treeview."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT course_number, subject_name, units, rating, final_grade, status FROM student")
        data = cursor.fetchall()

        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Insert data into the Treeview
        for row in data:
            tree.insert('', 'end', values=row)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

@db_connection
def insert_user_data_st(conn, name, student_number, course, mobile_number, email_address, password):
    """Insert student data into the database."""
    try:
        hashed_password = hash_password(password)
        cursor = conn.cursor()
        data_insert_query = '''INSERT INTO students (name, student_number, course, mobile_number, email_address, password) VALUES (?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (name, student_number, course, mobile_number, email_address, hashed_password)
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()  # Commit the changes
        print(f"Data inserted successfully: {name}, {student_number}, {course}, {mobile_number}, {email_address}")
    except sqlite3.IntegrityError:
        print(f"Error: Student number {student_number} already exists.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

@db_connection
def insert_user_dataR(conn, registrar_number, name, password):
    """Insert registrar data into the database."""
    try:
        hashed_password = hash_password(password)
        cursor = conn.cursor()
        data_insert_query2 = '''INSERT INTO registrars (registrar_number, name, password) VALUES (?, ?, ?)'''
        data_insert_tuple2 = (registrar_number, name, hashed_password)
        cursor.execute(data_insert_query2, data_insert_tuple2)
        conn.commit()  # Commit the changes
        print(f"Data inserted: {registrar_number}, {name}, {password}")
    except sqlite3.IntegrityError:
        print(f"Error: Registrar number {registrar_number} already exists.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# UI Constants and Styles
WINDOW_WIDTH = 1320
WINDOW_HEIGHT = 780
PADDING = 20
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
ENTRY_WIDTH = 250
ENTRY_HEIGHT = 30

class GradeEvaluationSystem:
    def __init__(self):
        self.initialize_database()  # Initialize database first
        self.setup_window()
        self.setup_styles()
        self.create_frames()
        self.create_entry_screen()  # Show the entry screen by default
        self.show_entry()  # Show the entry screen
        
    def setup_window(self):
        self.root = ttkthemes.ThemedTk()
        self.root.state('zoomed')
        self.root.title("EECP Grade Evaluation System")
        self.root.set_theme('arc')
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('TLabel', padding=5)
        
    def create_frames(self):
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for main container
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create frames
        self.create_entry_screen()
        self.create_student_login()
        self.create_student_signup()
        self.create_student_dashboard()
        self.create_registrar_login()
        self.create_registrar_dashboard()

    def create_entry_screen(self):
        """Create the entry screen with student and registrar login options."""
        self.entry_frame = ttk.Frame(self.main_container)
        self.entry_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create a centered frame for buttons
        center_frame = ttk.Frame(self.entry_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add title label
        title_label = ttk.Label(center_frame, text="Grade Evaluation System", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)
        
        # Add buttons
        ttk.Button(center_frame, text="Student Login", command=self.show_student_login, width=20).pack(pady=10)
        ttk.Button(center_frame, text="Student Sign Up", command=self.show_student_signup, width=20).pack(pady=10)
        ttk.Button(center_frame, text="Registrar Login", command=self.show_registrar_login, width=20).pack(pady=10)

    def create_student_login(self):
        """Create the student login frame."""
        self.student_login = ttk.Frame(self.main_container)
        
        # Create a centered frame for login
        login_frame = ttk.LabelFrame(self.student_login, text="Student Login")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Username
        ttk.Label(login_frame, text="Student Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.student_username = ttk.Entry(login_frame, width=30)
        self.student_username.grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.student_password = ttk.Entry(login_frame, show="*", width=30)
        self.student_password.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Login", command=self.student_login_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_entry).pack(side="left", padx=5)

    def create_student_signup(self):
        self.student_signup = ttk.Frame(self.main_container)
        self.student_signup.grid(row=0, column=0, sticky="nsew")
        self.student_signup.grid_remove()  # Hide initially
        
        # Create a centered frame for signup
        signup_frame = ttk.LabelFrame(self.student_signup, text="Student Sign Up")
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Name
        ttk.Label(signup_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.signup_name = ttk.Entry(signup_frame)
        self.signup_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Student Number
        ttk.Label(signup_frame, text="Student Number:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.signup_student_number = ttk.Entry(signup_frame)
        self.signup_student_number.grid(row=1, column=1, padx=5, pady=5)
        
        # Course
        ttk.Label(signup_frame, text="Course:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.signup_course = ttk.Combobox(signup_frame, state="readonly")
        self.signup_course['values'] = fetch_courses()
        self.signup_course.grid(row=2, column=1, padx=5, pady=5)
        
        # Mobile Number
        ttk.Label(signup_frame, text="Mobile Number:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.signup_mobile = ttk.Entry(signup_frame)
        self.signup_mobile.grid(row=3, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(signup_frame, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.signup_email = ttk.Entry(signup_frame)
        self.signup_email.grid(row=4, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(signup_frame, text="Password:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.signup_password = ttk.Entry(signup_frame, show="*")
        self.signup_password.grid(row=5, column=1, padx=5, pady=5)
        
        # Confirm Password
        ttk.Label(signup_frame, text="Confirm Password:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.signup_confirm_password = ttk.Entry(signup_frame, show="*")
        self.signup_confirm_password.grid(row=6, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(signup_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Sign Up", command=self.sign_up_st).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_entry).pack(side="left", padx=5)

    def create_student_dashboard(self):
        self.student_dashboard = ttk.Frame(self.main_container)
        
        # Create a centered dashboard
        dashboard_frame = ttk.LabelFrame(self.student_dashboard, text="Student Dashboard")
        dashboard_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create Treeview with scrollbar
        tree_frame = ttk.Frame(dashboard_frame)
        tree_frame.grid(row=0, column=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="nsew")
        
        # Create Treeview
        columns = ('course_code', 'course_name', 'units', 'midterm_grade', 'final_grade', 'remarks')
        self.student_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Define column headings
        self.student_tree.heading('course_code', text='Course Code')
        self.student_tree.heading('course_name', text='Course Name')
        self.student_tree.heading('units', text='Units')
        self.student_tree.heading('midterm_grade', text='Midterm Grade')
        self.student_tree.heading('final_grade', text='Final Grade')
        self.student_tree.heading('remarks', text='Remarks')
        
        # Define column widths
        self.student_tree.column('course_code', width=100)
        self.student_tree.column('course_name', width=200)
        self.student_tree.column('units', width=50)
        self.student_tree.column('midterm_grade', width=100)
        self.student_tree.column('final_grade', width=100)
        self.student_tree.column('remarks', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the Treeview and scrollbar
        self.student_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dashboard_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=PADDING)
        
        ttk.Button(button_frame, text="Refresh", command=self.populate_student_treeview).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_student_login).pack(side="left", padx=5)

    def populate_student_treeview(self):
        """Populate the student dashboard treeview with grades."""
        try:
            # Clear existing items
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)
            
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.course_code, c.course_name, c.units, 
                           g.midterm_grade, g.final_grade, g.remarks
                    FROM grades g
                    JOIN courses c ON g.course_code = c.course_code
                    WHERE g.student_number = ?
                    ORDER BY g.semester, c.course_code
                """, (self.current_student,))
                
                for row in cursor.fetchall():
                    self.student_tree.insert('', 'end', values=row)
                    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch grades: {e}")
            print(f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            print(f"Error: {e}")

    def create_registrar_login(self):
        """Create the registrar login frame."""
        self.registrar_login = ttk.Frame(self.main_container)
        
        # Create a centered frame for login
        login_frame = ttk.LabelFrame(self.registrar_login, text="Registrar Login")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Registrar Number
        ttk.Label(login_frame, text="Registrar Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.registrar_number = ttk.Entry(login_frame, width=30)
        self.registrar_number.grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.registrar_password = ttk.Entry(login_frame, show="*", width=30)
        self.registrar_password.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Login", command=self.registrar_login_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_entry).pack(side="left", padx=5)

    def registrar_login_action(self):
        """Handle registrar login."""
        registrar_number = self.registrar_number.get().strip()
        password = self.registrar_password.get()

        if not registrar_number or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        try:
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                hashed_password = hash_password(password)
                cursor.execute("""
                    SELECT name, registrar_number 
                    FROM registrars 
                    WHERE registrar_number = ? AND password = ?
                """, (registrar_number, hashed_password))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Success", f"Welcome, {result[0]}!")
                    self.current_registrar = result[1]  # Store registrar number for dashboard
                    self.show_registrar_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid registrar number or password!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to verify credentials: {e}")
            print(f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            print(f"Error: {e}")

    def create_registrar_signup(self):
        self.registrar_signup = ttk.Frame(self.main_container)
        
        # Create a centered signup form
        signup_frame = ttk.LabelFrame(self.registrar_signup, text="Registrar Signup")
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Registrar Number field
        ttk.Label(signup_frame, text="Registrar Number:").grid(row=0, column=0, padx=PADDING, pady=PADDING)
        self.rn_entry = ttk.Entry(signup_frame, width=30)
        self.rn_entry.grid(row=0, column=1, padx=PADDING, pady=PADDING)
        
        # Name field
        ttk.Label(signup_frame, text="Name:").grid(row=1, column=0, padx=PADDING, pady=PADDING)
        self.username_entry1 = ttk.Entry(signup_frame, width=30)
        self.username_entry1.grid(row=1, column=1, padx=PADDING, pady=PADDING)
        
        # Password field
        ttk.Label(signup_frame, text="Password:").grid(row=2, column=0, padx=PADDING, pady=PADDING)
        self.pass_entry1 = ttk.Entry(signup_frame, show="*", width=30)
        self.pass_entry1.grid(row=2, column=1, padx=PADDING, pady=PADDING)
        
        # Buttons
        button_frame = ttk.Frame(signup_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=PADDING)
        
        ttk.Button(button_frame, text="Sign Up", command=self.sign_up).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_registrar_login).pack(side="left", padx=5)

    def create_registrar_dashboard(self):
        self.registrar_dashboard = ttk.Frame(self.main_container)
        
        # Create a centered dashboard
        dashboard_frame = ttk.LabelFrame(self.registrar_dashboard, text="Registrar Dashboard")
        dashboard_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create search frame
        search_frame = ttk.Frame(dashboard_frame)
        search_frame.grid(row=0, column=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="ew")
        
        ttk.Label(search_frame, text="Search Student:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_student).pack(side="left", padx=5)
        
        # Create Treeview with scrollbar
        tree_frame = ttk.Frame(dashboard_frame)
        tree_frame.grid(row=1, column=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="nsew")
        
        # Create Treeview
        columns = ('student_number', 'name', 'course_code', 'course_name', 'semester', 'school_year', 'midterm_grade', 'final_grade', 'remarks')
        self.registrar_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Define column headings
        self.registrar_tree.heading('student_number', text='Student Number')
        self.registrar_tree.heading('name', text='Name')
        self.registrar_tree.heading('course_code', text='Course Code')
        self.registrar_tree.heading('course_name', text='Course Name')
        self.registrar_tree.heading('semester', text='Semester')
        self.registrar_tree.heading('school_year', text='School Year')
        self.registrar_tree.heading('midterm_grade', text='Midterm Grade')
        self.registrar_tree.heading('final_grade', text='Final Grade')
        self.registrar_tree.heading('remarks', text='Remarks')
        
        # Define column widths
        self.registrar_tree.column('student_number', width=100)
        self.registrar_tree.column('name', width=150)
        self.registrar_tree.column('course_code', width=100)
        self.registrar_tree.column('course_name', width=200)
        self.registrar_tree.column('semester', width=100)
        self.registrar_tree.column('school_year', width=100)
        self.registrar_tree.column('midterm_grade', width=100)
        self.registrar_tree.column('final_grade', width=100)
        self.registrar_tree.column('remarks', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.registrar_tree.yview)
        self.registrar_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the Treeview and scrollbar
        self.registrar_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Add double-click event binding for editing
        self.registrar_tree.bind("<Double-1>", self.edit_grade)
        
        # Buttons
        button_frame = ttk.Frame(dashboard_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=PADDING)
        
        ttk.Button(button_frame, text="Refresh", command=self.populate_registrar_treeview).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_registrar_login).pack(side="left", padx=5)

    def search_student(self):
        """Search for a student in the database."""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term")
            return
            
        try:
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT s.student_number, s.name, c.course_code, c.course_name,
                           g.semester, g.school_year, g.midterm_grade, g.final_grade, g.remarks
                    FROM grades g
                    JOIN students s ON g.student_number = s.student_number
                    JOIN courses c ON g.course_code = c.course_code
                    WHERE s.student_number LIKE ? OR s.name LIKE ?
                """, (f"%{search_term}%", f"%{search_term}%"))
                
                # Clear existing items
                for item in self.registrar_tree.get_children():
                    self.registrar_tree.delete(item)
                    
                # Insert new data
                for row in cursor.fetchall():
                    self.registrar_tree.insert('', 'end', values=row)
                    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to search student: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def edit_grade(self, event):
        """Handle double-click event to edit grades."""
        tree = event.widget
        region = tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        column = tree.identify_column(event.x)
        column_id = int(column[1]) - 1  # Convert visual column to data column
        item = tree.selection()[0]
        
        # Only allow editing midterm and final grades
        if column_id not in [6, 7]:  # midterm_grade and final_grade columns
            messagebox.showinfo("Info", "This field cannot be edited")
            return
            
        current_value = tree.item(item)['values'][column_id]
        column_name = tree['columns'][column_id]
        
        # Show dialog to edit value
        new_value = simpledialog.askstring(
            "Edit Grade",
            f"Enter new value for {column_name}:",
            initialvalue=current_value
        )
        
        if new_value is not None:
            try:
                # Update treeview
                values = list(tree.item(item)['values'])
                values[column_id] = new_value
                tree.item(item, values=values)
                
                # Update database
                with sqlite3.connect('my_database.db') as conn:
                    cursor = conn.cursor()
                    student_number = values[0]
                    course_code = values[2]
                    cursor.execute(f"""
                        UPDATE grades 
                        SET {column_name} = ? 
                        WHERE student_number = ? AND course_code = ?
                    """, (new_value, student_number, course_code))
                    conn.commit()
                    
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to update grade: {e}")
                self.populate_registrar_treeview()  # Refresh to show original data
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                self.populate_registrar_treeview()

    def populate_registrar_treeview(self):
        """Populate the registrar dashboard treeview with all student grades."""
        try:
            # Clear existing items
            for item in self.registrar_tree.get_children():
                self.registrar_tree.delete(item)
            
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT s.student_number, s.name, c.course_code, c.course_name,
                           g.semester, g.school_year, g.midterm_grade, g.final_grade, g.remarks
                    FROM grades g
                    JOIN students s ON g.student_number = s.student_number
                    JOIN courses c ON g.course_code = c.course_code
                    ORDER BY s.student_number, g.semester, c.course_code
                """)
                
                for row in cursor.fetchall():
                    self.registrar_tree.insert('', 'end', values=row)
                    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch grades: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def initialize_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                
                # Drop existing tables if they exist
                cursor.execute("DROP TABLE IF EXISTS student")
                cursor.execute("DROP TABLE IF EXISTS students")
                cursor.execute("DROP TABLE IF EXISTS registrars")
                cursor.execute("DROP TABLE IF EXISTS courses")
                cursor.execute("DROP TABLE IF EXISTS grades")
                
                # Create students table
                cursor.execute("""
                    CREATE TABLE students (
                        student_number TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        course TEXT NOT NULL,
                        mobile_number TEXT,
                        email_address TEXT,
                        password TEXT NOT NULL
                    )
                """)
                
                # Create registrars table
                cursor.execute("""
                    CREATE TABLE registrars (
                        registrar_number TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                """)
                
                # Create courses table
                cursor.execute("""
                    CREATE TABLE courses (
                        course_code TEXT PRIMARY KEY,
                        course_name TEXT NOT NULL,
                        units INTEGER NOT NULL
                    )
                """)
                
                # Create grades table
                cursor.execute("""
                    CREATE TABLE grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_number TEXT NOT NULL,
                        course_code TEXT NOT NULL,
                        semester TEXT NOT NULL,
                        school_year TEXT NOT NULL,
                        midterm_grade REAL,
                        final_grade REAL,
                        remarks TEXT,
                        FOREIGN KEY (student_number) REFERENCES students(student_number),
                        FOREIGN KEY (course_code) REFERENCES courses(course_code)
                    )
                """)
                
                # Insert default courses
                default_courses = [
                    ('CS101', 'Introduction to Computing', 3),
                    ('CS102', 'Computer Programming 1', 3),
                    ('CS103', 'Computer Programming 2', 3),
                    ('CS104', 'Data Structures and Algorithms', 3),
                    ('CS105', 'Object-Oriented Programming', 3)
                ]
                cursor.executemany(
                    "INSERT INTO courses (course_code, course_name, units) VALUES (?, ?, ?)",
                    default_courses
                )
                
                # Insert test accounts
                # Test student account (password: 123456)
                cursor.execute("""
                    INSERT INTO students (student_number, name, course, mobile_number, email_address, password)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ('2023-0001', 'Test Student', 'BS Computer Science', '1234567890', 
                      'test@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'))
                
                # Test registrar account (password: 123456)
                cursor.execute("""
                    INSERT INTO registrars (registrar_number, name, password)
                    VALUES (?, ?, ?)
                """, ('REG-001', 'Test Registrar', 
                     '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'))
                
                # Insert test grades
                test_grades = [
                    ('2023-0001', 'CS101', '1st', '2023-2024', 85.5, 88.0, 'PASSED'),
                    ('2023-0001', 'CS102', '1st', '2023-2024', 90.0, 92.5, 'PASSED'),
                    ('2023-0001', 'CS103', '1st', '2023-2024', 87.5, 89.0, 'PASSED')
                ]
                cursor.executemany("""
                    INSERT INTO grades (student_number, course_code, semester, school_year, 
                                     midterm_grade, final_grade, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, test_grades)
                
                conn.commit()
                print("Database initialized successfully!")
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            raise

    def show_entry(self):
        """Show the entry screen and hide other frames."""
        self.hide_all_frames()
        self.entry_frame.grid(row=0, column=0, sticky="nsew")
        
    def hide_all_frames(self):
        """Hide all frames in the application."""
        if hasattr(self, 'entry_frame'):
            self.entry_frame.grid_remove()
        if hasattr(self, 'student_login'):
            self.student_login.grid_remove()
        if hasattr(self, 'student_signup'):
            self.student_signup.grid_remove()
        if hasattr(self, 'student_dashboard'):
            self.student_dashboard.grid_remove()
        if hasattr(self, 'registrar_login'):
            self.registrar_login.grid_remove()
        if hasattr(self, 'registrar_dashboard'):
            self.registrar_dashboard.grid_remove()

    def show_student_login(self):
        """Show student login screen."""
        self.hide_all_frames()
        self.student_login.grid(row=0, column=0, sticky="nsew")

    def show_student_signup(self):
        """Show student signup screen."""
        self.hide_all_frames()
        self.student_signup.grid(row=0, column=0, sticky="nsew")

    def show_student_dashboard(self):
        """Show student dashboard screen."""
        self.hide_all_frames()
        self.student_dashboard.grid(row=0, column=0, sticky="nsew")
        self.populate_student_treeview()

    def show_registrar_login(self):
        """Show registrar login screen."""
        self.hide_all_frames()
        self.registrar_login.grid(row=0, column=0, sticky="nsew")

    def show_registrar_dashboard(self):
        """Show registrar dashboard screen."""
        self.hide_all_frames()
        self.registrar_dashboard.grid(row=0, column=0, sticky="nsew")
        self.populate_registrar_treeview()

    def student_login_action(self):
        student_number = self.student_username.get().strip()
        password = self.student_password.get()

        if not student_number or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        try:
            with sqlite3.connect('my_database.db') as conn:
                cursor = conn.cursor()
                hashed_password = hash_password(password)
                cursor.execute("""
                    SELECT name, student_number 
                    FROM students 
                    WHERE student_number = ? AND password = ?
                """, (student_number, hashed_password))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Success", f"Welcome, {result[0]}!")
                    self.current_student = result[1]  # Store student number for dashboard
                    self.show_student_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid student number or password!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to verify credentials: {e}")
            print(f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            print(f"Error: {e}")

    def sign_up_st(self):
        name = self.signup_name.get()
        student_number = self.signup_student_number.get()
        course = self.signup_course.get()
        mobile_number = self.signup_mobile.get()
        email = self.signup_email.get()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()

        # Check if all fields are filled
        if not name or not student_number or not course or not mobile_number or not email or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            # Call the function with all the necessary arguments
            insert_user_data_st(name, student_number, course, mobile_number, email, password)
            messagebox.showinfo("Success", "Sign-Up Successful!")
            self.show_student_login()
            self.clear_student_signup_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This student number is already taken.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def sign_up(self):
        registrar_number = self.rn_entry.get()
        name = self.username_entry1.get()
        password = self.pass_entry1.get()

        # Check if all fields are filled
        if not registrar_number or not name or not password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            # Insert data into the database
            insert_user_dataR(registrar_number, name, password)
            messagebox.showinfo("Success", "Sign-Up Successful!")
            self.show_registrar_login()
            self.clear_registrar_signup_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This registrar number is already taken.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def clear_student_signup_form(self):
        self.signup_name.delete(0, tk.END)
        self.signup_student_number.delete(0, tk.END)
        self.signup_course.set('')
        self.signup_mobile.delete(0, tk.END)
        self.signup_email.delete(0, tk.END)
        self.signup_password.delete(0, tk.END)
        self.signup_confirm_password.delete(0, tk.END)

    def clear_registrar_signup_form(self):
        self.rn_entry.delete(0, tk.END)
        self.username_entry1.delete(0, tk.END)
        self.pass_entry1.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Create images directory if it doesn't exist
    IMAGES_DIR.mkdir(exist_ok=True)
    
    # Initialize and run the application
    app = GradeEvaluationSystem()
    app.run()