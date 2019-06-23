import factory
from users import celery_, db
from datetime import datetime, timedelta
from users.models import User, Email

TASK_NEW_USERS_QUANTITY = 2


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Factory class for User model
    """
    username = factory.Faker('name')
    first_name = factory.Faker('name')
    surname = factory.Faker('last_name')

    class Meta:
        model = User
        sqlalchemy_session = db.session


class EmailFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Factory class for Email model
    """
    email = factory.Faker('email')

    class Meta:
        model = Email
        sqlalchemy_session = db.session


@celery_.task
def refresh_users():
    """
    Task for cleaning all of the Users that are more than 1 min old and create 2 new users with 2
    emails each
    :return:
    """
    one_min_ago = datetime.utcnow() - timedelta(minutes=1)
    # Delete old users
    User.query.filter(User.created_at < one_min_ago).delete()

    # Create x new users
    for i in range(TASK_NEW_USERS_QUANTITY):
        emails = [EmailFactory(), EmailFactory()]
        user = UserFactory(emails=emails)
        db.session.add(user)

    db.session.commit()
    print('End task')
