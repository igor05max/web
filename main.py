from flask import Flask, redirect, request, abort, jsonify
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
from key import KEY
from data.city import City
from data.location import Location
import time
from data.image import Image
from data.comment import Comment
from data import location_api
from data.similarity import search
import json
from forms.edit_a_comment import EditAComment
from datetime import datetime
from data.chat import Chat
from data.message import Message
from forms.new_chat import NewChat
from flask import make_response


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = KEY


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    app.register_blueprint(location_api.blueprint)
    user_ = db_sess.query(User).filter(User.id == 1).first()
    if user_ is None:
        user = User()
        user.name = "ADMINISTRATOR"
        user.email = "maksimov.i289@yandex.ru"
        user.about = "ADMINISTRATOR"
        user.name_image = "img/None_prof.png"
        user.set_password("111")
        db_sess.add(user)
        db_sess.commit()
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
            return render_template('registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()

        user.name = form.name.data

        user.email = form.email.data
        user.set_password(form.password.data)
        user.about = form.about.data
        user.name_image = "img/None_prof.png"
        db_sess.add(user)
        db_sess.commit()
        login_user(user)

        return redirect('/')
    return render_template('registration.html', form=form, title='Регистрация')


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "GET":
        try:
            db_sess = db_session.create_session()
            assert [i for i in db_sess.query(Message).all() if str(current_user.id) == i.recipient and not i.had_seen]
            color = "btn btn-danger"
        except (AttributeError, AssertionError):
            color = "btn btn-info"
        data_locations = db_session.create_session().query(Location).all()[::-1]
        return render_template('home_page.html', data_locations=data_locations, color=color)
    elif request.method == 'POST':
        request_text = request.form['input_ww'].strip()
        answer = search(request_text)
        if answer:
            return redirect('/search')


@app.route('/search', methods=['GET', 'POST'])
def search_():
    if request.method == "GET":
        with open('data_file.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data_locations = [db_session.create_session().query(Location).filter(Location.id == int(i)).first()
                          for i in [int(elem) for elem in data]]
        return render_template('home_page.html', data_locations=data_locations)
    elif request.method == "POST":
        request_text = request.form['input_ww'].strip()
        answer = search(request_text)
        if answer:
            return redirect('/search')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html', name_image=current_user.name_image, about=current_user.about,
                               name=current_user.name, name_id=current_user.id)


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
                user.name_image = "img/None_prof.png"
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
    if request.method == 'GET':
        db_sess = db_session.create_session()
        location = db_sess.query(Location).filter(Location.id == id_).first()
        location.count_visits = str(int(location.count_visits) + 1)
        db_sess.commit()
        location_list = []
        if location:
            comment_list = [i for i in db_sess.query(Comment).filter(Comment.location_id == id_)][::-1]
            location_ = location.img.split(', ')
            for el in location_:
                if el != "":
                    image_ = db_sess.query(Image).filter(Image.id == int(el)).first()
                    if image_:
                        location_list.append("img/" + image_.image)
            return render_template('location.html', location_list=location_list, name=location.name, location=location,
                                   comment_list=comment_list, creator=location.user.name)

    elif request.method == 'POST':
        text = request.form['comment']
        db_sess = db_session.create_session()
        if not text == "":
            comment = Comment()
            comment.comment = text
            comment.creator = current_user.id
            comment.location_id = id_
            comment.edit = ""
            db_sess.add(comment)
            db_sess.commit()
        return redirect(f'/location/{id_}')


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
        if form.city.data not in data_city:
            return render_template('add_location.html',
                                   message="Неправильный регион",
                                   entries=data_city,
                                   form=form)
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
        location.count_visits = "1"
        location.city_id = city.id
        location.creator = current_user.id
        location.about = form.about.data
        db_sess.add(location)
        db_sess.commit()

        return redirect('/')
    return render_template('add_location.html', form=form, entries=data_city)


@app.route('/profile_/<int:id_>', methods=['GET', 'POST'])
def profile_id(id_):
    if request.method == 'GET':
        try:
            assert current_user.id == id_
            return redirect('/profile')
        except (AttributeError, AssertionError):
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == id_).first()
            return render_template('profile_.html', name_image=user.name_image, about=user.about,
                                   name=user.name, name_id=user.id)
    elif request.method == 'POST':
        pass


@app.route('/city/<int:id_>', methods=['GET', 'POST'])
def city(id_):
    if request.method == 'GET':
        name = db_session.create_session().query(City).filter(City.id == id_).first().name
        data_locations = db_session.create_session().query(Location).filter(Location.city_id == id_)[::-1]
        return render_template('city.html', name_city=name, data_locations=data_locations)


@app.route('/edit_a_comment/<int:id_>', methods=['GET', 'POST'])
@login_required
def edit_a_comment(id_):
    form = EditAComment()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        comment = db_sess.query(Comment).filter(Comment.id == id_).first()
        if comment:
            form.comment.data = comment.comment
        return render_template('edit_a_comment.html', form=form)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        comment = db_sess.query(Comment).filter(Comment.id == id_).first()
        if comment:
            now = datetime.now()
            comment.edit = f"(ред. {now.strftime('%H:%M:%S')})"
            comment.comment = form.comment.data
            db_sess.commit()
        return redirect(
            f'/location/{db_sess.query(Location).filter(Location.id == comment.location_id).first().id}')
    return render_template('edit_a_comment.html', form=form)


@app.route('/delete_a_comment/<int:id_>/<int:id_2>', methods=['GET', 'POST'])
@login_required
def delete_a_comment(id_, id_2):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        comment = db_sess.query(Comment).filter(Comment.id == id_).first()
        if comment:
            if not comment.remote:
                user = db_sess.query(User).filter(User.id == id_2).first()
                if user:
                    if id_2 == 1:
                        comment.comment = "Удалён АДМИНИСТРАТОРОМ"
                    else:
                        comment.comment = f"Комментарий удалил пользователь"
                    comment.remote = True
                    now = datetime.now()
                    comment.edit = f"({now.strftime('%H:%M:%S')})"
                    db_sess.commit()
            return redirect(
                f'/location/{db_sess.query(Location).filter(Location.id == comment.location_id).first().id}')
        return redirect('/')


@app.route('/chat/<int:id_>', methods=['GET', 'POST'])
@login_required
def chat(id_):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        chat_list = []
        for i in db_sess.query(Chat).all():
            ms = list(map(int, i.participants.split(", ")))
            if id_ in ms:
                if ms[0] != id_:
                    id_2 = ms[0]
                else:
                    id_2 = ms[1]
                user = db_sess.query(User).filter(User.id == id_2).first()
                chat_list.append([i, user,
                                  db_sess.query(Message).filter(Message.id ==
                                                                int(i.list_messages.split(", ")[-1])).first()])
                chat_list = sorted(chat_list, key=lambda x: x[2].modified_date, reverse=True)

        return render_template('chat.html', chat_list=chat_list)
    elif request.method == 'POST':
        pass


@app.route('/chat_/<int:id_>', methods=['GET', 'POST'])
@login_required
def chat_id(id_):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        chat = db_sess.query(Chat).filter(Chat.id == id_).first()
        list_message_ = [db_sess.query(Message).filter(Message.id == id_i).first()
                         for id_i in [i for i in list(map(int, chat.list_messages.split(", ")))]]
        for i in list_message_:
            if i.recipient == str(current_user.id) and not i.had_seen:
                i.had_seen = True
        db_sess.commit()
        message_user_2 = list_message_[0]
        if message_user_2.recipient == str(current_user.id):
            message_user_2 = message_user_2.creator
        else:
            message_user_2 = message_user_2.recipient
        message_user_2 = db_sess.query(User).filter(User.id == int(message_user_2)).first()
        return render_template('chat_.html', list_message_=list_message_, current_user_id=str(current_user.id),
                               message_user_2=message_user_2, chat=chat)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        message = Message()
        message.creator = str(current_user.id)
        chat = db_sess.query(Chat).filter(Chat.id == id_).first()
        message_recipient_chat = chat.participants.split(", ")
        if int(message_recipient_chat[0]) == current_user.id:
            message.recipient = message_recipient_chat[1]
        else:
            message.recipient = message_recipient_chat[0]
        message.message = request.form['message']
        db_sess.add(message)
        db_sess.commit()

        chat.list_messages = chat.list_messages + ", " + str([i for i in db_sess.query(Message).all()
                                                              if i.creator == str(current_user.id)][-1].id)
        db_sess.commit()

        return redirect(f'/chat_/{id_}')


@app.route('/new_chat/<int:id_>', methods=['GET', 'POST'])
@login_required
def new_chat(id_):
    form = NewChat()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        chat_not_new = db_sess.query(Chat).filter(Chat.participants.in_([f'{current_user.id}, {id_}',
                                                                         f'{id_}, {current_user.id}'])).first()
        if chat_not_new:
            return redirect(f'/chat_/{chat_not_new.id}')
        else:
            return render_template('new_chat.html', form=form)
    elif form.validate_on_submit():
        db_sess = db_session.create_session()
        message_new_chat_text = form.message.data
        message_new_chat = Message()
        message_new_chat.message = message_new_chat_text
        message_new_chat.creator = str(current_user.id)
        message_new_chat.recipient = str(id_)
        db_sess.add(message_new_chat)
        db_sess.commit()
        message_new_id = db_sess.query(Message).filter(Message.creator == str(current_user.id),
                                                       Message.recipient == str(id_)).first()
        if message_new_id:
            message_new_id = message_new_id.id
            new_chat = Chat()
            new_chat.list_messages = str(message_new_id)
            new_chat.participants = f"{current_user.id}, {id_}"
            db_sess.add(new_chat)
            db_sess.commit()
        chat_not_new = db_sess.query(Chat).filter(Chat.participants.in_([f'{current_user.id}, {id_}',
                                                                         f'{id_}, {current_user.id}'])).first()
        if chat_not_new:
            return redirect(f'/chat_/{chat_not_new.id}')


@app.route('/delete_a_message/<int:message_id>/<int:current_user_id>/<int:chat_id>')
@login_required
def delete_a_message(message_id, current_user_id, chat_id):
    if current_user.id == current_user_id:
        db_sess = db_session.create_session()
        message = db_sess.query(Message).filter(Message.id == message_id).first()
        if message:
            dt = datetime.now()
            dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            message.message = f"Удалено сообщение ({dt})"
            message.remote = True
            db_sess.commit()
        return redirect(f'/chat_/{chat_id}')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(500)
def not_found(error):
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
