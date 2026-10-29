import os
import re
from datetime import datetime as dt

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Major

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(app.instance_path, "university.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "beyond_course_scope"

db.init_app(app)


def valid_email(email):
    return (
        bool(email)
        and len(email) <= 100
        and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) is not None
    )


@app.route("/view")
@app.route("/student/view")
def student_view_all():
    students = (
        Student.query
        .outerjoin(Major, Student.major_id == Major.major_id)
        .add_entity(Major)
        .order_by(Student.last_name, Student.first_name)
        .all()
    )
    return render_template("student_view_all.html", students=students)


@app.route("/student/view/<int:student_id>")
def student_view(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        flash("Student could not be found.", "error")
        return redirect(url_for("student_view_all"))

    majors = Major.query.order_by(Major.major).all()

    return render_template(
        "student_entry.html",
        student=student,
        majors=majors,
        action="read"
    )


@app.route("/student/create", methods=["GET", "POST"])
def student_create():
    majors = Major.query.order_by(Major.major).all()

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()

        if not first_name or not last_name:
            flash("First name and last name are required.", "error")
            return redirect(url_for("student_view_all"))

        if not valid_email(email):
            flash(
                "A valid email address of no more than 100 characters is required.",
                "error"
            )
            return redirect(url_for("student_view_all"))

        try:
            major_id = int(request.form.get("major_id", ""))
            birth_date = dt.strptime(
                request.form.get("birth_date", ""),
                "%Y-%m-%d"
            )
        except ValueError:
            flash("Select a major and enter a valid birth date.", "error")
            return redirect(url_for("student_view_all"))

        if db.session.get(Major, major_id) is None:
            flash("Select a valid major.", "error")
            return redirect(url_for("student_view_all"))

        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            major_id=major_id,
            birth_date=birth_date,
            is_honors="is_honors" in request.form
        )

        db.session.add(student)
        db.session.commit()

        flash(
            f"{first_name} {last_name} was successfully added!",
            "success"
        )
        return redirect(url_for("student_view_all"))

    return render_template(
        "student_entry.html",
        majors=majors,
        action="create"
    )


@app.route("/student/update/<int:student_id>", methods=["GET", "POST"])
def student_edit(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        flash("Student could not be found.", "error")
        return redirect(url_for("student_view_all"))

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()

        if not first_name or not last_name:
            flash("First name and last name are required.", "error")
            return redirect(url_for("student_view_all"))

        if not valid_email(email):
            flash(
                "A valid email address of no more than 100 characters is required.",
                "error"
            )
            return redirect(url_for("student_view_all"))

        try:
            major_id = int(request.form.get("major_id", ""))
            birth_date = dt.strptime(
                request.form.get("birth_date", ""),
                "%Y-%m-%d"
            )
            credits = int(request.form.get("num_credits_completed", ""))
            gpa = float(request.form.get("gpa", ""))
        except ValueError:
            flash("Enter valid values for all required fields.", "error")
            return redirect(url_for("student_view_all"))

        if db.session.get(Major, major_id) is None:
            flash("Select a valid major.", "error")
            return redirect(url_for("student_view_all"))

        if not 0 <= credits <= 200 or not 0 <= gpa <= 4:
            flash("Credits must be 0–200 and GPA must be 0–4.", "error")
            return redirect(url_for("student_view_all"))

        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.major_id = major_id
        student.birth_date = birth_date
        student.num_credits_completed = credits
        student.gpa = gpa
        student.is_honors = "is_honors" in request.form

        db.session.commit()

        flash(
            f"{student.first_name} {student.last_name} was successfully updated!",
            "success"
        )
        return redirect(url_for("student_view_all"))

    majors = Major.query.order_by(Major.major).all()

    return render_template(
        "student_entry.html",
        student=student,
        majors=majors,
        action="update"
    )


@app.route("/student/delete/<int:student_id>")
def student_delete(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        flash("Delete failed! Student could not be found.", "error")
    else:
        student_name = f"{student.first_name} {student.last_name}"

        db.session.delete(student)
        db.session.commit()

        flash(f"{student_name} was successfully deleted!", "success")

    return redirect(url_for("student_view_all"))


@app.route("/")
def home():
    return redirect(url_for("student_view_all"))


if __name__ == "__main__":
    app.run()