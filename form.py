from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed



class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name',[DataRequired(message="Hãy điền First Name của bạn!")])
    inputLastName = StringField('First Name',
                                [DataRequired(message="Hãy điền Last Name của bạn!")])
    inputEmail = StringField('Email address',
                             [Email(message="Email không hợp lệ"),
                              DataRequired(message="Hãy điền Email của bạn!")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="Hãy nhập mật khẩu của bạn"),
                                   EqualTo('inputConfirmPassword', message="Mật khẩu nhập lại không khớp")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')
class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
        [Email(message="Email không hợp lệ"),
        DataRequired(message="Hãy điền Email của bạn!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Hãy nhập mật khẩu của bạn")])
    submit = SubmitField('Sign In')

class FormTask(FlaskForm):

    inputTask = StringField('push your todo',[DataRequired(message="push your todo ")])
    inputPriority=SelectField('Payload Type', coerce=int)
    submit = SubmitField('ADD')


