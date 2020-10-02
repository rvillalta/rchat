from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User


def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError('Username or Password is incorrect')
    if user_object.password != password_entered:
        raise ValidationError('Username or Password is incorrect')

class RegistrationForm(FlaskForm):
    username        = StringField('username_label', 
        validators=[
        InputRequired(message="Username Reqired"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ])
    password        = PasswordField('password_label', 
        validators=[
        InputRequired(message="Password Required"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ])
    confirm_pswd    = PasswordField('confirm_pswd_label', 
        validators=[
        InputRequired(message="Password confirmation Required"), 
        EqualTo('password', message="Passwords must match")
        ])
    submit_button   = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Username already exist. Select a different username !')

class LoginForm(FlaskForm):
    username        = StringField('username_label',
        validators = [
            InputRequired(message='Username Required')
        ])
    password        = PasswordField('password_label',
        validators = [
            InputRequired(message='Password Required'),
            invalid_credentials
        ])
    submit_button   = SubmitField('Login')


