from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from users.models import db
from users.models import User, Email


class EmailSchema(ModelSchema):
    """
    Email schema serializer
    """
    class Meta:
        model = Email
        session = db.Session


class UserSchema(ModelSchema):
    """
    User Schema Serializer
    """
    emails = fields.Nested(EmailSchema(exclude=('user',), session=db.session, many=True), many=True)

    class Meta:
        model = User
        session = db.Session


user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True, many=True)
emails_schema = EmailSchema(strict=True, many=True)
