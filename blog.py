import functools
import sqlite3

from flask import request, render_template, redirect, url_for, Blueprint, g

DATABASE = 'database.db'

bp = Blueprint('bp', __name__, url_prefix='/posts')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def login_required(func):
    @functools.wraps(func)
    def warps_func(**kwargs):
        print(g.user)
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(**kwargs)

    return warps_func


@bp.route('/')
def index():
    connection = get_db()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()

    return render_template('index.html', posts=posts)


@bp.route('/<int:post_id>')
def show_post(post_id):
    connection = get_db()
    post = connection.execute(f"SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()

    return render_template('show.html', post=post)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        post = connection.execute('INSERT INTO posts (title,body,author_id) VALUES (?,?,?)', (title, body, 1))
        connection.commit()
        connection.close()
        return redirect(url_for('bp.index'))

    return render_template('create.html')
