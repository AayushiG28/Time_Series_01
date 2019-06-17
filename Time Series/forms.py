from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

import bs4 as bs  
import urllib.request
import re  
import nltk

pwd_regex = '^(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{7,30}$'
pwd_msg = 'Should be 7-30 in length. No whitespaces. Requires at least 1 of each: lowercase, uppercase, numeric, special character'

class LandingPage(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	btncontinue = SubmitField('Continue')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password',  validators=[DataRequired(), Regexp(pwd_regex, message=pwd_msg)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password',  validators=[DataRequired(), Regexp(pwd_regex, message=pwd_msg)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')