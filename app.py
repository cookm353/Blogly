"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post

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



@app.route('/users/<user_id>/posts/new')
def show_new_post_form(user_id: int):
    """Display form for creating new post"""
    user = User.get_user_by_id(user_id)
    print(user)
    print(user.full_name)
    
    return render_template('add_post.html', user=user)
    
@app.route('/users/<user_id>/posts/new', methods=['POST'])
def create_post(user_id: int):
    """Actually create the post"""
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    
    Post.add_post(post_title, post_content, user_id)
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def show_post(post_id: int):
    """Display specified post"""
    
    post = Post.get_post(post_id)
    
    return render_template('view_post.html', post=post)

@app.route('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    """Show form for editing a post"""
    post = Post.get_post(post_id)
    
    return render_template('edit_post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Actually edit the post"""    
    new_post_info = {'id': post_id,
                     'title': request.form['post_title'],
                     'content': request.form['post_content']}
    
    Post.edit_post(new_post_info)
        
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post"""
    user_id = Post.query.get(post_id).user_id

    # Delete the post
    Post.delete_post(post_id)
    
    return redirect(f'/users/{user_id}')