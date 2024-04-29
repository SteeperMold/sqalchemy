from flask import Flask, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
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
            is_finished=form.is_finished.data,
        )

        db_sess = db_session.create_session()
        db_sess.add(new_job)
        db_sess.commit()

        return redirect('/')

    return render_template('add_job.html', title='Создание работы', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if not job:
        return render_template('add_job.html', title='Изменение работы', message='Работа не найдена')

    if current_user.id not in (job.team_leader, 1):
        return render_template('add_job.html', title='Изменение работы', message='Недостаточно прав для редактирования')

    data = {
        'team_leader': job.team_leader,
        'job': job.job,
        'work_size': job.work_size,
        'collaborators': job.collaborators,
        'start_date': job.start_date,
        'end_date': job.end_date,
        'is_finished': job.is_finished,
    }

    form = CreateJobForm(data=data)

    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')

    return render_template('add_job.html', title='Изменение работы', form=form)


@app.route('/delete_job/<int:id>')
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if not job:
        return redirect('/')

    if current_user.id not in (job.team_leader, 1):
        return redirect('/')

    db_sess.delete(job)
    db_sess.commit()

    return redirect('/')


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
    app.register_blueprint(jobs_bp)
    app.register_blueprint(users_bp)
    app.run()
