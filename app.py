
from flask import Flask, render_template, request

app = Flask(__name__)


# Home Page
@app.route('/')
def home():
    return render_template('hello.html')


# Hello Page
@app.route('/hello')
def hello():
    return render_template('hello.html')


# Favorite Course Page
@app.route('/favorite-course')
def favorite_course():
    subject = request.args.get('subject', '')
    course_number = request.args.get('course_number', '')

    return render_template(
        'favorite-course.html',
        subject=subject,
        course_number=course_number
    )


# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')

        return render_template(
            'contact.html',
            submitted=True,
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message
        )

    return render_template(
        'contact.html',
        submitted=False
    )


# Run Flask Application
if __name__ == '__main__':
    app.run(debug=True, port=5001)
