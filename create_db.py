import os
import datetime as dt

from app import app
from models import db, Student, Major

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)

    db.drop_all()
    db.create_all()

    majors = [
        "Accounting",
        "Finance",
        "Information Systems",
        "International Business",
        "Management",
        "Operations Management & Business Analytics",
        "Supply Chain Management"
    ]

    for major_name in majors:
        db.session.add(Major(major=major_name))

    db.session.commit()

    students = [
        {
            "first_name": "Robert",
            "last_name": "Smith",
            "email": "robert.smith@example.com",
            "major_id": 3,
            "birth_date": dt.datetime(2007, 6, 1),
            "is_honors": True
        },
        {
            "first_name": "Leo",
            "last_name": "Van Munching",
            "email": "leo.vanmunching@example.com",
            "major_id": 6,
            "birth_date": dt.datetime(2008, 3, 24),
            "is_honors": False
        }
    ]

    for student_data in students:
        student = Student(**student_data)
        db.session.add(student)
        print(f"{student.first_name} {student.last_name} inserted")

    db.session.commit()
    print("Database recreated successfully with the email field.")