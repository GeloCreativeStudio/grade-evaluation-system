
from student import Student

class Registrar:
    @staticmethod
    def menu():
        print("\nRegistrar Portal")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            Registrar.login()
        elif choice == "2":
            print("Sign-up functionality not yet implemented.")
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

    @staticmethod
    def login():
        print("Registrar login (For simplicity, no password required).")
        Registrar.dashboard()

    @staticmethod
    def dashboard():
        while True:
            print("\nRegistrar Dashboard")
            print("1. Search Student")
            print("2. Edit Grades")
            print("3. Log Out")
            choice = input("Choose an option: ")

            if choice == "1":
                Registrar.search_student()
            elif choice == "2":
                Registrar.edit_grades()
            elif choice == "3":
                print("Logged out.")
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def search_student():
        student_id = input("Enter Student ID: ")
        if student_id in Student.students_db:
            student = Student.students_db[student_id]
            print(f"Student Found: {student['name']}")
            print(student["grades"])
        else:
            print("Student not found.")

    @staticmethod
    def edit_grades():
        student_id = input("Enter Student ID to edit grades: ")
        if student_id in Student.students_db:
            subject = input("Enter subject to edit: ")
            if subject in Student.subjects:
                grade = float(input("Enter new grade: "))
                units = Student.subjects[subject]["Units"]
                Student.students_db[student_id]["grades"][subject] = {"Grade": grade, "Units": units}
                print(f"Grade updated for {subject}.")
            else:
                print("Subject not found.")
        else:
            print("Student not found.")
