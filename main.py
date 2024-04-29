import datetime
from flask import Flask, render_template, redirect
from flask_login import login_user, login_required, logout_user, LoginManager
from data import db_session
from data.users import User, Jobs
from forms.user import RegisterForm, LoginForm
from forms.creation_forms import CreateJobForm
from data.jobs_api import blueprint as jobs_bp
from data.users_api import blueprint as users_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afdafggzv.,xkmc'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for job in jobs:
        team_leader = db_sess.query(User).get(job.team_leader)
        job.team_leader = f'{team_leader.name} {team_leader.surname}'
    return render_template('jobs.html', jobs=jobs)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = CreateJobForm()

    if form.validate_on_submit():
        new_job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )

        db_sess = db_session.create_session()
        db_sess.add(new_job)
        db_sess.commit()

        return redirect('/')

    return render_template('add_job.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form, active_tab='login')

    return render_template('login.html', form=form, active_tab='login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")

    import os

    if not os.path.exists(os.path.realpath('db/blogs.db')):

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

    app.register_blueprint(jobs_bp)
    app.register_blueprint(users_bp)
    app.run()
