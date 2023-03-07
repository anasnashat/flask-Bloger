from flask import Flask, request, redirect, url_for, render_template, flash, session, g
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "e6c0b139e0338a77479dccd2d499f38bea68ec238b3fdaf71d1bb098d8df2a29"

DATABASE = 'database.db'


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/posts/')
def index():
    connection = get_db()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()

    return render_template('index.html', posts=posts)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    connection = get_db()
    post = connection.execute(f"SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()

    return render_template('show.html', post=post)


@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        post = connection.execute('INSERT INTO posts (title,body,author_id) VALUES (?,?,?)', (title, body, 1))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        error = None
        if not name:
            error = 'الاسم مطلوب'
        elif not email:
            error = 'البريد الإلكتروني مطلوب'
        elif not username:
            error = 'اسم المستخدم مطلوب'
        elif not password:
            error = 'كلمة المرور مطلوبة'
        elif not password2:
            error = 'تأكيد كلمة المرور مطلوب'
        elif password != password2:
            error = 'كلمة المرور غير متطابقة'
        if error is None:
            connection = get_db()
            try:
                user = connection.execute('INSERT INTO users (username,name,email,password) VALUES (?,?,?,?)',
                                          (username, name, email, generate_password_hash(password)))
                connection.commit()
                connection.close()
            except sqlite3.IntegrityError:
                error = f"المستخدم {username} موجود بالفعل"
            else:
                return redirect(url_for('login'))

        flash(error)

    if request.method == "GET":
        return render_template('auth/register.html')



if __name__ == '__main__':
    app.run()
