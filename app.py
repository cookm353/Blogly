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
    # users = User.query.all()
    users = User.get_all_users()
    
    return render_template('index.html', users=users)
    
@app.route('/users/new')
def add_user():
    """
    Form for adding new users
    """
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Process adding new user"""
    first_name =  request.form['firstName']
    last_name = request.form['lastName']
    img_url = request.form['imgURL']
    
    if img_url:
        User.add_user(first_name, last_name, img_url)
    else:
        User.add_user(first_name, last_name)
    
    print(first_name, last_name, img_url)
    return redirect('/users')
    
@app.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)
    
@app.route('/users/<user_id>/edit')
def show_update_user_form(user_id):
    
    return render_template('edit_user.html', id=user_id)
    
@app.route('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    print(user)
    
    # if request.form.get('firstName'):
        # user.firstName = 
    
    for k, v in request.form.items():
        if v:
            # print(k, v)
            # print(user.k)
            print(user[k])
        
    # db.session.add(user)
    # db.session.commit()
    
    for k,v in request.form.items():
        print(k, v)
    # firstName =  request.form['firstName']
    # lastName = request.form['lastName']
    # imgUrl = request.form['imgURL']
    
    # if imgUrl != '':
    #     User.edit_user(user_id, firstName, lastName, imgUrl)
    # else:
    #     User.edit_user(user_id, **details)
    return redirect('/users')
    
@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id: int):
    """Deletes user from DB

    Args:
        user_id (int): id of user to be deleted
    """
    User.delete_user(user_id)
    return redirect('/users')
    
def main():
    ...
    
if __name__ == "__main__":
    main()