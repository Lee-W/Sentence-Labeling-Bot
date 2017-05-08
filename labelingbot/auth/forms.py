from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

from ..models import User


class LoginForm(FlaskForm):
    name = StringField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')
