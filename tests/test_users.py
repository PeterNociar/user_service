from users.models import User, Email


def test_index(test_client):
    response = test_client.get('/user/')
    assert [] == response.json


def test_create_user(test_client):
    data = {
        'username': 'TestUser1',
        'first_name': 'Peter',
        'surname': 'Parker',
        'emails': [{'email': 'email_1'}]
    }
    response = test_client.post('/user/', json=data)

    assert response.status_code == 200

    assert 'id' in response.json
    response.json.pop('id')
    assert 'emails' in response.json
    assert len(response.json['emails']) == 1
    assert response.json['emails'][0].pop('id')
    assert response.json == data


def test_update_user(user_factory, db, test_client):
    first_name = 'Miles'
    surname = 'Morales'
    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)

    db.session.add(user)
    db.session.commit()

    data = {'first_name': first_name, 'surname': surname}
    response = test_client.put(f'/user/{user.id}', json=data)

    assert response.status_code == 200

    assert response.json['first_name'] == first_name
    assert response.json['surname'] == surname

    user = User.query.all()[0]

    assert user.first_name == first_name
    assert user.surname == surname


def test_delete_user(user_factory, db, test_client):
    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)
    db.session.add(user)
    db.session.commit()

    response = test_client.delete(f'/user/{user.id}')

    assert response.status_code == 204
    assert len(User.query.all()) == 0


def test_search_user_by_username(user_factory, db, test_client):
    expected_data = {
        'id': 1,
        'username': 'Spiderman',
        'first_name': 'Peter',
        'surname': 'Parker',
        'emails': [
            {
                'id': 1,
                'email': 'email_1',
            }
        ]
    }

    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)
    db.session.add(user)
    db.session.commit()

    response = test_client.get(f'/user/search', query_string={'username': 'Spiderman'})

    assert response.status_code == 200

    assert response.json == expected_data


def test_search_user_by_email(user_factory, db, test_client):
    expected_data = {
        'id': 1,
        'username': 'Spiderman',
        'first_name': 'Peter',
        'surname': 'Parker',
        'emails': [
            {
                'id': 1,
                'email': 'email_1',
            }
        ]
    }

    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)
    db.session.add(user)
    db.session.commit()

    response = test_client.get(f'/user/search', query_string={'email': 'email_1'})

    assert response.status_code == 200

    assert response.json == expected_data


def test_update_user_add_emails(user_factory, db, test_client):
    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)

    db.session.add(user)
    db.session.commit()

    data = {'emails': [{'email': 'email_2'}, {'email': 'email_1'}]}
    response = test_client.put(f'/user/{user.id}', json=data)

    assert response.status_code == 200

    user = User.query.all()[0]

    assert len(user.emails) == 2


def test_update_user_remove_email(user_factory, db, test_client):
    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)

    db.session.add(user)
    db.session.commit()

    data = {'emails': []}
    response = test_client.put(f'/user/{user.id}', json=data)

    assert response.status_code == 200

    user = User.query.all()[0]

    assert len(user.emails) == 0


def test_update_user_update_username(user_factory, db, test_client):
    user = user_factory(username='Spiderman', first_name='Peter', surname='Parker')
    _email = Email(email='email_1', user=user)

    db.session.add(user)
    db.session.commit()

    data = {'username': 'Superhero'}
    response = test_client.put(f'/user/{user.id}', json=data)

    assert response.status_code == 200

    user = User.query.all()[0]
    assert user.username == 'Superhero'
