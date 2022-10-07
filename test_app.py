from unittest import TestCase
from app import app
from models import User, Post, Tag, PostTag, db

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
        
        Post.query.delete()
        post = Post(title='Foo', content='Bar', user_id=1)
        db.session.add(post)
        db.session.commit()
        
        Tag.query.delete()
        
        tag = Tag(tag_name='Wow!', posttag=[PostTag(post_id=1)])
        db.session.add(tag)
        db.session.commit()
        
        self.user_id = user.user_id
        self.user = user      
        self.post_id = post.post_id
        self.post = post
        
    def tearDown(self):
        db.session.rollback()
        
    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
            self.assertIn('Wow', html)
        
    """User tests"""

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
        with app.test_client() as client:
            d = {'first_name': 'Jane', 'last_name': 'Doe', 
                 'img_url': 'static/default_user.png'}
            resp = client.post('/users/new', data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Doe', html)
            
    def test_showing_user_details(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            
    def test_update_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/1/edit')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Doe', html)
            
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
            
    """Post Tests"""        
    
    def test_showing_posts(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Foo', html)
            
    def test_showing_new_post_form(self):
        with app.test_client() as client:
            resp = client.get('/users/1/posts/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Wow', html)
        
    def test_creating_post(self):
        with app.test_client() as client:
            data = {'post_title': 'Hello', 'post_content': 'World', 'tag1': '1'}
            resp = client.post('/users/1/posts/new', data=data,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello', html)
        
    def test_showing_post(self):
        with app.test_client() as client:
            resp = client.get('/posts/1')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bar', html)
            self.assertIn('Wow', html)
        
    def test_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get('/posts/1/edit')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', html)
            self.assertIn('Wow', html)
            
    def test_editing_post(self):
        with app.test_client() as client:
            data = {'post_title': 'Hello', 'post_content': 'World'}
            resp = client.post('/posts/1/edit', data=data,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('World', html)
            self.assertIn('Wow', html)
            self.assertNotIn('Foo', html)
        
    def test_deleting_post(self):
        with app.test_client() as client:
            resp = client.post('/posts/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Posts', html)
            self.assertNotIn('Foo', html)
            
    """Tag tests"""
            
    def test_tag_list(self):
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tags', html)
            self.assertIn('Wow!', html)
            
    def test_tag_details(self):
        with app.test_client() as client:
            resp = client.get('/tags/1')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Wow', html)
            self.assertIn('Foo', html)
            
    def test_missing_tag_details(self):
        with app.test_client() as client:
            resp = client.get('/tags/2')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 404)
            
    def test_new_tag_form(self):
        with app.test_client() as client:
            resp = client.get('/tags/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a Tag', html)
            
    def test_make_new_tag(self):
        with app.test_client() as client:
            data = {'tag_name': 'Triple Bam!'}
            
            resp = client.post('/tags/new', follow_redirects=True,
                               data=data)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Triple Bam!', html)
            
    def test_edit_tag_page(self):
        with app.test_client() as client:
            resp = client.get('/tags/1/edit')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit a Tag', html)
            
    def test_editing_tag(self):
        with app.test_client() as client:
            data = {'new_tag_name': 'Triple Bam!'}
            resp = client.post('/tags/1/edit', follow_redirects=True,
                               data=data)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Triple Bam!', html)
            self.assertNotIn('Wow', html)
            
    def test_tag_delete(self):
        with app.test_client() as client:
            resp = client.post('/tags/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Wow', html)
            self.assertIn('Tags', html)