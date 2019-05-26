from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import StringField, SubmitField, IntegerField, SelectField,\
    TextAreaField
from wtforms.validators import DataRequired, InputRequired


class AddForm(FlaskForm):
    price = IntegerField('Цена', validators=[DataRequired()],
                         render_kw={"class": "form-control form-control-sm",
                                    "placeholder": "100000"})

    description = TextAreaField('Описание', validators=[DataRequired()],
                                render_kw={
                                    "class": "form-control form-control-sm",
                                    "rows": "3",
                                    "placeholder": "Опишите "})
    holders = SelectField('Владельцев по ПТС', validators=[DataRequired()],
                          render_kw={"class": "form-control form-control-sm"},
                          choices=[
                              ('1', '1'), ('2', '2'),
                              ('3', '3'), ('4+', '4+')])

    condition = SelectField('Состояние', validators=[DataRequired()],
                            render_kw={"class": "form-control form-control-sm"},
                            choices=[('не битая', 'Не битая'),
                                     ('битая', 'Битая')])
    steering_wheel = SelectField('Руль', validators=[DataRequired()],
                                 render_kw={
                                    "class": "form-control form-control-sm"},
                                 choices=[('левый', 'Левый'),
                                          ('правый', 'Правый')])
    wheeldrive = SelectField('Привод', validators=[DataRequired()],
                             render_kw={"class": "form-control form-control-sm"},
                             choices=[('передний', 'Передний'),
                                      ('задний', 'Задний'),
                                      ('полный', 'Полный')])
    color = StringField('Цвет', validators=[DataRequired()],
                        render_kw={"class": "form-control form-control-sm"})

    model = SelectField('Модель', validators=[DataRequired()],
                        render_kw={"class": "form-control form-control-sm"},
                        choices=[])
    mileage = IntegerField('Пробег', validators=[DataRequired()],
                           render_kw={"class": "form-control form-control-sm",
                                      "placeholder": "Введите пробег"})
    brand = SelectField('Марка', validators=[DataRequired()],
                        render_kw={"class": "form-control form-control-sm"},
                        choices=[])
    year = IntegerField('Год выпуска', validators=[DataRequired()],
                        render_kw={"class": "form-control form-control-sm",
                                   "placeholder": ""})
    body_type = SelectField(
        'Тип кузова', validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm",
                   "placeholder": ""},
        choices=[('седан', 'Седан'), ('универсал', 'Универсал'),
                 ('купе', 'Купе'), ('пикап', 'Пикап'), ('лимузин', 'Лимузин')])
    type_engine = SelectField('Тип двигателя', validators=[DataRequired()],
                              render_kw={"class": "form-control form-control-sm",
                                         "placeholder": ""},
                              choices=[('бензин', 'Бензин'),
                                       ('дизель', 'Дизель')])
    gear = SelectField('Коробка передач', validators=[DataRequired()],
                       render_kw={"class": "form-control form-control-sm",
                                  "placeholder": ""},
                       choices=[('механика', 'Механика'),
                                ('автомат', 'Автомат')])
    url_picture = FileField('Изображение',
                            render_kw={
                                "type": "file", "class": "form-control-file",
                                "id": "exampleFormControlFile1",
                                "multiple": ""})
    submit = SubmitField('Разместить', render_kw={"class": "btn btn-success"})


class DeleteForm(FlaskForm):
    choice_yes = SubmitField('Удалить',  render_kw={"class": "btn btn-danger"})


class EditForm(FlaskForm):
    description = TextAreaField('Описание', validators=[DataRequired()],
                                render_kw={
                                    "class": "form-control", "rows": "3",
                                    "placeholder": "Опишите "})
    mileage = IntegerField('Пробег', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Введите пробег"})
    price = IntegerField('Цена', validators=[DataRequired()],
                         render_kw={"class": "form-control",
                                    "placeholder": "100000"})
    url_picture = FileField('Изображения',
                            render_kw={
                                "type": "file", "class": "form-control-file",
                                "id": "exampleFormControlFile1",
                                "multiple": ""})

    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-success"})


class FilterForm(FlaskForm):
    price_1 = IntegerField('Цена от', validators=[InputRequired()],
                           render_kw={"class": "form-control form-control-sm",
                                      "placeholder": "10000",
                                      "value": 0})
    price_2 = IntegerField('Цена до', validators=[InputRequired()],
                           render_kw={"class": "form-control form-control-sm",
                                      "placeholder": "200000",
                                      "value": 5000000})

    submit = SubmitField('Искать', render_kw={"class": "btn btn-success"})

