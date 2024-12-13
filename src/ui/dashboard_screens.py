"""
Dashboard screens for the Grade Evaluation System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from ..database.database_operations import (
    fetch_student_data, fetch_student_grades, update_grade,
    delete_grade, search_students, insert_user_data_st,
    update_student_data, get_student_info, delete_student
)
from ..utils.form_utilities import validate_email, validate_mobile
from .ui_components import COLORS, create_custom_button

class StudentDashboard(ttk.Frame):
    """Dashboard screen for students."""
    
    def __init__(self, root, nav_manager, app, student_id):
        super().__init__(root)
        self.root = root
        self.nav_manager = nav_manager
        self.app = app
        self.student_id = student_id
        
        self.create_widgets()
        self.load_student_info()
        self.load_student_grades(self.student_id)
    
    def create_widgets(self):
        """Create and setup the dashboard widgets."""
        # Main container with padding
        main_container = ttk.Frame(self, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_container, text="Student Dashboard", 
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Student Information Frame
        info_frame = ttk.LabelFrame(main_container, text="Student Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create two columns for student info
        left_frame = ttk.Frame(info_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        right_frame = ttk.Frame(info_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Left column labels
        self.id_label = ttk.Label(left_frame, text="Student ID:")
        self.id_label.pack(anchor='w', pady=2)
        
        self.name_label = ttk.Label(left_frame, text="Name:")
        self.name_label.pack(anchor='w', pady=2)
        
        self.college_label = ttk.Label(left_frame, text="College:")
        self.college_label.pack(anchor='w', pady=2)
        
        self.program_label = ttk.Label(left_frame, text="Program:")
        self.program_label.pack(anchor='w', pady=2)
        
        self.year_label = ttk.Label(left_frame, text="Year Level:")
        self.year_label.pack(anchor='w', pady=2)
        
        # Right column labels
        self.term_label = ttk.Label(right_frame, text="Term:")
        self.term_label.pack(anchor='w', pady=2)
        
        self.school_year_label = ttk.Label(right_frame, text="School Year:")
        self.school_year_label.pack(anchor='w', pady=2)
        
        self.status_label = ttk.Label(right_frame, text="Status:")
        self.status_label.pack(anchor='w', pady=2)
        
        self.email_label = ttk.Label(right_frame, text="Email:")
        self.email_label.pack(anchor='w', pady=2)
        
        self.mobile_label = ttk.Label(right_frame, text="Mobile:")
        self.mobile_label.pack(anchor='w', pady=2)
        
        # Grades Frame
        grades_frame = ttk.LabelFrame(main_container, text="Grade Information", padding="10")
        grades_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create Treeview for grades
        columns = ('Subject', 'Units', 'Rating', 'Final Grade', 'Status', 'Year Level', 'Term')
        self.grades_tree = ttk.Treeview(grades_frame, columns=columns, show='headings', height=10)
        
        # Set column headings and widths
        column_widths = {
            'Subject': 200,
            'Units': 80,
            'Rating': 80,
            'Final Grade': 100,
            'Status': 100,
            'Year Level': 100,
            'Term': 100
        }
        
        for col in columns:
            self.grades_tree.heading(col, text=col)
            self.grades_tree.column(col, width=column_widths[col])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(grades_frame, orient=tk.VERTICAL, command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.grades_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary Frame
        summary_frame = ttk.LabelFrame(main_container, text="Summary", padding="10")
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # GPA and Units
        gpa_frame = ttk.Frame(summary_frame)
        gpa_frame.pack(fill=tk.X, expand=True)
        
        ttk.Label(gpa_frame, text="GPA:").pack(side=tk.LEFT, padx=(0, 10))
        self.gpa_value = ttk.Label(gpa_frame, text="0.00")
        self.gpa_value.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(gpa_frame, text="Total Units:").pack(side=tk.LEFT, padx=(0, 10))
        self.units_value = ttk.Label(gpa_frame, text="0")
        self.units_value.pack(side=tk.LEFT)
        
        # Button Frame
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Refresh", 
                  command=lambda: self.load_student_grades(self.student_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Logout", 
                  command=self.app.logout).pack(side=tk.RIGHT, padx=5)

    def load_student_info(self):
        """Load and display student information."""
        try:
            student_info = get_student_info(self.student_id)
            if student_info:
                student_id, name, mobile, email, year, term, college, program, school_year, status = student_info
                
                # Update labels with student information
                self.id_label.config(text=f"Student ID: {student_id}")
                self.name_label.config(text=f"Name: {name}")
                self.college_label.config(text=f"College: {college}")
                self.program_label.config(text=f"Program: {program}")
                self.year_label.config(text=f"Year Level: {year}")
                self.term_label.config(text=f"Term: {term}")
                self.school_year_label.config(text=f"School Year: {school_year}")
                self.status_label.config(text=f"Status: {status}")
                self.email_label.config(text=f"Email: {email}")
                self.mobile_label.config(text=f"Mobile: {mobile}")
            else:
                messagebox.showerror("Error", "Failed to load student information")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_student_grades(self, student_id):
        """Load and display student grades in the treeview."""
        # Clear existing items
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        # Fetch and display grades
        grades = fetch_student_grades(student_id)
        total_units = 0
        total_rating = 0
        
        for grade in grades:
            self.grades_tree.insert("", tk.END, values=grade)
            units = float(grade[1])
            rating = float(grade[2])
            total_units += units
            total_rating += units * rating
        
        # Update summary
        if total_units > 0:
            gpa = total_rating / total_units
            self.gpa_value.config(text=f"{gpa:.2f}")
            self.units_value.config(text=str(total_units))
        else:
            self.gpa_value.config(text="N/A")
            self.units_value.config(text="0")

class RegistrarDashboardNew(ttk.Frame):
    """Dashboard screen for registrars with enhanced functionality."""
    
    def __init__(self, root, registrar_number, app):
        super().__init__(root)
        self.root = root
        self.registrar_number = registrar_number
        self.app = app
        
        self.create_widgets()
        self.populate_treeview_from_db()
    
    def create_widgets(self):
        """Create dashboard widgets."""
        # Title
        title_label = ttk.Label(self, text="Registrar Dashboard", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)

        # Search Frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_students).pack(side=tk.LEFT)
        
        # Student List Frame
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ('ID', 'Name', 'Mobile', 'Email', 'Year', 'Term', 'College', 'Program', 'School Year', 'Status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        column_widths = {
            'ID': 100,
            'Name': 200,
            'Mobile': 120,
            'Email': 200,
            'Year': 80,
            'Term': 80,
            'College': 150,
            'Program': 150,
            'School Year': 100,
            'Status': 100
        }
        
        # Set column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate tree with data
        self.populate_treeview_from_db()
        
        # Button Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # CRUD Buttons
        ttk.Button(btn_frame, text="Add Student", 
                  command=self.show_add_student_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Student", 
                  command=self.show_edit_student_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Student", 
                  command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Manage Grades", 
                  command=self.show_manage_grades_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", 
                  command=self.populate_treeview_from_db).pack(side=tk.LEFT, padx=5)
        
        # Logout Button
        ttk.Button(btn_frame, text="Logout", 
                  command=self.app.logout).pack(side=tk.RIGHT, padx=5)

    def show_add_student_dialog(self):
        """Show dialog for adding a new student."""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Student")
        dialog.geometry("400x650")
        dialog.resizable(False, False)
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form fields
        fields = {}
        row = 0
        
        # Basic Information
        ttk.Label(main_frame, text="Basic Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky='w')
        row += 1
        
        # Student ID
        ttk.Label(main_frame, text="Student Number *").grid(row=row, column=0, sticky='w')
        fields['student_id'] = ttk.Entry(main_frame, width=30)
        fields['student_id'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Name
        ttk.Label(main_frame, text="Full Name *").grid(row=row, column=0, sticky='w')
        fields['name'] = ttk.Entry(main_frame, width=30)
        fields['name'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Contact Information
        row += 1
        ttk.Label(main_frame, text="Contact Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky='w')
        row += 1
        
        # Mobile
        ttk.Label(main_frame, text="Mobile Number *").grid(row=row, column=0, sticky='w')
        fields['mobile_number'] = ttk.Entry(main_frame, width=30)
        fields['mobile_number'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Email
        ttk.Label(main_frame, text="Email Address *").grid(row=row, column=0, sticky='w')
        fields['email_address'] = ttk.Entry(main_frame, width=30)
        fields['email_address'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Academic Information
        row += 1
        ttk.Label(main_frame, text="Academic Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky='w')
        row += 1
        
        # College dropdown
        ttk.Label(main_frame, text="College *").grid(row=row, column=0, sticky='w')
        colleges = ['COMPUTER STUDIES', 'ENGINEERING', 'BUSINESS', 'ARTS AND SCIENCES', 'EDUCATION', 'HOSPITALITY']
        fields['college'] = ttk.Combobox(main_frame, values=colleges, width=27, state='readonly')
        fields['college'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Program/Course
        ttk.Label(main_frame, text="Program *").grid(row=row, column=0, sticky='w')
        fields['program'] = ttk.Combobox(main_frame, width=27, state='readonly')
        fields['program'].grid(row=row, column=1, pady=5, sticky='w')

        def update_programs(*args):
            college = fields['college'].get()
            if college == 'COMPUTER STUDIES':
                programs = ['BSIT - Bachelor of Science in Information Technology',
                           'BSCS - Bachelor of Science in Computer Science',
                           'BSCSAI - Bachelor of Science in Computer Science with AI']
            elif college == 'BUSINESS':
                programs = ['BSBA - Bachelor of Science in Business Administration',
                           'BSA - Bachelor of Science in Accountancy',
                           'BSMA - Bachelor of Science in Management Accounting']
            elif college == 'EDUCATION':
                programs = ['BSEd - Bachelor of Science in Education (Elementary)',
                           'BSEd - Bachelor of Science in Education (Secondary)',
                           'BEEd - Bachelor of Elementary Education']
            elif college == 'HOSPITALITY':
                programs = ['BSHRM - Bachelor of Science in Hotel & Restaurant Management',
                           'BSTM - Bachelor of Science in Tourism Management',
                           'BSHm - Bachelor of Science in Hospitality Management']
            elif college == 'ENGINEERING':
                programs = ['BSCE - Bachelor of Science in Civil Engineering',
                           'BSEE - Bachelor of Science in Electrical Engineering',
                           'BSME - Bachelor of Science in Mechanical Engineering']
            else:  # ARTS AND SCIENCES
                programs = ['BA COM - Bachelor of Arts in Communication',
                           'BA PSY - Bachelor of Arts in Psychology',
                           'BS PSY - Bachelor of Science in Psychology']
            fields['program']['values'] = programs
        
        fields['college'].bind('<<ComboboxSelected>>', update_programs)
        row += 1
        
        # Year Level
        ttk.Label(main_frame, text="Year Level *").grid(row=row, column=0, sticky='w')
        fields['year_level'] = ttk.Combobox(main_frame, values=['1', '2', '3', '4', '5'], width=27, state='readonly')
        fields['year_level'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Semester
        ttk.Label(main_frame, text="Term *").grid(row=row, column=0, sticky='w')
        fields['semester'] = ttk.Combobox(main_frame, values=['1', '2', '3'], width=27, state='readonly')
        fields['semester'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # School Year
        ttk.Label(main_frame, text="School Year *").grid(row=row, column=0, sticky='w')
        current_year = 2024
        school_years = [f"{year}-{year+1}" for year in range(current_year-5, current_year+5)]
        fields['school_year'] = ttk.Combobox(main_frame, values=school_years, width=27, state='readonly')
        fields['school_year'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Status
        ttk.Label(main_frame, text="Status *").grid(row=row, column=0, sticky='w')
        fields['enrollment_status'] = ttk.Combobox(main_frame, values=['Enrolled', 'Not Enrolled', 'LOA', 'Graduated'], width=27, state='readonly')
        fields['enrollment_status'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Password
        row += 1
        ttk.Label(main_frame, text="Account Security", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky='w')
        row += 1
        
        ttk.Label(main_frame, text="Password *").grid(row=row, column=0, sticky='w')
        fields['password'] = ttk.Entry(main_frame, width=30, show="*")
        fields['password'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        ttk.Label(main_frame, text="Confirm Password *").grid(row=row, column=0, sticky='w')
        fields['confirm_password'] = ttk.Entry(main_frame, width=30, show="*")
        fields['confirm_password'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=lambda: self.add_student(fields, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center the dialog on screen
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()
    
    def add_student(self, fields, dialog):
        """Add a new student to the database."""
        # Validate required fields
        required_fields = {
            'student_id': 'Student ID',
            'name': 'Full Name',
            'mobile_number': 'Mobile Number',
            'email_address': 'Email Address',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
            'college': 'College',
            'program': 'Program',
            'year_level': 'Year Level',
            'semester': 'Term',
            'school_year': 'School Year',
            'enrollment_status': 'Status'
        }
        
        # Check for empty fields
        for field, label in required_fields.items():
            if not fields[field].get().strip():
                messagebox.showwarning("Input Error", f"{label} is required!")
                return
        
        # Validate password match
        if fields['password'].get() != fields['confirm_password'].get():
            messagebox.showwarning("Input Error", "Passwords do not match!")
            return
        
        # Validate email format
        email = fields['email_address'].get().strip()
        if not validate_email(email):
            messagebox.showwarning("Input Error", "Invalid email format! Must end with @eecp.edu.ph")
            return
        
        # Validate mobile number
        mobile = fields['mobile_number'].get().strip()
        if len(mobile) != 11:
            messagebox.showwarning("Input Error", "Mobile number must be exactly 11 digits!")
            return
        if not mobile.startswith('09'):
            messagebox.showwarning("Input Error", "Mobile number must start with '09'!")
            return
        if not mobile[2:].isdigit():
            messagebox.showwarning("Input Error", "Mobile number must contain only digits!")
            return
        
        try:
            # Get all field values
            success = insert_user_data_st(
                student_number=fields['student_id'].get().strip(),
                name=fields['name'].get().strip().upper(),
                mobile_number=fields['mobile_number'].get().strip(),
                email_address=fields['email_address'].get().strip().lower(),
                password=fields['password'].get(),
                college=fields['college'].get().strip(),
                program=fields['program'].get().strip(),
                year_level=fields['year_level'].get().strip(),
                semester=fields['semester'].get().strip(),
                school_year=fields['school_year'].get().strip(),
                enrollment_status=fields['enrollment_status'].get().strip()
            )
            
            if success:
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                self.populate_treeview_from_db()
            else:
                messagebox.showerror("Error", "Failed to add student. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_students(self):
        """Search students based on the search entry text"""
        search_text = self.search_var.get().strip().upper()
        
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Get all students
            students = fetch_student_data()
            
            # Filter and display matching students
            for student in students:
                student_id, name, mobile, email, year, term, college, program, school_year, status = student
                
                # Check if search text matches any field
                if (search_text in str(student_id).upper() or
                    search_text in str(name).upper() or
                    search_text in str(mobile).upper() or
                    search_text in str(email).upper() or
                    search_text in str(college).upper() or
                    search_text in str(program).upper() or
                    search_text in str(status).upper()):
                    
                    self.tree.insert('', 'end', values=(
                        student_id, name, mobile, email,
                        year, term, college, program,
                        school_year, status
                    ))
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    def populate_treeview_from_db(self):
        """Populate the treeview with student data from the database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch and insert student data
        students = fetch_student_data()
        for student in students:
            self.tree.insert('', 'end', values=student)

    def show_edit_student_dialog(self):
        """Show dialog for editing student information."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student to edit!")
            return
        
        student_values = self.tree.item(selected[0])['values']
        student_id = student_values[0]
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Student Information")
        dialog.geometry("400x650")
        dialog.resizable(False, False)
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form fields
        fields = {}
        row = 0
        
        # Basic Information
        ttk.Label(main_frame, text="Basic Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky='w')
        row += 1
        
        # Student ID (readonly)
        ttk.Label(main_frame, text="Student Number").grid(row=row, column=0, sticky='w')
        fields['student_id'] = ttk.Entry(main_frame, width=30, state='readonly')
        fields['student_id'].grid(row=row, column=1, pady=5, sticky='w')
        fields['student_id'].configure(state='normal')
        fields['student_id'].insert(0, student_values[0])
        fields['student_id'].configure(state='readonly')
        row += 1
        
        # Name
        ttk.Label(main_frame, text="Full Name *").grid(row=row, column=0, sticky='w')
        fields['name'] = ttk.Entry(main_frame, width=30)
        fields['name'].grid(row=row, column=1, pady=5, sticky='w')
        fields['name'].insert(0, student_values[1])
        row += 1
        
        # Contact Information
        row += 1
        ttk.Label(main_frame, text="Contact Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky='w')
        row += 1
        
        # Mobile
        ttk.Label(main_frame, text="Mobile Number *").grid(row=row, column=0, sticky='w')
        fields['mobile_number'] = ttk.Entry(main_frame, width=30)
        fields['mobile_number'].grid(row=row, column=1, pady=5, sticky='w')
        fields['mobile_number'].insert(0, student_values[2])  # Updated index
        row += 1
        
        # Email
        ttk.Label(main_frame, text="Email Address *").grid(row=row, column=0, sticky='w')
        fields['email_address'] = ttk.Entry(main_frame, width=30)
        fields['email_address'].grid(row=row, column=1, pady=5, sticky='w')
        fields['email_address'].insert(0, student_values[3])  # Updated index
        row += 1
        
        # Academic Information
        row += 1
        ttk.Label(main_frame, text="Academic Information", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky='w')
        row += 1
        
        # College dropdown
        ttk.Label(main_frame, text="College *").grid(row=row, column=0, sticky='w')
        colleges = ['COMPUTER STUDIES', 'ENGINEERING', 'BUSINESS', 'ARTS AND SCIENCES', 'EDUCATION', 'HOSPITALITY']
        fields['college'] = ttk.Combobox(main_frame, values=colleges, width=27, state='readonly')
        fields['college'].grid(row=row, column=1, pady=5, sticky='w')
        fields['college'].set(student_values[6])
        row += 1
        
        # Program/Course
        ttk.Label(main_frame, text="Program *").grid(row=row, column=0, sticky='w')
        fields['program'] = ttk.Combobox(main_frame, width=27, state='readonly')
        fields['program'].grid(row=row, column=1, pady=5, sticky='w')
        
        def update_programs(*args):
            college = fields['college'].get()
            if college == 'COMPUTER STUDIES':
                programs = ['BSIT - Bachelor of Science in Information Technology',
                           'BSCS - Bachelor of Science in Computer Science',
                           'BSCSAI - Bachelor of Science in Computer Science with AI']
            elif college == 'BUSINESS':
                programs = ['BSBA - Bachelor of Science in Business Administration',
                           'BSA - Bachelor of Science in Accountancy',
                           'BSMA - Bachelor of Science in Management Accounting']
            elif college == 'EDUCATION':
                programs = ['BSEd - Bachelor of Science in Education (Elementary)',
                           'BSEd - Bachelor of Science in Education (Secondary)',
                           'BEEd - Bachelor of Elementary Education']
            elif college == 'HOSPITALITY':
                programs = ['BSHRM - Bachelor of Science in Hotel & Restaurant Management',
                           'BSTM - Bachelor of Science in Tourism Management',
                           'BSHm - Bachelor of Science in Hospitality Management']
            elif college == 'ENGINEERING':
                programs = ['BSCE - Bachelor of Science in Civil Engineering',
                           'BSEE - Bachelor of Science in Electrical Engineering',
                           'BSME - Bachelor of Science in Mechanical Engineering']
            else:  # ARTS AND SCIENCES
                programs = ['BA COM - Bachelor of Arts in Communication',
                           'BA PSY - Bachelor of Arts in Psychology',
                           'BS PSY - Bachelor of Science in Psychology']
            fields['program']['values'] = programs
        
        fields['college'].bind('<<ComboboxSelected>>', update_programs)
        
        # Set initial program and trigger update
        fields['college'].set(student_values[6])
        update_programs()
        fields['program'].set(student_values[7])
        row += 1
        
        # Year Level
        ttk.Label(main_frame, text="Year Level *").grid(row=row, column=0, sticky='w')
        fields['year_level'] = ttk.Combobox(main_frame, values=['1', '2', '3', '4', '5'], width=27, state='readonly')
        fields['year_level'].grid(row=row, column=1, pady=5, sticky='w')
        fields['year_level'].set(student_values[4])
        row += 1
        
        # Semester
        ttk.Label(main_frame, text="Term *").grid(row=row, column=0, sticky='w')
        fields['semester'] = ttk.Combobox(main_frame, values=['1', '2', '3'], width=27, state='readonly')
        fields['semester'].grid(row=row, column=1, pady=5, sticky='w')
        fields['semester'].set(student_values[5])
        row += 1
        
        # School Year
        ttk.Label(main_frame, text="School Year *").grid(row=row, column=0, sticky='w')
        current_year = 2024
        school_years = [f"{year}-{year+1}" for year in range(current_year-5, current_year+5)]
        fields['school_year'] = ttk.Combobox(main_frame, values=school_years, width=27, state='readonly')
        fields['school_year'].grid(row=row, column=1, pady=5, sticky='w')
        fields['school_year'].set(student_values[8])
        row += 1
        
        # Status
        ttk.Label(main_frame, text="Status *").grid(row=row, column=0, sticky='w')
        fields['enrollment_status'] = ttk.Combobox(main_frame, values=['Enrolled', 'Not Enrolled', 'LOA', 'Graduated'], width=27, state='readonly')
        fields['enrollment_status'].grid(row=row, column=1, pady=5, sticky='w')
        fields['enrollment_status'].set(student_values[9])
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=lambda: self.update_student(fields, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center dialog and make it modal
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()
    
    def update_student(self, fields, dialog):
        """Update student information."""
        # Validate required fields
        required_fields = {
            'name': 'Full Name',
            'mobile_number': 'Mobile Number',
            'email_address': 'Email Address',
            'college': 'College',
            'program': 'Program',
            'year_level': 'Year Level',
            'semester': 'Term',
            'school_year': 'School Year',
            'enrollment_status': 'Status'
        }
        
        # Check for empty fields
        for field, label in required_fields.items():
            if not fields[field].get().strip():
                messagebox.showwarning("Input Error", f"{label} is required!")
                return
        
        # Validate email format
        email = fields['email_address'].get().strip()
        if not validate_email(email):
            messagebox.showwarning("Input Error", "Invalid email format! Must end with @eecp.edu.ph")
            return
        
        # Validate mobile number
        mobile = fields['mobile_number'].get().strip()
        if len(mobile) != 11:
            messagebox.showwarning("Input Error", "Mobile number must be exactly 11 digits!")
            return
        if not mobile.startswith('09'):
            messagebox.showwarning("Input Error", "Mobile number must start with '09'!")
            return
        if not mobile[2:].isdigit():
            messagebox.showwarning("Input Error", "Mobile number must contain only digits!")
            return
        
        try:
            # Get all field values
            student_data = {
                'student_id': fields['student_id'].get().strip(),
                'name': fields['name'].get().strip().upper(),
                'mobile_number': fields['mobile_number'].get().strip(),
                'email_address': fields['email_address'].get().strip().lower(),
                'college': fields['college'].get().strip(),
                'program': fields['program'].get().strip(),
                'year_level': fields['year_level'].get().strip(),
                'semester': fields['semester'].get().strip(),
                'school_year': fields['school_year'].get().strip(),
                'enrollment_status': fields['enrollment_status'].get().strip()
            }
            
            # Update in database
            success = update_student_data(**student_data)
            
            if success:
                messagebox.showinfo("Success", "Student information updated successfully!")
                dialog.destroy()
                self.populate_treeview_from_db()
            else:
                messagebox.showerror("Error", "Failed to update student information. Please try again.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_manage_grades_dialog(self):
        """Show dialog for managing student grades."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student first!")
            return
        
        student_id = self.tree.item(selected[0])['values'][0]
        student_name = self.tree.item(selected[0])['values'][1]
        
        dialog = tk.Toplevel(self)
        dialog.title(f"Manage Grades - {student_name}")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student info header
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Student: {student_name}", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"ID: {student_id}", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=20)
        
        # Grades treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Subject', 'Units', 'Rating', 'Final Grade', 'Status', 'Year Level', 'Semester')
        self.grades_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configure columns
        self.grades_tree.heading('Subject', text='Subject', anchor=tk.W)
        self.grades_tree.heading('Units', text='Units', anchor=tk.CENTER)
        self.grades_tree.heading('Rating', text='Rating', anchor=tk.CENTER)
        self.grades_tree.heading('Final Grade', text='Final Grade', anchor=tk.CENTER)
        self.grades_tree.heading('Status', text='Status', anchor=tk.CENTER)
        self.grades_tree.heading('Year Level', text='Year Level', anchor=tk.CENTER)
        self.grades_tree.heading('Semester', text='Semester', anchor=tk.CENTER)
        
        # Set column widths and alignment
        self.grades_tree.column('Subject', width=200, anchor=tk.W)
        self.grades_tree.column('Units', width=70, anchor=tk.CENTER)
        self.grades_tree.column('Rating', width=70, anchor=tk.CENTER)
        self.grades_tree.column('Final Grade', width=100, anchor=tk.CENTER)
        self.grades_tree.column('Status', width=100, anchor=tk.CENTER)
        self.grades_tree.column('Year Level', width=100, anchor=tk.CENTER)
        self.grades_tree.column('Semester', width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.grades_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Add Grade", 
                  command=lambda: self.show_add_edit_grade_dialog(student_id, False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Grade", 
                  command=lambda: self.show_add_edit_grade_dialog(student_id, True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Grade", 
                  command=lambda: self.delete_selected_grade(student_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Load grades
        self.refresh_grades(student_id)
        
        # Center dialog and make it modal
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()
    
    def show_add_edit_grade_dialog(self, student_id, edit_mode=False):
        """Show dialog for adding or editing a grade."""
        if edit_mode and not self.grades_tree.selection():
            messagebox.showwarning("Selection Required", "Please select a grade to edit!")
            return
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Grade" if edit_mode else "Add Grade")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form fields
        fields = {}
        row = 0
        
        # Subject
        ttk.Label(main_frame, text="Subject *").grid(row=row, column=0, sticky='w')
        fields['subject'] = ttk.Entry(main_frame, width=30)
        fields['subject'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Units
        ttk.Label(main_frame, text="Units *").grid(row=row, column=0, sticky='w')
        fields['units'] = ttk.Combobox(main_frame, values=['1', '2', '3', '4', '5', '6'], width=27, state='readonly')
        fields['units'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Rating
        ttk.Label(main_frame, text="Rating *").grid(row=row, column=0, sticky='w')
        ratings = ['1.00', '1.25', '1.50', '1.75', '2.00', '2.25', '2.50', '2.75', '3.00', '5.00']
        fields['rating'] = ttk.Combobox(main_frame, values=ratings, width=27, state='readonly')
        fields['rating'].grid(row=row, column=1, pady=5, sticky='w')
        
        def update_status(*args):
            rating = fields['rating'].get()
            if rating:
                rating_float = float(rating)
                status = 'Passed' if rating_float < 3.0 else 'Failed'
                fields['status'].set(status)
        
        fields['rating'].bind('<<ComboboxSelected>>', update_status)
        row += 1
        
        # Final Grade (same as rating)
        ttk.Label(main_frame, text="Final Grade *").grid(row=row, column=0, sticky='w')
        fields['final_grade'] = ttk.Entry(main_frame, width=30, state='readonly')
        fields['final_grade'].grid(row=row, column=1, pady=5, sticky='w')
        
        def update_final_grade(*args):
            rating = fields['rating'].get()
            if rating:
                fields['final_grade'].configure(state='normal')
                fields['final_grade'].delete(0, tk.END)
                fields['final_grade'].insert(0, rating)
                fields['final_grade'].configure(state='readonly')
        
        fields['rating'].bind('<<ComboboxSelected>>', lambda e: [update_status(), update_final_grade()])
        row += 1
        
        # Status
        ttk.Label(main_frame, text="Status *").grid(row=row, column=0, sticky='w')
        fields['status'] = ttk.Combobox(main_frame, values=['Passed', 'Failed'], width=27, state='readonly')
        fields['status'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Year Level
        ttk.Label(main_frame, text="Year Level *").grid(row=row, column=0, sticky='w')
        fields['year_level'] = ttk.Combobox(main_frame, values=['1', '2', '3', '4', '5'], width=27, state='readonly')
        fields['year_level'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Semester
        ttk.Label(main_frame, text="Semester *").grid(row=row, column=0, sticky='w')
        fields['semester'] = ttk.Combobox(main_frame, values=['1', '2', '3'], width=27, state='readonly')
        fields['semester'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # If editing, populate fields
        if edit_mode:
            selected = self.grades_tree.item(self.grades_tree.selection()[0])['values']
            fields['subject'].insert(0, selected[0])
            fields['units'].set(str(selected[1]))
            fields['rating'].set(str(selected[2]))
            fields['final_grade'].configure(state='normal')
            fields['final_grade'].insert(0, str(selected[3]))
            fields['final_grade'].configure(state='readonly')
            fields['status'].set(selected[4])
            fields['year_level'].set(str(selected[5]))
            fields['semester'].set(str(selected[6]))
            fields['subject'].configure(state='readonly')  # Can't change subject when editing
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        save_command = lambda: self.update_grade(student_id, fields, dialog) if edit_mode else self.add_grade(student_id, fields, dialog)
        ttk.Button(button_frame, text="Save", command=save_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center dialog and make it modal
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()
    
    def refresh_grades(self, student_id):
        """Refresh the grades treeview."""
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        grades = fetch_student_grades(student_id)
        for grade in grades:
            self.grades_tree.insert('', 'end', values=grade)
    
    def add_grade(self, student_id, fields, dialog):
        """Add a grade for the selected student."""
        values = {field: widget.get() for field, widget in fields.items()}
        
        try:
            # Get all field values
            update_grade(
                student_id, values['subject'],
                float(values['rating']), int(values['units']),
                values['final_grade'], values['status'],
                1, 1  # TODO: Get current year and semester
            )
            messagebox.showinfo("Success", "Grade added successfully!")
            
            # Refresh grades display
            self.refresh_grades(student_id)
            
            # Clear entry fields
            for widget in fields.values():
                if hasattr(widget, 'delete'):
                    widget.delete(0, tk.END)
                else:
                    widget.set('')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add grade: {str(e)}")
    
    def update_grade(self, student_id, fields, dialog):
        """Update the selected grade."""
        selected = self.grades_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a grade to update.")
            return
        
        values = {field: widget.get() for field, widget in fields.items()}
        
        try:
            # Get all field values
            update_grade(
                student_id, values['subject'],
                float(values['rating']), int(values['units']),
                values['final_grade'], values['status'],
                1, 1  # TODO: Get current year and semester
            )
            messagebox.showinfo("Success", "Grade updated successfully!")
            
            # Refresh grades display
            self.refresh_grades(student_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update grade: {str(e)}")
    
    def delete_selected_grade(self, student_id):
        """Delete the selected grade."""
        selected = self.grades_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a grade to delete.")
            return
        
        grade_values = self.grades_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete this grade?\n\nSubject: {grade_values[0]}\nYear Level: {grade_values[5]}\nSemester: {grade_values[6]}"):
            try:
                delete_grade(
                    student_id=student_id,
                    subject=grade_values[0],
                    year_level=grade_values[5],
                    semester=grade_values[6]
                )
                
                messagebox.showinfo("Success", "Grade deleted successfully!")
                
                # Refresh grades display
                self.refresh_grades(student_id)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete grade: {str(e)}")

    def delete_student(self):
        """Delete selected student."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", 
                                 "Please select a student to delete.")
            return
        
        student_id = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                             "Are you sure you want to delete this student?"):
            try:
                delete_student(student_id)
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.populate_treeview_from_db()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
