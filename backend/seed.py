# seed.py

from app import app
from models import db, User

with app.app_context():

    print('Deleting existing birds...')
    User.query.delete()

    print('Creating bird objects...')
    users = []
    user1 = User(username='lightyagami')
    users.append(user1)

    print('Adding bird objects to transaction...')
    db.session.add_all(users)

    print('Committing transaction...')
    db.session.commit()

    print('Complete.')
