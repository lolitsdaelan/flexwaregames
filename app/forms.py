from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Game


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('This username already exists!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This email already exists!')


class NewGameForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	comments = StringField('Additional Comments')
	players_min = IntegerField('Minimum Players', validators=[DataRequired()])
	players_max = IntegerField('Maximum Players', validators=[DataRequired()])
	playtime = IntegerField('Playtime (minutes)', validators=[DataRequired()])
	submit = SubmitField('Add')


class NewEventForm(FlaskForm):
	#game_id = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
	#game_id = SelectField('Games',choices=[(game.id, game.title) for game in Game.query.all()])
	game_id = SelectField('Games', choices=[])
	location = StringField('Location', validators=[DataRequired()])
	timestamp = DateTimeField('Date/Time', validators=[DataRequired()])
	submit = SubmitField('Create!')

