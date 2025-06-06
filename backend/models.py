# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    amount = db.Column(db.Float, default=0)

    sent_transactions = relationship('Transaction', back_populates='sender', foreign_keys='Transaction.sender_id')
    received_transactions = relationship('Transaction', back_populates='receiver', foreign_keys='Transaction.receiver_id')

    def __repr__(self):
        return f'<User {self.username}>'

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    sender = relationship('User', back_populates='sent_transactions', foreign_keys=[sender_id])
    receiver = relationship('User', back_populates='received_transactions', foreign_keys=[receiver_id])

    def __repr__(self):
        return f'<Transaction {self.amount} from {self.sender_id} to {self.receiver_id}>'