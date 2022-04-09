from flask import Flask, redirect, request, abort
from data import db_session
from data.users import User
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.registration import RegistrationForm
from forms.entrance import EntranceForm
from forms.to_change_profile import To_changeForm
import os
from flask import Flask, flash, request, redirect, url_for
from forms.location import LocationForm
from werkzeug.utils import secure_filename
from key import KEY
from data.city import City
from data.location import Location
import time
from data.image import Image


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = KEY


def main():
    db_session.global_init("db/blogs.db")
    # location = Location()
    # location.name = "Чудо"
    # location.city_id = 1
    # location.comments = ""
    # location.img = ""
    # location.category = ""
    #
    # db_sess = db_session.create_session()
    # db_sess.add(location)
    # db_sess.commit()

    # city = City()
    # city.name = "Абаза	Республика Хакасия	19"
    # city.attractions = "1"
    # db_sess = db_session.create_session()
    # db_sess.add(city)
    # db_sess.commit()
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
    data_locations = db_session.create_session().query(Location).all()
    return render_template('home_page.html', data_locations=data_locations)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html', name_image=current_user.name_image, about=current_user.about)


@app.route('/to_change_profile', methods=['GET', 'POST'])
def to_change_profile():
    form = To_changeForm()
    if request.method == "GET":
        if current_user:
            form.name.data = current_user.name
            form.email.data = current_user.email
            form.about.data = current_user.about
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user.email and user.email != current_user.email:
            return render_template('to_change_profile.html', title='',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.name = form.name.data
            user.email = form.email.data
            user.about = form.about.data
            f = request.files['file']
            data = f.read()
            if str(data) == "b''":
                pass
            else:
                map_file = f"static/img/profile{current_user.id}.jpg"
                with open(map_file, "wb") as file:
                    file.write(data)
                user.name_image = f"img/profile{current_user.id}.jpg"

            db_sess.commit()
        return redirect('/')
    return render_template('to_change_profile.html', form=form, title="")


@app.route('/location/<int:id_>', methods=['GET', 'POST'])
def location_id(id_):
    db_sess = db_session.create_session()
    location = db_sess.query(Location).filter(Location.id == id_).first()
    location_list = []
    if location:
        location_ = location.img.split(', ')
        for el in location_:
            if el != "":
                image_ = db_sess.query(Image).filter(Image.id == int(el)).first()
                if image_:
                    location_list.append("img/" + image_.image)
        return render_template('location.html', location_list=location_list)
    return render_template('location.html', location_list=location_list)


@app.route('/add_location', methods=['GET', 'POST'])
@login_required
def add_location():
    form = LocationForm()
    f = open("all_cities.txt", encoding="utf8")
    data_city = [i.replace("\t", " ").replace("\n", "") for i in f]
    f.close()
    if form.validate_on_submit():
        number = 0
        mass = []
        db_sess = db_session.create_session()
        true = form.file.data[0].filename
        if true:
            for file in form.file.data:
                number += 1
                name_file = f'{time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())}0{current_user.id}_{number}.png'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], name_file))
                image = Image()
                image.image = name_file
                image.creator = current_user.id
                db_sess = db_session.create_session()
                db_sess.add(image)
                db_sess.commit()
                mass.append(str(db_sess.query(Image).filter(Image.image == name_file).first().id))
        city = db_sess.query(City).filter(City.name == form.city.data).first()
        if not city:
            city = City()
            city.name = form.city.data
            city.attractions = ""
            db_sess = db_session.create_session()
            db_sess.add(city)
            db_sess.commit()
            city = db_sess.query(City).filter(City.name == form.city.data).first()
        location = Location()
        location.name = form.name_location.data
        location.img = ", ".join(mass)
        location.city_id = city.id
        location.about = form.about.data
        db_sess.add(location)
        db_sess.commit()

        return redirect('/')
    return render_template('add_location.html', form=form, entries=data_city)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
