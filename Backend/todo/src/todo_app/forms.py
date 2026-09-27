from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


class TaskForm(FlaskForm):
    title = StringField(
        "Название",
        validators=[DataRequired(message="Введите название задачи."), Length(max=200, message="Не более 200 символов.")],
    )
    description = TextAreaField(
        "Описание",
        validators=[Optional(), Length(max=1000, message="Не более 1000 символов.")],
    )
    priority = RadioField(
        "Приоритет",
        choices=[(1, "Высокий"), (2, "Средний"), (3, "Низкий")],
        coerce=int,
        default=2,
        validators=[DataRequired(message="Выберите приоритет.")],
    )
    due_date = DateField(
        "Дата выполнения",
        format="%Y-%m-%d",
        default=date.today,
        validators=[DataRequired(message="Выберите дату.")],
    )
    submit = SubmitField("Сохранить")

    def validate_title(self, field):
        if not field.data or not field.data.strip():
            raise ValidationError("Название не может состоять только из пробелов.")
