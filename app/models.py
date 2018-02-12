from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), index=True, unique=True)
	description = db.Column(db.String())
	comments = db.Column(db.String())
	players_min = db.Column(db.Integer)
	players_max = db.Column(db.Integer)
	playtime = db.Column(db.Integer)

	def __repr__(self):
		return '<id={}, title={}>'.format(self.id, self.title)


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	host_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	location = db.Column(db.String())
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	