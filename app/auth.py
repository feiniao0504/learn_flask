from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', method=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif db.execute('SELECT id from user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already exists'

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', method=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()
        error = None

        user = db.execute('SELECT * FROM user WHERE username = ?', (username, )).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password)
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')
