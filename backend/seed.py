# seed.py

from app import app
from models import db, User

with app.app_context():

    print('Deleting existing birds...')
    User.query.delete()

    print('Creating user objects...')
    users = []
    user1 = User(username='lightyagami')
    user2 = User(username='roronoazoro')
    users.append(user1)
    users.append(user2)

    print('Adding bird objects to transaction...')
    db.session.add_all(users)

    print('Committing transaction...')
    db.session.commit()

    print('Complete.')
