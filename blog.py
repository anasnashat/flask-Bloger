import functools
import sqlite3

from flask import request, render_template, redirect, url_for, Blueprint, g, abort, flash

DATABASE = 'database.db'

bp = Blueprint('bp', __name__, url_prefix='/posts')


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def get_post(post_id , check_author = True):
    post = get_db().execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if post is None:
        abort(404, f'can not found this post with id {post_id}')
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


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
    post = get_post(post_id, check_author=False)

    return render_template('show.html', post=post)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        post = connection.execute('INSERT INTO posts (title,body,author_id) VALUES (?,?,?)', (title, body, g.user.id))
        connection.commit()
        connection.close()
        return redirect(url_for('bp.index'))

    return render_template('create.html')





@bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'the title is required'
        if not body:
            error = 'the body is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE posts SET title = ? , body = ? WHERE id = ?', (title, body, post_id))
            db.commit()
            db.close()
            return redirect(url_for('bp.index'))

    return render_template('create.html', post=post)


@bp.route('/<int:post_id>/delete' , methods=['POST'])
def delete_post(post_id):
    post = get_post(post_id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id=?',(post_id,)).fetchone()
    db.commit()
    db.close()
    return redirect(url_for('bp.index'))