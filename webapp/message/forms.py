from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    message = TextAreaField('Message',
                            validators=[DataRequired(),
                                        Length(min=0, max=140)],
                            render_kw={"class": "form-control",
                                       "placeholder": "Enter your message"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-success"})
