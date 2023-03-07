import sqlite3
from flask import url_for, redirect, g, request, flash, render_template, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, url_prefix='/auth')

DATABASE = 'database.db'


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db




@auth.route('/register', methods=['GET', 'POST'])
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
                return redirect(url_for('auth.login'))

        flash(error)

    if request.method == "GET":
        return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        connection = get_db()
        user = connection.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            error = 'البريد الإلكتروني غير موجود برجاء التسجيل أولا '
        elif not check_password_hash(user['password'], password):
            error = 'كلمه المرور او البريد الإلكتروني غير صحيح '
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('bp.index'))

        flash(error)
    if g.user:
        return redirect(url_for('bp.index'))
    return render_template('auth/login.html')


@auth.before_app_request
def load_logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        connection = get_db()
        g.user = connection.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bp.index'))
