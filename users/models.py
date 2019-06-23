import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class ModelMixin:
    """
    Model mixin for updating the model from dictionary
    """
    def update(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except Exception as ex:
                pass


class User(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


class Email(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("emails", uselist=True))

    def __repr__(self):
        return f'<Email {self.email}>'
