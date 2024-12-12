"""
Authentication screens for the Grade Evaluation System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from ..database.database_operations import fetch_user_credentials, fetch_user_credentials2, insert_user_dataR
from ..utils.form_utilities import validate_email, validate_mobile
from .ui_components import (
    COLORS, 
    STYLES, 
    create_title_bar,
    create_card,
    create_button,
    create_entry
)

class LoginScreen(ttk.Frame):
    """Login screen for EECP GESYS."""
    
    def __init__(self, root, nav_manager, app):
        super().__init__(root)
        self.root = root
        self.nav_manager = nav_manager
        self.app = app
        
        self.configure(style='App.TFrame', padding=40)
        self.create_widgets()
    
    def create_widgets(self):
        """Create login screen widgets."""
        # Title bar
        create_title_bar(self, "Login")
        
        # Main container with padding and centering
        main_container = ttk.Frame(self, style='App.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Center the login card
        center_frame = ttk.Frame(main_container, style='App.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Login card with modern styling
        login_card = create_card(center_frame, padding=40)
        login_card.pack(padx=20, pady=20)
        
        # Welcome message
        welcome_label = ttk.Label(login_card, 
                                text="Welcome to EECP GESYS",
                                style='Heading.TLabel',
                                font=STYLES['subtitle'])
        welcome_label.pack(pady=(0, 30))
        
        # Login form with improved spacing
        form_frame = ttk.Frame(login_card, style='App.TFrame')
        form_frame.pack(pady=10)
        
        # Username field
        username_label = ttk.Label(form_frame,
                                 text="Username",
                                 style='App.TLabel',
                                 font=STYLES['body_bold'])
        username_label.pack(anchor='w', pady=(0, 5))
        self.username_entry = create_entry(form_frame)
        self.username_entry.pack(pady=(0, 20), ipady=5)
        
        # Password field
        password_label = ttk.Label(form_frame,
                                 text="Password",
                                 style='App.TLabel',
                                 font=STYLES['body_bold'])
        password_label.pack(anchor='w', pady=(0, 5))
        self.password_entry = create_entry(form_frame)
        self.password_entry.pack(pady=(0, 30), ipady=5)
        self.password_entry.configure(show='•')
        
        # User type selection
        self.user_type = tk.StringVar(value="student")
        
        type_frame = ttk.Frame(form_frame, style='App.TFrame')
        type_frame.pack(pady=(0, 20))
        
        ttk.Radiobutton(type_frame, text="Student", variable=self.user_type,
                       value="student", style='App.TRadiobutton').pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Registrar", variable=self.user_type,
                       value="registrar", style='App.TRadiobutton').pack(side=tk.LEFT, padx=10)
        
        # Login button with proper styling and positioning
        button_frame = ttk.Frame(form_frame, style='App.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        login_button = create_button(button_frame,
                                   "Login",
                                   self.login,
                                   is_primary=False)
        login_button.pack(fill=tk.X)
        
        # Register link
        register_frame = ttk.Frame(form_frame, style='App.TFrame')
        register_frame.pack(fill=tk.X)
        
        register_label = ttk.Label(register_frame,
                                 text="Don't have an account?",
                                 style='App.TLabel',
                                 font=STYLES['small'])
        register_label.pack(side=tk.LEFT)
        
        register_button = create_button(register_frame,
                                      "Register",
                                      self.show_register,
                                      is_primary=False)
        register_button.pack(side=tk.LEFT, padx=(10, 0))
    
    def login(self):
        """Handle login attempt."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_type = self.user_type.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if user_type == "student":
            user_data = fetch_user_credentials(username, password)
        else:
            user_data = fetch_user_credentials2(username, password)
        
        if user_data:
            self.app.current_user = user_data
            self.app.user_type = user_type
            # Create and show the appropriate dashboard
            self.app.create_dashboard(user_type, username)
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def show_register(self):
        """Show registration screen based on user type."""
        user_type = self.user_type.get()
        if user_type == "student":
            self.nav_manager("StudentSignupScreen")  
        else:
            self.nav_manager("RegistrarSignupScreen")

class RegistrarLoginScreen(ttk.Frame):
    """Login screen for registrars."""
    
    def __init__(self, root, nav_manager, app):
        super().__init__(root)
        self.root = root
        self.nav_manager = nav_manager
        self.app = app
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and setup the login screen widgets."""
        # Title
        title = ttk.Label(self, text="Registrar Login", font=STYLES['title'])
        title.pack(pady=20)
        
        # Login form
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Registrar Number:", font=STYLES['body_bold']).pack()
        self.registrar_number = create_entry(form_frame)
        self.registrar_number.pack(pady=(5, 15))
        
        ttk.Label(form_frame, text="Password:", font=STYLES['body_bold']).pack()
        self.password = create_entry(form_frame)
        self.password.configure(show="•")
        self.password.pack(pady=(5, 20))
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        
        create_button(btn_frame, "Login", self.login, is_primary=False).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Back", lambda: self.nav_manager("LoginScreen"), is_primary=False).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Sign Up", lambda: self.nav_manager("RegistrarSignupScreen"), is_primary=False).pack(side=tk.LEFT, padx=5)
    
    def login(self):
        """Handle login attempt."""
        registrar_number = self.registrar_number.get().strip()
        password = self.password.get().strip()
        
        if not registrar_number or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        user_data = fetch_user_credentials2(registrar_number, password)
        if user_data:
            self.app.current_user = user_data
            self.app.user_type = "registrar"
            self.app.create_dashboard("registrar", registrar_number)
        else:
            messagebox.showerror("Error", "Invalid credentials")

class StudentSignupScreen(tk.Frame):
    """Student signup screen."""
    def __init__(self, parent, nav_manager, app):
        super().__init__(parent)
        self.nav_manager = nav_manager
        self.app = app
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        """Create signup form widgets."""
        # Title
        tk.Label(self, text="Student Registration", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Form frame
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=5)

        # Form fields
        fields = [
            ('student_number', 'Student Number:'),
            ('name', 'Full Name:'),
            ('course', 'Course:'),
            ('mobile_number', 'Mobile Number:'),
            ('email_address', 'Email Address:'),
            ('password', 'Password:')
        ]

        # Create form entries
        for field, label in fields:
            frame = ttk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            if field == 'password':
                entry.config(show='*')
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[field] = entry

        # Buttons frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        # Sign Up button
        ttk.Button(btn_frame, text="Sign Up",
                  command=lambda: handle_student_signup(
                      self.entries, 
                      lambda: self.nav_manager("LoginScreen")
                  )).pack(pady=5)

        # Back to Login button
        ttk.Button(btn_frame, text="Back to Login",
                  command=lambda: self.nav_manager("LoginScreen")).pack()

class RegistrarSignupScreen(ttk.Frame):
    """Screen for registrar registration."""
    
    def __init__(self, parent, nav_manager, app):
        super().__init__(parent)
        self.nav_manager = nav_manager
        self.app = app
        self.entries = {}
        self.create_widgets()
        
    def create_widgets(self):
        """Create and setup all widgets for the registrar signup screen."""
        self.main_frame = self.create_registrar_signup_frame()
        
    def create_registrar_signup_frame(self):
        """Create registrar signup frame."""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Registrar Registration", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form fields
        fields = {}
        row = 0
        
        # Registrar ID
        ttk.Label(form_frame, text="Registrar ID *").grid(row=row, column=0, sticky='w')
        fields['registrar_number'] = ttk.Entry(form_frame, width=30)
        fields['registrar_number'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Name
        ttk.Label(form_frame, text="Full Name *").grid(row=row, column=0, sticky='w')
        fields['name'] = ttk.Entry(form_frame, width=30)
        fields['name'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Department
        ttk.Label(form_frame, text="Department *").grid(row=row, column=0, sticky='w')
        departments = ['REGISTRAR OFFICE', 'ACADEMIC AFFAIRS', 'STUDENT SERVICES', 'ADMISSIONS']
        fields['department'] = ttk.Combobox(form_frame, values=departments, width=27, state='readonly')
        fields['department'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Position
        ttk.Label(form_frame, text="Position *").grid(row=row, column=0, sticky='w')
        positions = ['REGISTRAR', 'ASSISTANT REGISTRAR', 'RECORDS OFFICER', 'ADMIN STAFF']
        fields['position'] = ttk.Combobox(form_frame, values=positions, width=27, state='readonly')
        fields['position'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Password
        ttk.Label(form_frame, text="Password *").grid(row=row, column=0, sticky='w')
        fields['password'] = ttk.Entry(form_frame, width=30, show="*")
        fields['password'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Confirm Password
        ttk.Label(form_frame, text="Confirm Password *").grid(row=row, column=0, sticky='w')
        fields['confirm_password'] = ttk.Entry(form_frame, width=30, show="*")
        fields['confirm_password'].grid(row=row, column=1, pady=5, sticky='w')
        row += 1
        
        # Buttons frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Register", 
                  command=lambda: self.register_registrar(fields)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Login", 
                  command=self.show_login).pack(side=tk.LEFT, padx=5)
        
        return main_frame
    
    def register_registrar(self, fields):
        """Handle registrar registration."""
        # Validate required fields
        required_fields = {
            'registrar_number': 'Registrar ID',
            'name': 'Full Name',
            'department': 'Department',
            'position': 'Position',
            'password': 'Password',
            'confirm_password': 'Confirm Password'
        }
        
        # Check for empty fields
        for field, label in required_fields.items():
            if not fields[field].get().strip():
                messagebox.showwarning("Input Error", f"{label} is required!")
                return
        
        # Validate registrar ID format (e.g., REG001)
        registrar_id = fields['registrar_number'].get().strip()
        if not re.match(r"^REG\d{3}$", registrar_id):
            messagebox.showwarning("Input Error", "Registrar ID must be in format 'REGxxx' where x is a digit!")
            return
        
        # Validate password match
        if fields['password'].get() != fields['confirm_password'].get():
            messagebox.showwarning("Input Error", "Passwords do not match!")
            return
        
        # Validate password strength
        password = fields['password'].get()
        if len(password) < 8:
            messagebox.showwarning("Input Error", "Password must be at least 8 characters long!")
            return
        
        try:
            # Insert into database
            success = insert_user_dataR(
                registrar_id=fields['registrar_number'].get().strip(),
                name=fields['name'].get().strip().upper(),
                password=fields['password'].get()
            )
            
            if success:
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.show_login()
            else:
                messagebox.showerror("Error", "Registration failed. Please try again.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_login(self):
        """Return to login screen."""
        self.nav_manager("LoginScreen")
