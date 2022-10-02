"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import functions as func
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(20),
                           nullable=False)
    
    last_name = db.Column(db.String(20),
                          nullable=False)
    
    img_url = db.Column(db.String,
                          nullable=True,
                          default="static/default_user.png")

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()
        
    def __repr__(self):
        return f"<User id={self.user_id} First name={self.first_name} last name={self.last_name} image url={self.img_url}>"
    
    @staticmethod
    def add_user(first_name: str, last_name: str, *img_url: str):
        """Method for adding users to database

        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            img_url (str): URL of image
        """
        if img_url:
            new_user = User(first_name = first_name, last_name = last_name, img_url = img_url[0])
            print(img_url)
        else:
            new_user = User(first_name = first_name, last_name = last_name)
        db.session.add(new_user)
        db.session.commit()
        
    def edit_user(updated_info):
        user = User.query.get_or_404(updated_info['id'])
        
        if updated_info.get('first_name'):
            user.first_name = updated_info['first_name']
        if updated_info.get('last_name'):
            user.last_name = updated_info['last_name']
        if updated_info.get('img_url'):
            user.img_url = updated_info['img_url']
        
        db.session.add(user)
        db.session.commit()
        
    def delete_user(id):
        User.query.filter_by(user_id=id).delete()
        db.session.commit()
    
    def get_all_users():
        return User.query.order_by(User.last_name)
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'
    
    post_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', 
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'))
    
    user = db.relationship('User', backref='posts', single_parent=True)
    
    def __repr__(self):
        return f"<Post id={self.id} title={self.title} author={self.User.full_name}>"
    
    def add_post(title, content, user_id):
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        
    def delete_post(post_id):
        # deleted_post = Post.get_post(post_id)
        Post.query.filter_by(post_id=post_id).delete()
        db.session.commit()
        
    def edit_post(new_details):
        post = Post.query.get_or_404(new_details['id'])
        
        if new_details.get('title'):
            post.title = new_details['title']
        if new_details.get('content'):
            post.content = new_details['content']
            
        db.session.add(post)
        db.session.commit()
            
        
    def get_post(post_id):
        return Post.query.get(post_id)
    
    @property
    def timestamp(self):
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September',
                  'October', 'November', 'December']
        date = self.created_at
        
        return f'{months[date.month]} {date.day}, {date.year} {date.hour}:{date.minute}:{date.second}'
