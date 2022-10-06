"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    new_user_info = request.form
    User.add_user(new_user_info)

    return redirect('/users')
    
@app.route('/users/<user_id>')
def get_user_details(user_id):
    """Displays details of selected user"""
    user = User.get_user_by_id(user_id)
    
    return render_template('user_details.html', user=user)
    
@app.route('/users/<user_id>/edit')
def show_update_user_form(user_id):
    """Display form for updating user info"""
    
    return render_template('edit_user.html', id=user_id)
    
@app.route('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Edit user information"""
    User.edit_user(user_id, request.form)

    return redirect('/users')
    
@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id: int):
    """Deletes user from DB"""
    
    User.delete_user(user_id)
    return redirect('/users')

# Routes related to posts

@app.route('/users/<user_id>/posts/new')
def show_new_post_form(user_id: int):
    """Display form for creating new post"""
    user = User.get_user_by_id(user_id)
    tags = Tag.get_tags()
    
    return render_template('add_post.html', user=user, tags=tags)
    
@app.route('/users/<user_id>/posts/new', methods=['POST'])
def create_post(user_id: int):
    """Actually create the post"""
    Post.add_post(user_id, request.form)
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def show_post(post_id: int):
    """Display specified post"""
    post = Post.get_post(post_id)
    tags = Post.get_tags_by_post(post_id)
    
    return render_template('view_post.html', post=post, tags=tags)

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

    Post.delete_post(post_id)
    
    return redirect(f'/users/{user_id}')

# Routes related to tags

@app.route('/tags')
def show_tags():
    tags = Tag.get_tags()
    
    return render_template('show_tags.html', tags=tags)
    
@app.route('/tags/<tag_id>')
def show_tag_details(tag_id):
    tag, posts = Tag.get_posts_by_tag(tag_id)
    
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def show_make_tag_form():
    return render_template('add_tag.html')
    
@app.route('/tags/new', methods=['POST'])
def make_tag():
    tag_name = request.form['tag_name']
    Tag.make_tag(tag_name)
    
    return redirect('/tags')
    
@app.route('/tags/<tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.get_tag(tag_id)
    
    return render_template('edit_tag.html', tag=tag)
    
@app.route('/tags/<tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    new_tag_name = request.form['new_tag_name']
    Tag.edit_tag(tag_id, new_tag_name)
    
    return redirect(f'/tags/{tag_id}')
    
@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    Tag.delete_tag(tag_id)
    return redirect('/tags')