import flask
from . import db_session
from .users import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=["GET"])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<job_id>', methods=["GET"])
def get_job(job_id):
    try:
        job_id = int(job_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    return flask.jsonify(
        {
            'job': job.to_dict()
        }
    )


@blueprint.route('/api/jobs', methods=["POST"])
def post_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return flask.make_response(flask.sonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    new_job = Jobs(
        team_leader=flask.request.json['team_leader'],
        job=flask.request.json['job'],
        work_size=flask.request.json['work_size'],
        collaborators=flask.request.json['collaborators'],
        start_date=flask.request.json['start_date'],
        end_date=flask.request.json['end_date'],
        is_finished=flask.request.json['is_finished']
    )
    db_sess.add(new_job)
    db_sess.commit()
    return flask.jsonify({'id': new_job.id})


@blueprint.route('/api/jobs/<job_id>', methods=["DELETE"])
def delete_job(job_id):
    try:
        job_id = int(job_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<job_id>', methods=["PUT"])
def update_job(job_id):
    try:
        job_id = int(job_id)
    except ValueError:
        return flask.make_response(flask.jsonify({'error': 'Wrong request'}), 400)

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    job.team_leader = flask.request.json['team_leader']
    job.job = flask.request.json['job']
    job.work_size = flask.request.json['work_size']
    job.collaborators = flask.request.json['collaborators']
    job.start_date = flask.request.json['start_date']
    job.end_date = flask.request.json['end_date']
    job.is_finished = flask.request.json['is_finished']

    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
