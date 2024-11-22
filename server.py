import subprocess
import os
from flask import Flask, render_template, request

app = Flask(__name__)  # Замените на секретный ключ

app.config['DATABASE'] = 'users.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['STATIC_FOLDER'] = 'static'  # Настройка папки статических файлов
app.config['STATIC_URL_PATH'] = '/static'  # Настройка пути для доступа к статическим файлам
os.makedirs('static/uploads', exist_ok=True)


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
    # ТУТ НАДО НАПИСАТЬ ЗАПРОС ПО USERNAME НА БАЛАНС
    balance = 1
    free_count = balance / 0.1
    if request.method == 'POST':
        if free_count > 0:
            free_count -= 1
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

    if free_count > 0:
        if video_ai:
            result_text = os.path.exists(os.path.join(app.root_path, 'static', 'results', 'result.txt'))
            if result_text:
                with open('static/results/result.txt', 'r', encoding='utf-8') as file:
                    content = file.read()
                return render_user(username, content, '')
            else:
                return render_user(username, '', '')
        elif not video_ai:
            result_image = os.path.exists(os.path.join(app.root_path, 'static', 'results', 'result.txt'))
            if result_image:
                with open('static/results/result.txt', 'r', encoding='utf-8') as file:
                    content = file.read()
                return render_user(username, '', content)
            else:
                return render_user(username, '', '')
        else:
            return render_user(username, '', '')
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
                    return render_user(username, '', '')
                else:
                    return render_template('auth.html', show_register_fields=show_register_fields)
            else:
                if check_login(username, password):
                    return render_user(username, '', '')
                else:
                    return render_template('auth.html', show_register_fields=show_register_fields)

    return render_template('auth.html', show_register_fields=show_register_fields)


@app.route("/user", methods=['GET', 'POST'])
def render_user(username: str, result_text_exists: str, result_image_exists: str):
    balance = 1
    # ТУТ ТЫ ДОЛЖЕН НАПИСАТЬ ЗАПРОС К БД, ЧТОБЫ ВЫВЕСТИ БАЛАНС И ПРИСВОИТЬ ЕГО В ПЕРЕМЕННУЮ
    free_count = balance / 0.1
    return render_template('user.html', username=username, balance=balance, result_text_exists=result_text_exists, result_image_exists=result_image_exists, free_count=free_count)


def check_login(username: str, password: str) -> bool:
    # ТУТ ТЫ ДОЛЖЕН СДЕЛАТЬ ЗАПРОС К БД, ПРОВЕРИТЬ ЛОГИН И ПАРОЛЬ И ПРОПИСАТЬ УСЛОВИЕ, ЕСЛИ ОК = ТРУ, НЕ ОК = ФОЛС
    # ТВОЙ ЗАПРОС ДОЛЖЕН ВЕРНУТЬ НЕ ОК ЕСЛИ ПОЛЬЗОВАТЕЛЬ С ТКАИМ ИМЕНЕМ УЖЕ ИМЕЕТСЯ, ЕСЛИ ПОЛЕ ПУСТОЕ
    return True


def check_register(username: str, password: str, email: str) -> bool:
    # ТУТ ТЫ ДОЛЖЕН СДЕЛАТЬ ЗАПРОС К БД, И ПОПРОБОВАТЬ ЗАПИСАТЬ НОВЫЕ ДАННЫЕ
    # ТВОЙ ЗАПРОС ДОЛЖЕН ВЕРНУТЬ НЕ ОК, ЕСЛИ ПОЛЯ ПУСТЫЕ ИЛИ ТАКОЙ ЮЗЕР УЖЕ ЕСТЬ
    return True


if __name__ == '__main__':
    app.run(ssl_context=('/Users/vladimirskobcov/Desktop/Labs/KURSACH/certficate/server.crt', '/Users/vladimirskobcov/Desktop/Labs/KURSACH/certficate/server.key'), host='0.0.0.0', port=443)
