from flask import Flask, render_template, url_for, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import openai
from chatbot import CustomChatGPT
import chatbot

# Set up Google Cloud API key for OpenAI
openai.api_key = "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"
message = []

app = Flask(__name__)

# Configure SQLAlchemy and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Route to gather data from the interview form and pass it to GPT
@app.route('/dashboard', methods=['POST'])
@login_required
def chat():
    exec(open('chatbot.py').read())
    chatbot.job = request.form["areaOfApplication"]
    chatbot.company = request.form["companyName"]
    chatbot.additionalinfo = request.form["additionalInfo"]
    chatbot.count = 0
    chatbot.messages = []
    return render_template('chat.html', is_authenticated=is_user_authenticated(), username=get_username())

# Route to get data from GPT
@app.route('/api/chat', methods=['POST'])
def chatt():
    user_input = request.json['input']
    response = CustomChatGPT(user_input)
    return jsonify({'response': response})

# Functions for authentication, username retrieval, and user ID loading
def is_user_authenticated():
    return current_user.is_authenticated

def get_username():
    if current_user.is_authenticated:
        return current_user.username
    else:
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User class for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# Form for user registration
class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

# Form for user login
class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

# Various route handlers
@app.route('/')
def home():
    return render_template('home.html', is_authenticated=is_user_authenticated(), username=get_username())

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', is_authenticated=is_user_authenticated(), username=get_username())

@app.route('/contact')
def contact():
    return render_template('contact.html', is_authenticated=is_user_authenticated(), username=get_username())

@app.route('/godashboard')
@login_required
def godashboard():
    return render_template('dashboard.html', is_authenticated=is_user_authenticated(), username=get_username())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', is_authenticated=is_user_authenticated(), username=get_username(), form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', is_authenticated=is_user_authenticated(), username=get_username())

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form, is_authenticated=is_user_authenticated(), username=get_username())

if __name__ == "__main__":
    app.run(debug=True)
