import datetime
from flask import Flask, render_template
from data import db_session
from data.users import User, Jobs

app = Flask(__name__)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for job in jobs:
        team_leader = db_sess.query(User).get(job.team_leader)
        job.team_leader = f'{team_leader.name} {team_leader.surname}'
    return render_template('jobs.html', jobs=jobs)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")

    users = [
        ["Scott", "Riddley", 21, 'captain', 'research engineer', 'module_1', "scott_chief@mars.org"],
        ["Scott2", "Riddley", 22, 'not captain', 'research engineer', 'module_2', "scott2_chief@mars.org"],
        ["Scott3", "Riddley", 23, 'not captain', 'research engineer', 'module_3', "scott3_chief@mars.org"],
        ["Scott4", "Riddley", 24, 'not captain', 'research engineer', 'module_4', "scott4_chief@mars.org"],
    ]

    db_sess = db_session.create_session()

    for surname, name, age, position, speciality, address, email in users:
        new_user = User()
        new_user.surname = surname
        new_user.name = name
        new_user.age = age
        new_user.position = position
        new_user.speciality = speciality
        new_user.address = address
        new_user.email = email
        db_sess.add(new_user)

    for i in range(5):
        new_job = Jobs()
        new_job.team_leader = 1
        new_job.job = 'deployment of residential modules 1 and 2'
        new_job.work_size = 15
        new_job.collaborators = '2, 3'
        new_job.start_date = datetime.datetime.now()
        new_job.is_finished = False
        db_sess.add(new_job)

    db_sess.commit()

    app.run()
