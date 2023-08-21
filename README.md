InterviewGuru Web Application

InterviewGuru is a web application developed as a CSCI-50 final project with the potential to become a startup. It provides a platform for practicing interview questions and preparing for job interviews.

Folders:

InterviewGuru: The main folder, contains the application files like folders, app.py, chatbot.py, design.md and readme.md.
__pycache__: Python-generated directory, can be ignored.
instance: Contains the database for user authentication.
static: Contains CSS files and images.
templates: Contains HTML files.

Files:

chatbot.py : Chat-GPT configuration
app.py : Mainly flask paths.

Requirements:
To use InterviewGuru, make sure you have the following libraries installed:

openai
flask_bcrypt
wtforms
wtforms.validators
flask_wtf
flask_login
flask_sqlalchemy
flask
Additionally, ensure that your code editor supports the following languages: Jinja, Python, JavaScript, HTML, and CSS.

How to Run:

Run "flask run" in your terminal to start the application. (Make sure you are in the right directory)
Access the homepage from your browser, where you can navigate between pages and explore the application's features.
Sign in or register to access the interview application. Provide data about your interview preparation, and the application will use chatgpt 3.5 turbo model to generate sample questions tailored to your needs. 

Note: My chatbot can only answer 3 questions in a minute because of the api restrictions.

InterviewGuru allows you to practice interview questions, view pricing details, and find contact information for further inquiries.

