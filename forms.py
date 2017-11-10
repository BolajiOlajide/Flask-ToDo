from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class AddTodoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()], 
                       render_kw={"placeholder": "add a to-do..."})
    status = StringField('status')

    class Meta:
        csrf = False


class AuthenticationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})

    class Meta:
        csrf = False
