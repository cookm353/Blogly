from models import User, Post, Tag, PostTag, db
from app import app


# Recreate tables
db.drop_all()
db.create_all()

# Ensure tables are empty
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

"""
Users
"""
# Add starting users
jackie = User(first_name='Jackie', last_name='Chan',
            img_url='static/jackie_chan.jpg')
grohl = User(first_name='Dave', last_name='Grohl',
            img_url='static/dave_grohl.png')
warren = User(first_name='Elizabeth', last_name='Warren',
            img_url='static/elizabeth_warren.jpg')
doe = User(first_name='Jane', last_name='Doe')

"""
Posts
"""
# Add starting users
doe_post = Post(title='First Post!', 
                 content='Hello world!', user_id=4)
grohl_post = Post(title='Newest Album',
                  content='Check out our latest album, Medicine at Midnight!',
                  user_id=2)
warren_post = Post(title='Have a Problem?',
                   content='I have a plan for that!',
                   user_id=3)

# Add posts to DB
db.session.add_all([jackie, grohl, warren, doe, doe_post, 
                    grohl_post, warren_post])
db.session.commit()

"""
Tags
"""
# Add a few tags
funny_tag = Tag(tag_name='Funny', posttag=[PostTag(post_id=3)])
hi_tag = Tag(tag_name='Hi', posttag=[PostTag(post_id=1)])
wow_tag = Tag(tag_name='Wow!', posttag=[PostTag(post_id=2)])
news_tag = Tag(tag_name='News', posttag=[PostTag(post_id=2), PostTag(post_id=3)])

# Add tags and users to DB
db.session.add_all([funny_tag, hi_tag, wow_tag, news_tag])
db.session.commit()


# Posts -> Post Tags -> Tags