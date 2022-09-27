"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
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
        return cls.query.filter_by(id=id).all()
        
    def __repr__(self):
        return f"<User id>={self.id} First name={self.first_name} last name={self.last_name} image url={self.img_url}"