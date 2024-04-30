import flask
import sqlalchemy
from flask import Flask, render_template, request
from data import db_session
from data.news import News
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from flask import redirect
import requests
from forms.new_news import NewsForm
from forms.register import RegisterForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id > 0)
    return render_template("index.html", news=news[::-1])


@app.route("/my_records")
def records():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id > 0)
    return render_template("records.html", news=news[::-1])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            phone=form.phone.data,
            sex=form.sex.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        f = open("static/fonts/iterators.txt", encoding="utf8")
        g = int(f.read())
        h = ""
        f.close()
        if request.method == 'POST':
            ph = request.files['file']
            if ph:
                h = f"static/photos/photo{g}.jpg"
                with open(h, "wb") as file:
                    file.write(ph.read())
        db_sess = db_session.create_session()
        news = News()
        news.type = form.type.data
        news.content = form.content.data
        news.address = form.address.data
        news.image = f"static/img/image{g}.png"
        k = form.address.data
        news.photo = h
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        photo(k)
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


def photo(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                       f"geocode={address}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = ",".join(toponym["Point"]["pos"].split())
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates}&spn=0.002,0.002&" \
                  f"l=map&pt={toponym_coodrinates},pm2rdm"
    response = requests.get(map_request)
    f = open("static/fonts/iterators.txt", encoding="utf8")
    k = int(f.read())
    map_file = "image" + str(k) + ".png"
    f.close()
    f = open("static/fonts/iterators.txt", 'w', encoding="utf8")
    f.write(str(k + 1))
    f.close()
    with open(f"static/img/{map_file}", "wb") as file:
        file.write(response.content)


def photo_reload(address, ph):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                       f"geocode={address}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = ",".join(toponym["Point"]["pos"].split())
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates}&spn=0.002,0.002&" \
                  f"l=map&pt={toponym_coodrinates},pm2rdm"
    response = requests.get(map_request)
    with open(ph, "wb") as file:
        file.write(response.content)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.type.data = news.type
            form.content.data = news.content
            form.address.data = news.address
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        p = news.photo
        k = news.image[(news.image.index("e") + 1):news.image.index(".")]
        if request.method == 'POST':
            ph = request.files['file']
            if ph:
                if p != "":
                    with open(p, "wb") as file:
                        file.write(ph.read())
                if p == "":
                    p = f"static/photos/photo{k}.jpg"
                    with open(p, "wb") as file:
                        file.write(ph.read())
            else:
                p = ""
        if news:
            news.type = form.type.data
            news.content = form.content.data
            news.address = form.address.data
            news.photo = p
            ad = form.address.data
            k = news.image
            db_sess.commit()
            photo_reload(ad, k)
            return redirect('/')
        else:
            flask.abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        k = news.image
        p = news.photo
        db_sess.delete(news)
        db_sess.commit()
        os.remove(k)
        os.remove(p)
    else:
        flask.abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("db/hero.db")
    app.run("127.0.0.1", port=3000)