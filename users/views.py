from flask import jsonify, make_response
from flask import Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError

from users import db
from users.models import User, Email
from users.serializers import user_schema, users_schema, UserSchema, emails_schema, EmailSchema

bp = Blueprint('users', __name__, url_prefix='/user')


@bp.route('/', methods=('GET',))
def users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@bp.route('/<id>', methods=('GET',))
def user_detail(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)


@bp.route('/', methods=('POST',))
def create_user():
    data = request.get_json(force=True)
    us = UserSchema(session=db.session, transient=True)
    user_obj = us.load(data=data).data

    existing_user = User.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return make_response(jsonify({'message': 'Username already exists'}), 409)
    else:
        db.session.add(user_obj)
        db.session.commit()

    return jsonify(user_schema.dump(user_obj).data)


@bp.route('/<id>', methods=('PUT',))
def update_user(id):
    data = request.get_json(force=True)
    es = EmailSchema(session=db.session, many=True)

    existing_user = User.query.get(id)

    emails_obj = None
    emails_data = data.pop('emails', None)
    if emails_data is not None:
        emails_obj = _extract_emails(es.load(emails_data, many=True).data)

    if existing_user:
        existing_user.update(**data)
        if emails_obj is not None:
            existing_user.emails = emails_obj
        try:
            db.session.commit()
        except IntegrityError:
            return make_response(jsonify({'message': 'Username already exists'}), 400)

    else:
        return make_response(jsonify({'message': 'User not found'}), 404)

    return jsonify(user_schema.dump(existing_user).data)


@bp.route('/<id>', methods=('DELETE',))
def delete_user(id):
    existing_user = User.query.get(id)

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
    else:
        return make_response(jsonify({'message': 'User not found'}), 404)

    return make_response(jsonify({}), 204)


@bp.route('/search', methods=('GET',))
def search_user():
    search_data = []

    for key, field in (('username', User.username), ('email', Email.email)):
        if request.args.get(key):
            search_data.append(field == request.args.get(key))

    if search_data == {}:
        return make_response(jsonify({'message': 'No search parameters provided'}), 400)

    existing_user = User.query.join(User.emails).filter(*search_data).first()

    if not existing_user:
        return make_response(jsonify({'message': 'User not found'}), 404)

    return jsonify(user_schema.dump(existing_user).data)


def _extract_emails(emails_data):
    emails = {e.email: e for e in emails_data}
    existing_emails = Email.query.filter(Email.email.in_(emails.keys())).all()
    emails.update({e.email: e for e in existing_emails})

    return list(emails.values())
