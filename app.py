
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


# About Me Page
@app.route('/about')
def about():
    return render_template('about.html')


# Styled About Me Page
@app.route('/about-css')
def about_css():
    return render_template('about-css.html')


# Favorite Course Page
@app.route('/favorite-course')
def favorite_course():
    subject = request.args.get('subject', 'BMGT')
    course_number = request.args.get('course_number', '407')

    return render_template(
        'favorite-course.html',
        subject=subject,
        course_number=course_number
    )


# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)

