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
    return redirect('/users')
    
@app.route('/users')
def show_users():
    """
    Show all users
    """
    users = User.query.all()
    
    return render_template('index.html', users=users)
    
# @app.route('/users/new')
# def add_user():
#     """
#     Form for adding new users
#     """
#     pass

# @app.route('/users/new', methods=['POST'])
# def create_user():
#     """Process user add"""
#     ...
    
@app.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)
    
# @app.route('/users/<user_id>/edit')
# def show_update_user_form(user_id):
#     ...
    
# @app.route('/users/<user_id>/edit', methods=['POST'])
# def update_user(user_id):
#     ...
    
# @app.route('/users/<user_id>/delete', methods=['POST'])
# def delete_user(user_id):
#     ...
    
def main():
    # db.create_all()
    print(db)
    print(db.app)
    
if __name__ == "__main__":
    main()