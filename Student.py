# student.py

class Student:
    students_db = {}
    subjects = {
        "Math": {"Year": 1, "Semester": 1, "Units": 3},
        "Science": {"Year": 1, "Semester": 1, "Units": 4},
    }

    @staticmethod
    def menu():
        print("\nStudent Portal")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            Student.login()
        elif choice == "2":
            Student.signup()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

    @staticmethod
    def signup():
        name = input("Enter your name: ")
        student_id = input("Enter a unique student ID: ")
        if student_id in Student.students_db:
            print("Student ID already exists. Try logging in.")
            return
        Student.students_db[student_id] = {"name": name, "grades": {}}
        print(f"Account created for {name}!")

    @staticmethod
    def login():
        student_id = input("Enter your student ID: ")
        if student_id in Student.students_db:
            print(f"Welcome, {Student.students_db[student_id]['name']}!")
            Student.student_portal(student_id)
        else:
            print("Invalid Student ID. Please sign up first.")

    @staticmethod
    def student_portal(student_id):
        while True:
            print("\nStudent Dashboard")
            print("1. View Grades")
            print("2. Search Subject")
            print("3. Log Out")
            choice = input("Choose an option: ")

            if choice == "1":
                Student.view_grades(student_id)
            elif choice == "2":
                Student.search_subject()
            elif choice == "3":
                print("Logged out.")
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_grades(student_id):
        grades = Student.students_db[student_id]["grades"]
        if not grades:
            print("No grades available.")
        else:
            total_units = 0
            total_score = 0
            for subject, data in grades.items():
                print(f"{subject} - Grade: {data['Grade']}, Units: {data['Units']}")
                total_units += data["Units"]
                total_score += data["Grade"] * data["Units"]
            gpa = total_score / total_units
            print(f"Total GPA: {gpa:.2f}")
            if gpa >= 1.75:
                print("Latin Honor: Yes")
            else:
                print("Latin Honor: No")

    @staticmethod
    def search_subject():
        subject = input("Enter subject to search: ")
        if subject in Student.subjects:
            print(f"{subject} found!")
            print(Student.subjects[subject])
        else:
            print(f"{subject} not found.")
