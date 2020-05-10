from flask import Flask, render_template, request, json
from forms import LoginForm

from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

from users_data import User
from flask import render_template, flash, redirect


@app.route('/SignIn', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/handle_data_for_sign_in', methods=['POST'])
def handle_data_for_sign_in():
    email = request.form['email']
    password = request.form['password']
    if db.session.query(User).filter_by(email = email).first() is None:
       return sign_up()
    else:
        u = db.session.query(User).filter_by(email = email).first()
        if (u.password == password):
            return show_home_page(u.id)
        else:
            return login()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def sign_up():
    return render_template('signup.html')


@app.route('/Home/<_id>')
def show_home_page(_id):
    return render_template('dairy.html')


@app.route('/handle_data_for_sign_up', methods=['POST'])
def handle_data_for_sign_up():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    _id = hash(email)
    if db.session.query(User).filter_by(email = email).first() is None:
        is_created = True
        user = User(email=email, name=name, active=True, password=password, id = _id)
        db.session.add(user)
        db.session.commit()
    else:
        is_created = False
    return render_template('login.html', user_id = _id, succeed = is_created)


if __name__ == '__main__':
    app.run()

