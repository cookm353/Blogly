"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bloggo'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

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
    
    
def main():
    # db.create_all()
    print(db)
    print(db.app)
    
if __name__ == "__main__":
    main()