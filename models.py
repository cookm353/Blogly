"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import functions as func
import sqlalchemy.sql as sql

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
                          nullable=True)
    
    img_url = db.Column(db.String,
                          nullable=True,
                          default="static/default_user.png")

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()
        
    def __repr__(self):
        if self.last_name:
            return f"<User id={self.user_id} First name={self.first_name} last name={self.last_name} image url={self.img_url}>"
        else:
            return f"<User id={self.user_id} First name={self.first_name} image url={self.img_url}>"
    
    @staticmethod
    def add_user(new_user_info):
        """Method for adding users to database"""
        first_name = new_user_info['first_name']
        last_name = new_user_info.get('last_name', None)
        img_url = new_user_info.get('img_url', None)
        
        if img_url and last_name:
            new_user = User(first_name=first_name, last_name=last_name, 
                            img_url=img_url)
        elif last_name:
            new_user = User(first_name=first_name, last_name=last_name)
        elif img_url:
            new_user = User(first_name=first_name, img_url=img_url)
        else:
            new_user = User(first_name=first_name)
        
        db.session.add(new_user)
        db.session.commit()
        
    def edit_user(user_id, updated_user_info):
        user = User.query.get_or_404(user_id)
        
        if updated_user_info.get('first_name'):
            user.first_name = updated_user_info['first_name']
            
        # Shh
        if updated_user_info.get('last_name') == '9999':
            user.last_name = sql.null()
        elif updated_user_info.get('last_name'):
            user.last_name = updated_user_info['last_name']
            
        # Don't tell anyone
        if updated_user_info.get('img_url') == '9999':
            user.img_url = sql.null()
        elif updated_user_info.get('img_url'):
            user.img_url = updated_user_info['img_url']
        
        db.session.add(user)
        db.session.commit()
        
    def delete_user(id):
        User.query.filter_by(user_id=id).delete()
        db.session.commit()
    
    def get_all_users():
        return User.query.order_by(User.last_name)
        
    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name}"


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
    
    user = db.relationship('User', backref='posts')
    tag = db.relationship('Tag', backref='posts', secondary='post_tags')
    posttags = db.relationship('PostTag', backref='posts')
    
    def __repr__(self):
        return f"<Post id={self.post_id} title={self.title} author={self.user.full_name}>"
    
    def add_post(user_id, post_info):
        title = post_info['post_title']
        content = post_info['post_content']
        
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        
        post_id = Post.query.filter(title==title and user_id==user_id).all()[-1].post_id
        
        for k, v in post_info.items():
            if 'tag' in k:
                PostTag.add_posttag(post_id, v)
                
        
    def delete_post(post_id):
        Post.query.filter_by(post_id=post_id).delete()
        db.session.commit()
        
    def edit_post(post_id, new_details):
        post = Post.query.get_or_404(post_id)
        
        for k, v in new_details.items():        
            if k == 'post_title' and v != '':
                post.title = new_details['post_title']
            if k == 'post_content' and v != '':
                post.content = new_details['post_content']
            if 'tag' in k:
                PostTag.add_posttag(post_id, v)
            
        db.session.add(post)
        db.session.commit()
        
    def get_post(post_id):
        return Post.query.get(post_id)
    
    def get_all_posts():
        return Post.query.all()
    
    def get_tags_by_post(post_id):
        tags = Post.query.get_or_404(post_id).tag
        
        return tags
    
    @property
    def timestamp(self):
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September',
                  'October', 'November', 'December']
        date = self.created_at
        
        if date.hour >= 12:
            hour = date.hour - 12
            time = f"{hour}:{date.minute}:{date.second} PM"
        else:
            hour = date.hour
            time = f"{hour}:{date.minute}:{date.second} AM"
        
        return f'{months[date.month]} {date.day}, {date.year} {time}'

    
class Tag(db.Model):
    __tablename__ = 'tags'
    
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.Text, nullable=False)
    
    posttag = db.relationship('PostTag', backref='tags')
    
    def __repr__(self):
        return f"<Tag id={self.tag_id} name={self.tag_name}>"
    
    def get_tags():
        return Tag.query.all()

    def get_tag(tag_id):
        return Tag.query.get_or_404(tag_id)
    
    def get_posts_by_tag(tag_id):
        tag = Tag.get_tag(tag_id)
        posts = tag.posts
        return (tag, posts)
            
    def make_tag(name):
        tag = Tag(tag_name=name)
        db.session.add(tag)
        db.session.commit()

    def edit_tag(tag_id, name):
        tag = Tag.query.get_or_404(tag_id)
        tag.tag_name = name
        
        db.session.add(tag)
        db.session.commit()

    def delete_tag(tag_id):
        Tag.query.filter_by(tag_id = tag_id).delete()
        db.session.commit()
    
    
class PostTag(db.Model):
    __tablename__ = 'post_tags'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id', 
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'),
                       primary_key=True)
    
    def add_posttag(post_id, tag_id):
        # First check if the posttag exists
        row_exists = PostTag.query.filter(post_id == post_id and tag_id == tag_id).count()
        
        if not row_exists:
            posttag = PostTag(post_id=post_id, tag_id=tag_id)
            db.session.add(posttag)
            db.session.commit()
        