# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

##########################
# CONFIGURATION
##########################

DATABASE = '/tmp/dewey.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our application
app = Flask(__name__)
app.config.from_object(__name__)

##########################
# FEATURES
##########################

@app.route('/')
def show_books():
    cur = g.db.execute('select title, author from books order by id desc')
    books = [dict(title=row[0], author=row[1]) for row in cur.fetchall()]
    return render_template('show_books.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into books (title, author, description, isbn) values (?, ?, ?, ?)',
                 [request.form['title'], request.form['author'], request.form['description'], request.form['isbn']])
    g.db.commit()
    flash('New book was successfully added')
    return redirect(url_for('show_books'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_books'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('show_books'))

##########################
#  DATABASE
##########################

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()