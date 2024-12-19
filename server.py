import datetime
import os
import uuid
import shutil
import hashlib
from functools import wraps
from time import sleep

import jwt
import sqlalchemy as db
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from database.db import insert_user, select_users
from flask import Flask, render_template, request, abort, jsonify
import static.scripts.pose_detection.Model.Processing as nv
from static.scripts.img_detection.detector_img import predict
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

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

ui_request = []


def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Файл {file_path} успешно удален.')
        else:
            print(f'Файл {file_path} не найден.')
    except Exception as e:
        print(f'Ошибка при удалении файла {file_path}: {e}')


def is_video_file(filename):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    return any(filename.lower().endswith(ext) for ext in video_extensions)


def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']
    return any(filename.lower().endswith(ext) for ext in image_extensions)


@app.route('/', methods=['GET'])
def index():
    return render_template('guest.html')


def create_token(username):
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Токен действителен 1 час
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.form.get('token')
        print(token)
        if not token:
            abort(403)

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = data['username']

        return f(current_user, *args, **kwargs)

    return decorated_function


@app.route('/upload_a', methods=['POST', 'GET'])
@token_required
def process_video_a(current_user):
    username = current_user

    global ui_request
    id, _, _, _, balance = select_users(username)[0]
    free_count = balance

    if request.method == 'POST':
        if free_count <= 0:
            return render_user(username, '', '')

        if 'file' not in request.files:
            return render_user(username, '', 'Нет файла для загрузки.')

        file = request.files['file']
        if file.filename == '' and is_video_file(file.filename) and is_image_file(file.filename):
            return render_user(username, '', 'Недопустимый файл.')

        unique_filename = f"{uuid.uuid4()}{Path(file.filename).suffix}"
        file.save(f'static/uploads/{unique_filename}')

        try:
            ui_request.append([username, unique_filename])
            while ui_request and username != ui_request[0][0]:
                sleep(0.01)

            if is_video_file(f'static/uploads/{ui_request[0][1]}'):
                shutil.copy(f'static/uploads/{ui_request[0][1]}',
                            f'static/scripts/pose_detection/Source/{ui_request[0][1]}')
                os.rename('static/scripts/pose_detection/Source/' + ui_request[0][1],
                          "static/scripts/pose_detection/Source/91" +
                          Path(f'static/scripts/pose_detection/Source/{ui_request[0][1]}').suffix)
                content = nv.neuro_processing()
                ui_request.pop(0)
                if os.path.exists('static/uploads/' + file.filename):
                    delete_file('static/uploads/' + file.filename)
                    if os.path.exists('static/scripts/pose_detection/Source/91.mp4'):
                        delete_file('static/scripts/pose_detection/Source/91.mp4')
                        if os.path.exists('static/scripts/pose_detection/Poses/90.txt'):
                            delete_file('static/scripts/pose_detection/Poses/90.txt')
                return render_user(username, content, '')
                pass
            elif is_image_file(f'static/uploads/{ui_request[0][1]}'):
                content = predict('static/uploads/' + ui_request[0][1])
                if content:
                    ui_request.pop(0)
                    if os.path.exists('static/uploads/' + file.filename):
                        delete_file('static/uploads/' + file.filename)
                    return render_user(username, '', "Фото сгенерированной нейронной сетью")
                else:
                    ui_request.pop(0)
                    if os.path.exists('static/uploads/' + file.filename):
                        delete_file('static/uploads/' + file.filename)
                    return render_user(username, '', "Фото оригинальное")
                pass
            else:
                return render_user(username, '', 'Недопустимый файл.')
        finally:
            if os.path.exists(f'static/uploads/{unique_filename}'):
                delete_file(f'static/uploads/{unique_filename}')
    else:
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
                    token = create_token(username)
                    return render_user(username, '', '', token)
                else:
                    return render_template('auth.html', show_register_fields=show_register_fields, show_alert=True)
            else:
                if check_login(username, password):
                    token = create_token(username)
                    return render_user(username, '', '', token)
                else:
                    return render_template('auth.html', show_alert=True)
        else:
            abort(403)
    return render_template('auth.html', show_register_fields=show_register_fields)


def render_user(username: str = '', result_text_exists: str = '', result_image_exists: str = '', token: str = '',
                flag_exists: bool = False):

    balance = select_users(username)[0][4]
    free_count = balance
    return render_template('user.html', username=username, balance=balance,
                           result_text_exists=result_text_exists,
                           result_image_exists=result_image_exists,
                           free_count=free_count, token=token)


def check_login(username: str, password: str) -> bool:
    if select_users(username):
        _, name, passwd, email, _ = select_users(username)[0]
        if passwd == str(hashlib.sha256(password.encode()).hexdigest()):
            return True
        else:
            return False
    else:
        return False


def check_register(username: str, password: str, email: str) -> bool:
    if select_users(username):
        _, name, passwd, mail, _ = select_users(username)[0]

        if name == username or mail == email:
            return False
        else:
            insert_user(username, password, email)
        return True
    else:
        insert_user(username, password, email)
        return True


if __name__ == '__main__':
    app.run(ssl_context=('certficate/server.crt', 'certficate/server.key'), host='0.0.0.0', port=443)
