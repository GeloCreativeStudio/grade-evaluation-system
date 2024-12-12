import tkinter as tk
from tkinter import ttk, messagebox
import ttkthemes
from pymongo import MongoClient
import bcrypt
from PIL import Image, ImageTk

def connect_to_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client["grades_management"]
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to MongoDB: {e}")
        return None

db = connect_to_db()

def fetch_grades(student_id):
    if db:
        return list(db["grades"].find({"student_id": student_id}))
    return []

def add_student(student_data):
    if db:
        students_collection = db["students"]
        hashed_password = bcrypt.hashpw(
            student_data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        student_data["password"] = hashed_password
        students_collection.insert_one(student_data)
        messagebox.showinfo("Success", "Student added successfully!")

def authenticate_student(student_number, password):
    if db:
        student = db["students"].find_one({"student_number": student_number})
        if student:
            return student
    return None

class EECPApp(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("EECP Grade Evaluation System")
        self.set_theme("arc")

        self.frames = {}
        self.init_frames()
        self.show_frame("LoginFrame")

    def init_frames(self):
        for FrameClass in (LoginFrame, SignupFrame, GradesFrame):
            frame = FrameClass(parent=self)
            self.frames[FrameClass.__name__] = frame
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.bg_image = self.load_image("rsignup.jpg", parent.winfo_screenwidth(), parent.winfo_screenheight())
        self.canvas = tk.Canvas(self, width=parent.winfo_screenwidth(), height=parent.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        login_body = tk.Frame(
            self,
            bg="white",
            bd=2,
            relief="solid",
            highlightthickness=0,
        )
        login_body.place(relx=0.5, rely=0.5, anchor="center", width=450, height=400)

        self.canvas.create_rectangle(
            login_body.winfo_x() - 5,
            login_body.winfo_y() - 5,
            login_body.winfo_x() + 450 + 5,
            login_body.winfo_y() + 400 + 5,
            fill="gray80",
            outline="",
        )

        title_label = ttk.Label(
            login_body,
            text="Login",
            font=("Helvetica", 18, "bold"),
            background="white",
            anchor="center",
        )
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        self.add_input_field(login_body, "Student Number", 0.3)
        self.add_input_field(login_body, "Password", 0.45, show="*")

        self.add_login_button(login_body, 0.65)
        self.add_signup_button(login_body, 0.8)

    def add_input_field(self, parent_frame, label_text, rel_y, show=None):
        """Helper function to add a labeled input field."""
        label = ttk.Label(parent_frame, text=label_text, font=("Helvetica", 14), background="white")
        label.place(relx=0.1, rely=rel_y, anchor="w")

        entry = ttk.Entry(parent_frame, font=("Helvetica", 12), width=30, show=show)
        entry.place(relx=0.5, rely=rel_y, anchor="center")
        if label_text == "Student Number":
            self.student_number_entry = entry
        elif label_text == "Password":
            self.password_entry = entry

    def add_login_button(self, parent_frame, rel_y):
        """Helper function to add the login button."""
        login_button = ttk.Button(parent_frame, text="Login", command=self.login, style="Accent.TButton")
        login_button.place(relx=0.5, rely=rel_y, anchor="center")

    def add_signup_button(self, parent_frame, rel_y):
        """Helper function to add the signup button."""
        signup_button = ttk.Button(parent_frame, text="Sign Up", command=lambda: self.parent.show_frame("SignupFrame"))
        signup_button.place(relx=0.5, rely=rel_y, anchor="center")

    def login(self):
        student_number = self.student_number_entry.get()
        password = self.password_entry.get()
        user = authenticate_student(student_number, password)
        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {user['name']}!")
            self.parent.frames["GradesFrame"].populate_grades(student_number)
            self.parent.show_frame("GradesFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    @staticmethod
    def load_image(path, width, height):
        try:
            img = Image.open(path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Image Error", f"Unable to load image: {e}")
            return None

class SignupFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Sign Up for EECP", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white", pady=10).pack(
            fill="x"
        )
        signup_body = tk.Frame(self, pady=20)
        signup_body.pack()

        ttk.Label(signup_body, text="Name:", font=("Helvetica", 14)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.name_entry = ttk.Entry(signup_body, font=("Helvetica", 12), width=30)
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)

        ttk.Label(signup_body, text="Student Number:", font=("Helvetica", 14)).grid(
            row=1, column=0, padx=20, pady=10, sticky="w"
        )
        self.student_number_entry = ttk.Entry(signup_body, font=("Helvetica", 12), width=30)
        self.student_number_entry.grid(row=1, column=1, padx=20, pady=10)

        ttk.Label(signup_body, text="Password:", font=("Helvetica", 14)).grid(
            row=2, column=0, padx=20, pady=10, sticky="w"
        )
        self.password_entry = ttk.Entry(signup_body, font=("Helvetica", 12), show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=20, pady=10)

        ttk.Button(signup_body, text="Sign Up", command=self.register_student).grid(
            row=3, column=0, columnspan=2, pady=20
        )
        ttk.Button(signup_body, text="Back to Login", command=lambda: parent.show_frame("LoginFrame")).grid(
            row=4, column=0, columnspan=2, pady=5
        )

    def register_student(self):
        student_data = {
            "name": self.name_entry.get(),
            "student_number": self.student_number_entry.get(),
            "password": self.password_entry.get(),
        }
        if all(student_data.values()):
            add_student(student_data)
            self.parent.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", "All fields must be filled out!")

class GradesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Your Grades", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white", pady=10).pack(
            fill="x"
        )
        grades_body = tk.Frame(self, pady=20)
        grades_body.pack()

        self.tree = ttk.Treeview(
            grades_body, columns=("Course Number", "Subject", "Units", "Rating", "Final Grade", "Status"), show="headings"
        )
        self.tree.grid(row=0, column=0, columnspan=2, pady=20)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        ttk.Button(grades_body, text="Log Out", command=lambda: parent.show_frame("LoginFrame")).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    def populate_grades(self, student_id):
        for item in self.tree.get_children():
            self.tree.delete(item)
        grades = fetch_grades(student_id)
        for grade in grades:
            self.tree.insert(
                "", "end", values=(grade["course_id"], grade["subject"], grade["credits"], grade["rating"], grade["final_grade"], grade["status"])
            )

if __name__ == "__main__":
    app = EECPApp()
    app.mainloop()