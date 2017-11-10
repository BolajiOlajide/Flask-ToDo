from flask import Flask, render_template, request, url_for, redirect, flash, g
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
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


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AuthenticationForm()

    if request.method == 'GET':
        return render_template('index.html', form=form)

    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('index'))
    login_user(registered_user)
    return redirect(url_for('dashboard'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AuthenticationForm()

    if request.method == 'GET':
        return render_template('signup.html', form=form)

    user = User(username=request.form['username'],
                password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AddTodoForm()
    current_todos = Todo.query.filter_by(created_by=g.user.user_id, status='current')
    completed_todos = Todo.query.filter_by(created_by=g.user.user_id, status='completed')
    if request.method == 'POST':
        if 'submit' in request.form.keys():
            name = request.form['submit']
            todo = Todo.query.filter_by(name=name, created_by=g.user.user_id).first()
            print(name)
            todo.status = 'completed'
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('dashboard'))
        name = request.form['name']
        todo = Todo(name=name, status='current')
        todo.created_by = g.user.user_id
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, current_todos=current_todos, completed_todos=completed_todos)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


if __name__ == '__main__':
    manager.run()
