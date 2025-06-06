# app.py

import os

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Users(Resource):

    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

api.add_resource(Users, '/users')

class UsersByID(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return make_response(jsonify(user.to_dict()), 200)
    
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'error': 'User not found'}, 404
        
        data = request.get_json()
        amount = data.get('amount')

        if amount is None or not isinstance(amount, (int, float)):
            return {'error': "Invalid or missing 'amount'"}, 400
        
        user.amount += amount
        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)

api.add_resource(UsersByID, '/users/<int:id>')

class Transactions(Resource):

    def get(self):
        transactions = [transaction.to_dict() for transaction in Transaction.query.all()]
        return make_response(jsonify(transactions), 200)

    def post(self):
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        amount = data.get('amount')

        if not sender_id or not receiver_id or not amount:
            return {'error': 'sender_id, receiver_id, and amount are required'}, 400
        
        if sender_id == receiver_id:
            return {'error': 'Sender and receiver cannot be the same user'}, 400
        
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)

        if not sender or not receiver:
            return {'error': 'Sender or receiver not found'}, 400
        
        if sender.amount < amount:
            return {'error': 'Insufficent funds'}, 400
        
        sender.amount -= amount
        receiver.amount += amount

        transaction = Transaction(
            sender_id = sender_id,
            receiver_id = receiver_id,
            amount=amount
        )

        db.session.add(transaction)
        db.session.commit()

        return make_response(jsonify(transaction.to_dict()), 201)
    
api.add_resource(Transactions, '/transactions')