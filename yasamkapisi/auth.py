import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from yasamkapisi.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
""""""""""""""""""
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        surname=request.form['surname']
        password = request.form['password']
        tc=request.form['tc']
        birim=request.form['birim']
        dogumtarihi=request.form['dogumtarihi']
        telefon=request.form['telefon']
        eposta=request.form['eposta']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not surname:
            error = 'Surname is required.'
        elif not tc:
            error = 'tc is required.'
        elif not birim:
            error = 'birim is required.'
        elif not dogumtarihi:
            error = 'Dogum tarihi is required.'
        elif not telefon:
            error = 'Telefon is required.'
        elif not eposta:
            error = 'E posta is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            session.clear()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
""""""""""""""""""""""""""""""""""""

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password=request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE password = ?', (password,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            return  redirect(url_for('auth.register'))
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            return redirect(url_for('auth.forgot'))

        if error is None:
           session.clear()
           session['username'] = user['username']
           return redirect(url_for('auth.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.route('/index', methods=('GET', 'POST'))
def index():
   

       


    return render_template('auth/index.html')
""""""""""""
@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'POST':
        eposta = request.form['eposta']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE eposta = ?', (eposta,)
        ).fetchone()

        if user is None:
            error = 'Incorrect eposta.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            return  redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/forgot.html')
@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view 