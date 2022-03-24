from flask import Flask, redirect, request, abort
from data import db_session
from data.users import User
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.registration import RegistrationForm
from forms.entrance import EntranceForm
from forms.to_change_profile import To_changeForm

from key import KEY

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = KEY

photo_user = None


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/entrance', methods=['GET', 'POST'])
def entrance():
    form = EntranceForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('entrance.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('entrance.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()

        user.name = form.name.data

        user.email = form.email.data
        user.set_password(form.password.data)
        user.about = form.about.data
        db_sess.add(user)
        db_sess.commit()
        login_user(user)

        return redirect('/')
    return render_template('registration.html', form=form, title='Регистрация')


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home_page.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html', name_image=current_user.name_image, about=current_user.about)


@app.route('/to_change_profile', methods=['GET', 'POST'])
def to_change_profile():
    form = To_changeForm()
    db_sess = db_session.create_session()
    user_ = db_sess.query(User).filter(User.id == current_user.id).first()
    photo_user = user_.name_image
    if request.method == "GET":
        if user_:
            form.name.data = user_.name
            form.email.data = user_.email
            form.about.data = user_.about
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        email_ = db_sess.query(User).filter(User.email == form.email.data).first().email

        if email_ and email_ != user_.email:
            return render_template('to_change_profile.html', title='',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if user_:
            user_.name = form.name.data
            user_.email = form.email.data
            user_.about = form.about.data
            print(photo_user)
            user_.name_image = photo_user
            db_sess.commit()
        return redirect('/')
    return render_template('to_change_profile.html', form=form, title="")


@app.route('/profile_photo/<int:id>', methods=['GET', 'POST'])
def profile_photo(id):
    db_sess = db_session.create_session()
    user_ = db_sess.query(User).filter(User.id == id).first()
    if request.method == 'GET':
        return render_template('profile_photo.html', name_image=user_.name_image)
    elif request.method == 'POST':
        f = request.files['file']
        data = f.read()
        if str(data) == "b''":
            map_file = None
        else:
            map_file = f"static/img/profile{user_.id}.jpg"
            with open(map_file, "wb") as file:
                file.write(data)
        global photo_user
        if map_file is not None:
            photo_user = map_file[7::]
        else:
            photo_user = None
        return render_template('profile_photo.html', name_image=photo_user)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
