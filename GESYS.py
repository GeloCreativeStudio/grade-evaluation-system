
from student import Student
from registrar import Registrar

def main():
    while True:
        print("\nGrade Evaluation System")
        print("1. Student Login")
        print("2. Registrar Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            Student.menu()
        elif choice == "2":
            Registrar.menu()
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
