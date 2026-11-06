from datetime import datetime
from pathlib import Path

from werkzeug.security import generate_password_hash

from app import app, db
from models import Major, Student, User


student_username = 'nhusain'
student_email = 'nhusain@terpmail.umd.edu'
student_major = 'Operations Management & Business Analytics'

Path(app.instance_path).mkdir(parents=True, exist_ok=True)

with app.app_context():
    db.drop_all()
    db.create_all()

    majors = [
        'Accounting',
        'Finance',
        'Information Systems',
        'International Business',
        'Management',
        student_major,
        'Supply Chain Management',
    ]

    majors_by_name = {name: Major(major=name) for name in majors}
    db.session.add_all(majors_by_name.values())
    db.session.flush()

    users = [
        User(
            username='student',
            first_name='Imma',
            last_name='Student',
            email='student@umd.edu',
            password=generate_password_hash('studentpw', method='pbkdf2:sha256'),
            role='STUDENT',
        ),
        User(
            username='manager',
            first_name='Joe',
            last_name='King',
            email='manager@umd.edu',
            password=generate_password_hash('managerpw', method='pbkdf2:sha256'),
            role='MANAGER',
        ),
        User(
            username='admin',
            first_name='Crystal',
            last_name='Ball',
            email='admin@umd.edu',
            password=generate_password_hash('adminpw', method='pbkdf2:sha256'),
            role='ADMIN',
        ),
        User(
            username=student_username,
            first_name='Naasera',
            last_name='Husain',
            email=student_email,
            password=generate_password_hash(student_username, method='pbkdf2:sha256'),
            role='STUDENT',
        ),
    ]

    students = [
        Student(
            first_name='Test',
            last_name='Student',
            email='student@umd.edu',
            major_id=majors_by_name['Information Systems'].major_id,
            birth_date=datetime(2007, 8, 1),
            is_honors=True,
        ),
        Student(
            first_name='Naasera',
            last_name='Husain',
            email=student_email,
            major_id=majors_by_name[student_major].major_id,
            birth_date=datetime(2005, 1, 1),
            is_honors=True,
        ),
    ]

    db.session.add_all(users)
    db.session.add_all(students)
    db.session.commit()

    for user in users:
        print(f'{user.username} inserted into user')

    for student in students:
        print(f'{student.first_name} {student.last_name} inserted into student')