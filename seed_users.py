from models import User, db
from app import app


# Recreate tables
db.drop_all()
db.create_all()

# Ensure it's empty
User.query.delete()

# Add starting users
jackie_chan = User(first_name='Jackie', last_name='Chan',
            img_url='static/jackie_chan.jpg')
dave_grohl = User(first_name='Dave', last_name='Grohl',
            img_url='static/dave_grohl.png')
warren = User(first_name='Elizabeth', last_name='Warren',
            img_url='static/elizabeth_warren.jpg')
doe = User(first_name='Jane', last_name='Doe')

# Add new users to session
db.session.add(jackie_chan)
db.session.add(dave_grohl)
db.session.add(warren)
db.session.add(doe)

# Commit to DB
db.session.commit()