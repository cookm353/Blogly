from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class Test_User(TestCase):
    def setUp(self):
        User.query.delete()
    
    def tearDown(self):
        db.session.rollback()
        
    def test_get_user(self):
        user = User(first_name='Jimmy', last_name='Page')
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.get(1)
        self.assertEqual(retrieved_user.first_name, 'Jimmy')
        
    def test_default_img(self):
        user = User(first_name='Jimmy', last_name='Page')
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.get(1)
        self.assertEqual(retrieved_user.img_url, 'static/default_user.png')
        
    def test_repr(self):
        user = User(first_name='Jimmy', last_name='Page')
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(repr(user), '<User id=1 First name=Jimmy last name=Page image url=static/default_user.png>')
        
    def test_adding_user(self):
        User.add_user('Jimmy', 'Page', 'https://www.zombo.com')
        user = User.query.get(1)
        
        self.assertEqual(user.last_name, 'Page')
        self.assertEqual(user.img_url, 'https://www.zombo.com')
        
    def test_edit_user(self):
        User.add_user('Jimmy', 'Page')
        user = User.query.get(1)
        
        self.assertEqual(user.first_name, 'Jimmy')
        
        new_details = {'id': 1, 'first_name': 'Jimi',
                       'last_name': 'Hendrix'}
        User.edit_user(new_details)
        
        self.assertEqual(user.first_name, 'Jimi')
        self.assertNotEqual(user.last_name, 'Page')
        
    def test_delete_user(self):
        User.add_user('Jimmy', 'Page')
        user = User.query.get(1)
        self.assertEqual(user.first_name, 'Jimmy')
        
        User.delete_user(user.user_id)
        self.assertEqual(User.query.one_or_none(), None)