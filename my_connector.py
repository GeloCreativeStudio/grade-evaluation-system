import sqlite3
from tkinter import *
from tkinter import messagebox


# Connect to your existing database (if you already have it in DB Browser)
def connect_to_db():
    conn = sqlite3.connect('path_to_your_existing_database.db')  # Replace with your database file path
    return conn


# Sign-up functions for student and registrar
def student_signup(username, password, full_name, age):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert student data into the students table
    try:
        cursor.execute('''
            INSERT INTO students (username, password, full_name, age)
            VALUES (?, ?, ?, ?)
        ''', (username, password, full_name, age))
        conn.commit()
        messagebox.showinfo("Success", "Student account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

    conn.close()


def registrar_signup(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert registrar data into the registrars table
    try:
        cursor.execute('''
            INSERT INTO registrars (username, password)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registrar account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

    conn.close()


# Login functions for student and registrar
def student_login(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Check if student exists
    cursor.execute('SELECT * FROM students WHERE username = ? AND password = ?', (username, password))
    student = cursor.fetchone()

    if student:
        messagebox.showinfo("Success", f"Welcome, {student[2]}!")
        conn.close()
        return True
    else:
        messagebox.showerror("Error", "Invalid username or password")
        conn.close()
        return False


def registrar_login(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Check if registrar exists
    cursor.execute('SELECT * FROM registrars WHERE username = ? AND password = ?', (username, password))
    registrar = cursor.fetchone()

    if registrar:
        messagebox.showinfo("Success", "Welcome, Registrar!")
        conn.close()
        return True
    else:
        messagebox.showerror("Error", "Invalid username or password")
        conn.close()
        return False


# Student Form (View Only)
def student_form(username):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Get student details
    cursor.execute('SELECT * FROM students WHERE username = ?', (username,))
    student = cursor.fetchone()

    if student:
        # Display student details in the form (read-only)
        student_details = f"Name: {student[2]}\nAge: {student[4]}"
        messagebox.showinfo("Student Details", student_details)
    else:
        messagebox.showerror("Error", "Student not found!")

    conn.close()


# Registrar Form (For Editing Student Data)
def registrar_form():
    def edit_student_data():
        username = entry_username.get()
        full_name = entry_full_name.get()
        age = entry_age.get()

        conn = connect_to_db()
        cursor = conn.cursor()

        # Update student information
        cursor.execute('''
            UPDATE students
            SET full_name = ?, age = ?
            WHERE username = ?
        ''', (full_name, age, username))
        conn.commit()

        messagebox.showinfo("Success", "Student data updated successfully!")

        conn.close()

    # Creating the registrar form
    registrar_form = Tk()
    registrar_form.title("Registrar Form")

    Label(registrar_form, text="Username:").pack()
    entry_username = Entry(registrar_form)
    entry_username.pack()

    Label(registrar_form, text="Full Name:").pack()
    entry_full_name = Entry(registrar_form)
    entry_full_name.pack()

    Label(registrar_form, text="Age:").pack()
    entry_age = Entry(registrar_form)
    entry_age.pack()

    Button(registrar_form, text="Update Student", command=edit_student_data).pack()

    registrar_form.mainloop()


# Tkinter GUI for Login and Signup
def show_login_window():
    def student_login_action():
        username = entry_username.get()
        password = entry_password.get()
        if student_login(username, password):
            student_form(username)

    def registrar_login_action():
        username = entry_username.get()
        password = entry_password.get()
        if registrar_login(username, password):
            registrar_form()

    login_window = Tk()
    login_window.title("Login")

    Label(login_window, text="Username:").pack()
    entry_username = Entry(login_window)
    entry_username.pack()

    Label(login_window, text="Password:").pack()
    entry_password = Entry(login_window, show="*")
    entry_password.pack()

    Button(login_window, text="Student Login", command=student_login_action).pack()
    Button(login_window, text="Registrar Login", command=registrar_login_action).pack()

    login_window.mainloop()


# Main function to initialize database and show login window
if __name__ == "__main__":
    show_login_window()