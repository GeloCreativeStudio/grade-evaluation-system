"""
This module handles form-related utilities and functions for the Grade Evaluation System.
It includes functions for form handling, clearing forms, and entry field management.
"""

import re
from tkinter import messagebox
import logging
from .logger import logger
from .validation import validate_email, validate_mobile, validate_required_fields
import tkinter as tk

def on_entry_click(event, entry, default_text):
    """Handle click event on entry fields with placeholder text."""
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(foreground='black')

def on_focusout(event, entry, default_text):
    """Handle focus out event on entry fields with placeholder text."""
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(foreground='grey')

def clear_student_form(entries):
    """Clear all fields in the student registration form.
    
    Args:
        entries (dict): Dictionary containing entry widgets for the student form
    """
    for entry in entries.values():
        entry.delete(0, tk.END)

def clear_registrar_form(entries):
    """Clear all fields in the registrar registration form.
    
    Args:
        entries (dict): Dictionary containing entry widgets for the registrar form
    """
    for entry in entries.values():
        entry.delete(0, tk.END)

def handle_student_signup(entries, show_login_callback):
    """Handle student signup process."""
    from ..database.database_operations import insert_user_data_st
    required_fields = {
        'student_number': 'Student Number',
        'name': 'Full Name',
        'course': 'Course',
        'mobile_number': 'Mobile Number',
        'email_address': 'Email Address',
        'password': 'Password'
    }
    
    # Check for empty fields
    if not validate_required_fields(required_fields, entries):
        return
    
    # Validate email format
    email = entries['email_address'].get().strip()
    if not validate_email(email):
        messagebox.showwarning("Invalid email address format", "Invalid email address format")
        return
    
    # Validate mobile number (simple validation)
    mobile = entries['mobile_number'].get().strip()
    if not validate_mobile(mobile):
        messagebox.showwarning("Invalid mobile number", "Mobile number should contain only digits")
        return
    
    success = insert_user_data_st(
        student_number=entries['student_number'].get().strip(),
        name=entries['name'].get().strip(),
        course=entries['course'].get().strip(),
        mobile_number=entries['mobile_number'].get().strip(),
        email_address=entries['email_address'].get().strip(),
        password=entries['password'].get().strip()
    )

    if success:
        messagebox.showinfo("Success", "Student registration successful!")
        show_login_callback()
    else:
        messagebox.showerror("Error", "Failed to create account. Please try again.")

def handle_registrar_signup(entries, show_login_callback):
    """Handle registrar signup process.
    
    Args:
        entries (dict): Dictionary containing entry widgets for the registrar form
        show_login_callback (callable): Callback function to show login screen
    """
    from ..database.database_operations import insert_user_dataR
    required_fields = ['registrar_number', 'name', 'password']
    
    # Check if all fields are filled
    if not validate_required_fields(required_fields, entries):
        return
            
    success = insert_user_dataR(
        registrar_number=entries['registrar_number'].get(),
        name=entries['name'].get(),
        password=entries['password'].get()
    )

    if success:
        messagebox.showinfo("Success", "Sign-Up Successful!")
        clear_registrar_form(entries)
        show_login_callback()
    else:
        messagebox.showerror("Error", "Failed to create account. Please try again.")
