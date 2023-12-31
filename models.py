from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    texts = db.relationship('Text', backref='user', lazy='subquery')

    grammar_errors = db.relationship('Grammar_Error', backref='user', lazy='subquery')

    spelling_errors = db.relationship('Spelling_Error', backref='user', lazy='subquery')

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}>"
    
    @classmethod
    def signup(cls, username, email, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Text(db.Model):
    
    __tablename__ = 'texts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    original_text = db.Column(
        db.Text,
        nullable=False
    )

    edited_text = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Text id: {self.id}, user: {self.user_id}, original_text: {self.original_text}>"
    

class Grammar_Error(db.Model):

    __tablename__ = 'grammar_errors'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    text_id = db.Column(
        db.Integer,
        db.ForeignKey('texts.id'),
        nullable=False
    )

    error_type = db.Column(
        db.Text,
        nullable=False
    )

    start = db.Column(
        db.Integer,
        nullable=False
    )

    end = db.Column(
        db.Integer,
        nullable=False
    )

    replacement = db.Column(
        db.Text,
        nullable=False
    )

    sentence = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Grammar_Error id: {self.id}, user: {self.user_id}, error_type: {self.error_type}, replacement: {self.replacement}>"


class Spelling_Error(db.Model):
   
    __tablename__ = 'spelling_errors'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    text_id = db.Column(
        db.Integer,
        db.ForeignKey('texts.id'),
        nullable=False
    )

    start = db.Column(
        db.Integer,
        nullable=False
    )

    end = db.Column(
        db.Integer,
        nullable=False
    )

    replacement = db.Column(
        db.Text,
        nullable=False
    )

    sentence = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Spelling_Error id: {self.id}, user: {self.user_id}, replacement: {self.replacement}>"
    

def connect_db(app):
    db.app = app
    db.init_app(app)














