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
    """Redirect to list of users (for now...)"""
    
    return redirect('/users')
    
@app.route('/users')
def show_users():
    """Show all users"""
    
    users = User.get_all_users()
    
    return render_template('index.html', users=users)
    
@app.route('/users/new')
def add_user():
    """Form for adding new users"""
    
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Process adding new user"""
    
    first_name =  request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_urlRL']
    
    if img_url:
        User.add_user(first_name, last_name, img_url)
    else:
        User.add_user(first_name, last_name)
    
    print(first_name, last_name, img_url)
    return redirect('/users')
    
@app.route('/users/<user_id>')
def get_user_details(user_id):
    """Displays details of selected user"""
    
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)
    
@app.route('/users/<user_id>/edit')
def show_update_user_form(user_id):
    """Display form for updating user info"""
    
    return render_template('edit_user.html', id=user_id)
    
@app.route('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Edit user information"""
    
    updated_user_info = {'id': user_id,
                       'first_name': request.form['first_name'],
                       'last_name': request.form['last_name'],
                       'img_url': request.form['img_url']}
    
    User.edit_user(updated_user_info)

    return redirect('/users')
    
@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id: int):
    """Deletes user from DB"""
    
    User.delete_user(user_id)
    return redirect('/users')