"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bloggo'

connect_db(app)
db.create_all()


@app.route('/')
def index():
    """
    Redirect to list of users (for now)
    """
    return render_template('index.html')
    
@app.route('/users')
def show_users():
    """
    Show all users
    """
    pass
    
@app.route('/users/new')
def add_user():
    """
    Form for adding new users
    """
    pass

@app.route('/users/new', methods=['POST'])
def create_user():
    ...