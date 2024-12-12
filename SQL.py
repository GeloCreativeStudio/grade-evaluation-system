from pymongo import MongoClient
import re

def connect_to_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client["grades_management"]
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

db = connect_to_db()

def populate_students_from_doc():
    if db is not None:
        print("Database connection is unavailable.")
        return

    students_collection = db["students"]

    raw_data = """
    Brucal, Christine Joy M., 210179, BACHELOR OF SCIENCE IN COMPUTER SCIENCE, 09663454607, cjbrucal@gmail.com
    Salazar, Myca M., 210240, BACHELOR OF SCIENCE IN COMPUTER SCIENCE, 09163854234, mycasalazar@gmail.com
    Mangaring, Dhaian Kris, 201687, BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION Major: Marketing Management, 09171234567, dhaian.kris.mangaring@gmail.com
    Pestaño, Ellen, 210138, BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION Major: Marketing Management, 09229876543, ellen.pestano@gmail.com
    Fabregas, Marvin F., 220235, BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION Major: Financial Management, 09357468529, marvin.f.fabregas@gmail.com

    """

    lines = raw_data.strip().split("\n")

    for line in lines:

        match = re.match(
            r"(?P<name>.+?),\s(?P<student_number>\d+),\s(?P<program>.+?),\s(?P<contact>\d+),\s(?P<email>.+)",
            line.strip()
        )
        if match:
            student_data = match.groupdict()

            if not students_collection.find_one({"student_number": student_data["student_number"]}):
                students_collection.insert_one(student_data)
                print(f"Inserted: {student_data}")
            else:
                print(f"Duplicate found: {student_data['student_number']}")
        else:
            print(f"Failed to parse line: {line}")

populate_students_from_doc()