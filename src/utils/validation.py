"""
Validation utilities for the Grade Evaluation System.
"""

import re
from tkinter import messagebox

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return False
    return True

def validate_mobile(mobile):
    """Validate mobile number format."""
    pattern = r'^\d{10}$'
    if not re.match(pattern, mobile):
        messagebox.showerror("Invalid Mobile", "Please enter a valid 10-digit mobile number.")
        return False
    return True

def validate_required_fields(fields):
    """Validate that all required fields are filled."""
    for field_name, field_value in fields.items():
        if not field_value:
            messagebox.showerror("Required Field", f"{field_name} is required.")
            return False
    return True
