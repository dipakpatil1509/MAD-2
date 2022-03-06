from datetime import datetime
import enum

from flask_security import RoleMixin, UserMixin
from application.database import db

Base = db.Model

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(Base, UserMixin):

    class Role(enum.Enum):
        STUDENT = "1"
        TEACHER = "2"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100))
    fs_uniquifier = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(Role), server_default="STUDENT")
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

    decks = db.relationship("Deck", backref="deck", lazy="dynamic")
    reviewResponses = db.relationship("ReviewResponse", backref="reviewresponse", lazy="dynamic")

    def review_response(self):
        try:
            return round(sum(review.score for review in self.reviewResponses)/self.reviewResponses.count(), 2)
        except:
            return 0.00