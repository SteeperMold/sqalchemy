from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired


class CreateJobForm(FlaskForm):
    team_leader = IntegerField('Id лидера команды', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Сложность работы', validators=[DataRequired()])
    collaborators = StringField('Участники работы', validators=[DataRequired()])
    start_date = DateTimeLocalField('Дата начала работы', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('Дата окончания работы', format='%Y-%m-%dT%H:%M')
    is_finished = BooleanField('Закончена ли работа?')
    submit = SubmitField('Сохранить')
