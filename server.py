import subprocess
import os
from flask import Flask, render_template, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from database.db import insert_user, insert_action, select_users, select_actions
from static.scripts.img_detection.detector_img import predict
import static.scripts.pose_detection.Model.Processing

app = Flask(__name__)  # Замените на секретный ключ

app.config['DATABASE'] = 'users.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['STATIC_FOLDER'] = 'static'  # Настройка папки статических файлов
app.config['STATIC_URL_PATH'] = '/static'  # Настройка пути для доступа к статическим файлам
os.makedirs('static/uploads', exist_ok=True)

engine = db.create_engine('sqlite:///myDatabase.db')
metadata = db.MetaData()
Session = sessionmaker(bind=engine)
session = Session()


def is_video_file(filename):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    return any(filename.lower().endswith(ext) for ext in video_extensions)


def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']
    return any(filename.lower().endswith(ext) for ext in image_extensions)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('guest.html')


@app.route('/upload_a/<username>', methods=['GET', 'POST'])
def process_video_a(username: str):
    video_ai = True
    id, _, _, _, balance = select_users(username)[0]
    # ТУТ НАДО НАПИСАТЬ ЗАПРОС ПО USERNAME НА БАЛАНС
    free_count = balance
    if request.method == 'POST':
        if free_count > 0:
            free_count -= 1
            insert_action(id, 1, 2)
            # ТУТ НУЖНО НАПИСАТЬ ЗАПРОС К БД НА УМЕНЬШЕНИЕ БАЛАНСА НА 0.1
            if 'file' not in request.files:
                print('Нет файла для загрузки.')

            file = request.files['file']
            if file.filename == '':
                print('файл не выбран')

            file.save(f'static/uploads/{file.filename}')

            if is_video_file(f'static/uploads/{file.filename}'):
                # func(f'static/uploads/{file.filename}')
                subprocess.run(['python3', 'static/scripts/moi.py', f'static/uploads/{file.filename}'])
            else:
                if is_image_file(f'static/uploads/{file.filename}'):
                    video_ai = False
                    # func(f'static/uploads/{file.filename}')
                    subprocess.run(['python3', 'static/scripts/tvoi.py', f'static/uploads/{file.filename}'])
                else:
                    raise Exception("BAD ALL")
    return render_user(username, '', '')


@app.route('/auth', methods=['GET', 'POST'])
def show_redirect_page():
    show_register_fields = False

    if request.method == 'POST':
        show_register_fields = True
        if request:
            username = request.form['username']
            password = request.form['password']
            if request.form['email']:
                email = request.form['email']
                if check_register(username, password, email):
                    return render_user(username, '', '')
                else:
                    return render_template('auth.html', show_register_fields=show_register_fields)
            else:
                if check_login(username, password):
                    print("zaebok")
                    return render_user(username, '', '')
                else:
                    return render_template('auth.html', show_register_fields=show_register_fields)

    return render_template('auth.html', show_register_fields=show_register_fields)


@app.route("/user", methods=['GET', 'POST'])
def render_user(username: str, result_text_exists: str, result_image_exists: str):
    balance = select_users(username)[0][4]
    free_count = balance
    return render_template('user.html', username=username, balance=balance, result_text_exists=result_text_exists, result_image_exists=result_image_exists, free_count=free_count)


def check_login(username: str, password: str) -> bool:
    # ТУТ ТЫ ДОЛЖЕН СДЕЛАТЬ ЗАПРОС К БД, ПРОВЕРИТЬ ЛОГИН И ПАРОЛЬ И ПРОПИСАТЬ УСЛОВИЕ, ЕСЛИ ОК = ТРУ, НЕ ОК = ФОЛС
    # ТВОЙ ЗАПРОС ДОЛЖЕН ВЕРНУТЬ НЕ ОК ЕСЛИ ПОЛЬЗОВАТЕЛЬ С ТКАИМ ИМЕНЕМ УЖЕ ИМЕЕТСЯ, ЕСЛИ ПОЛЕ ПУСТОЕ
    if select_users(username) == []:
        return False
    else:
        _, name, passwd, email, _ = select_users(username)[0]
        if passwd == password:
            return True
        else:
            print(passwd, password)
            return False


def check_register(username: str, password: str, email: str) -> bool:
    # ТУТ ТЫ ДОЛЖЕН СДЕЛАТЬ ЗАПРОС К БД, И ПОПРОБОВАТЬ ЗАПИСАТЬ НОВЫЕ ДАННЫЕ
    # ТВОЙ ЗАПРОС ДОЛЖЕН ВЕРНУТЬ НЕ ОК, ЕСЛИ ПОЛЯ ПУСТЫЕ ИЛИ ТАКОЙ ЮЗЕР УЖЕ ЕСТЬ
    print(select_users(username))
    if select_users(username) is None:
        return False
    else:
        _, name, passwd, mail, _ = select_users(username)[0]
        if name == username or mail == email:
            return False
        else:
            insert_user(username, password, email)
        return True


if __name__ == '__main__':
    app.run(ssl_context=('C:\\Users\\Азиатка\\ТПЗРП\\web_site\\certficate\\server.crt', 'C:\\Users\\Азиатка\\ТПЗРП\\web_site\\certficate\\server.key'), host='0.0.0.0', port=443)
