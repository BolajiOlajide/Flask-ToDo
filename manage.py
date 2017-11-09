from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_required
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
import dotenv

from config import config
from models import db, User, Todo
from forms import AddTodoForm, AuthenticationForm


dotenv.load()

app = Flask(__name__)

config_name = dotenv.get('CONFIG')

app.config.from_object(config[config_name])
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AuthenticationForm(csrf_enabled=False)

    return render_template('index.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AuthenticationForm(csrf_enabled=False)

    if request.method == 'POST':
        user = User(request.form['username'] , request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = AddTodoForm(csrf_enabled=False)
    # todos = Todo.query.filter_by(created_by=g.user.user_id)
    todos = Todo.query.all()
    return render_template('dashboard.html', form=form)


if __name__ == '__main__':
    manager.run()
