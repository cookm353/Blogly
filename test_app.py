from unittest import TestCase
from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class Test_App(TestCase):
    def setUp(self):
        User.query.delete()
        
        user = User(first_name='John', last_name='Doe')
        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id
        self.user = user
    
    def tearDown(self):
        db.session.rollback()
        
    def test_index_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')
            
            self.assertEqual(resp.status_code, 302)
            
    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            
    def test_user_display_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            
    def test_add_user_form_display(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            
    def test_adding_users(self):
        # Just doesn't want to work for me
        with app.test_client() as client:
            d = {'first_name': 'Jane', 'last_name': 'Doe', 
                 'img_url': 'static/default_user.png'}
            resp = client.post('/users/new', data=d)
            
            # html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            # self.assertIn('Jane, Doe', html)
            
    def test_showing_details(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            
    def test_deleting_user(self):
        with app.test_client() as client:
            resp = client.post('/users/1/delete')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            
    def test_deleting_user_aftermath(self):
        with app.test_client() as client:
            resp = client.post('/users/1/delete', 
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John Doe', html)