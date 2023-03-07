from flask import Flask

from blog import bp as blogbp
from auth import auth

app = Flask(__name__)
app.secret_key = "e6c0b139e0338a77479dccd2d499f38bea68ec238b3fdaf71d1bb098d8df2a29"
app.register_blueprint(blogbp)
app.register_blueprint(auth)
app.add_url_rule('/', 'bp.index')


if __name__ == '__main__':
    app.run()
