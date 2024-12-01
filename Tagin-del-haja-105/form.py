from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, EmailField, StringField, IntegerField)
from wtforms.validators import InputRequired, Length

class SignupForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[InputRequired(), Length(min=7, max=1000)], render_kw={"placeholder": "Email Address"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    conpassword = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Create Account", render_kw={"class": "button"})
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=7, max=1000)], render_kw={"placeholder": "Email Address"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In", render_kw={"class": "button"})
class RecoveryForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=7, max=1000)], render_kw={"placeholder": "Email Address"})
    submit = SubmitField("Send Code", render_kw={"class": "button"})
class VerifyForm(FlaskForm):
    code = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Verification Code"})
    submit = SubmitField("Verify", render_kw={"class": "button"})
class ResetPasswordForm(FlaskForm):
    newpassword = StringField(validators=[InputRequired()], render_kw={"placeholder": "New Password"})
    submit = SubmitField("Save Changes", render_kw={"class": "button"})