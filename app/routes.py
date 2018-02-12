from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewEventForm, NewGameForm
from app.models import User, Game


@app.route('/')
@app.route('/index')
#@login_required
def index():
	games = [
		{
			'title': 'Clank!',
			'desc': 'A dungeon crawling deck builder!'
		},
		{
			'title': 'Dicey Peaks',
			'desc': 'Roll dice and push your luck!'
		}
	]
	return render_template('index.html', title='Home', games=games)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/events/new', methods=['GET', 'POST'])
@login_required
def event_new():
	games = [(game.id, game.title) for game in Game.query.all()]
	form = NewEventForm()
	form.game_id.choices = games
	#form.host_user_id = User.query.filter_by(username=current_user)[0].id
	return render_template('events_new.html', form=form)


@app.route('/games/new', methods=['GET', 'POST'])
@login_required
def game_new():
	form = NewGameForm()
	if form.validate_on_submit():
		game = Game(title=form.title.data, description=form.description.data, comments=form.comments.data
			, players_min=form.players_min.data, players_max=form.players_max.data, playtime=form.playtime.data)
		db.session.add(game)
		db.session.commit()
		return redirect(url_for('event_new'))
	return render_template('games_new.html', form=form)