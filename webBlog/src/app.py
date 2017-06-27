'''
Notes: We are going to create 3 models for our blog app: Posts, Blogs, and Users
We are going to create a Database class so each of our models has access to the same endpoint
The models will live in a python module called models
The database class will live in a python module called common
'''

from flask import Flask, render_template, request, session
from models.user import User
from src.common.database import Database

app = Flask(__name__)
app.secret_key = "password"


@app.route('/')
def home_template():
    return render_template('index.html')


@app.route('/login') # localhost:5000/
def login_template():
    return render_template('login.html')


@app.route('/register') # localhost:5000/
def register_template():
    return render_template('register.html')


@app.before_first_request
def initalize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    # you can define a custom port
    app.run(port=4995)
