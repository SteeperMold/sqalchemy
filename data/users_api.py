import flask
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=["GET"])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users': [user.to_dict() for user in users]
        }
    )


@blueprint.route('/api/users/<user_id>', methods=["GET"])
def get_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()

    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    return flask.jsonify(
        {
            'user': user.to_dict()
        }
    )


@blueprint.route('/api/users', methods=["POST"])
def post_user():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    new_user = User(
        surname=flask.request.json['surname'],
        name=flask.request.json['name'],
        age=flask.request.json['age'],
        position=flask.request.json['position'],
        speciality=flask.request.json['speciality'],
        address=flask.request.json['address'],
        email=flask.request.json['email'],
        hashed_password=flask.request.json['hashed_password']
    )
    db_sess.add(new_user)
    db_sess.commit()
    return flask.jsonify({'id': new_user.id})


@blueprint.route('/api/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    user.surname = flask.request.json['surname']
    user.name = flask.request.json['name']
    user.age = flask.request.json['age']
    user.position = flask.request.json['position']
    user.speciality = flask.request.json['speciality']
    user.address = flask.request.json['address']
    user.email = flask.request.json['email']
    user.hashed_password = flask.request.json['hashed_password']

    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
