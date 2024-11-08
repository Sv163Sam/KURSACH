from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Key'  # Замените на секретный ключ

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}
app.config['DATABASE'] = 'users.db'  # Имя файла базы данных
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], balance=session['balance'])
    else:
        return render_template('index.html')
# Отображаем auth.html


@app.route('/auth', methods=['POST'])
def auth():
    auth_type = request.form.get('auth-type')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    # Проверка введенных данных
    if auth_type == 'login':
        user = check_login(username, password)  # Ваша функция проверки входа
        if user:
            session['username'] = username
            session['balance'] = user['balance']  # Добавьте логику получения баланса
            return jsonify({'success': True, 'message': 'Успешный вход', 'balance': user['balance']})
        else:
            return jsonify({'success': False, 'message': 'Неверный логин или пароль'})
    elif auth_type == 'register':
        # session сделать
        # Проверка введенных данных
        if register_user(username, password, email):  # Ваша функция регистрации
            return jsonify({'success': True, 'message': 'Успешная регистрация'})
        else:
            return jsonify({'success': False, 'message': 'Ошибка регистрации'})
    else:
        return jsonify({'success': False, 'message': 'Неверный тип авторизации'})


@app.route('/upload', methods=['POST'])
def upload():
    if 'video-file' not in request.files:
        return jsonify({'success': False, 'message': 'Файл не выбран'})
    file = request.files['video-file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Файл не выбран'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Проверяем тип файла
        if filename.lower().endswith(('.mp4')):
            # Вызываем скрипт для анализа видео
            result = process_video(filename)
            return jsonify({'success': True, 'message': result})
        else:
            # Вызываем скрипт для анализа изображения
            result = process_image(filename)
            return jsonify({'success': True, 'message': result, 'image': result})

    return jsonify({'success': False, 'message': 'Неверный тип файла'})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Местозаполнители для функций работы с БД
def check_login(username, password):
    user = {'username': username, 'password': password, 'balance': 150, 'email': ""}
    return user


def register_user(username, password, email):
    user = {'username': username, 'password': password, 'balance': 150, 'email': email}
    return user


def process_video(filename):
    result = []
    return result


def process_image(filename):
    result = []
    return result


if __name__ == '__main__':
    app.run(debug=True)




"""from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'users.db' # Имя файла базы данных
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'


# Получение соединения с базой данных
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    return db


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Обработка авторизации
@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        # Успешная авторизация
        return jsonify({'success': True, 'user_id': user[0], 'balance': user[4]})
    else:
        # Неверный логин или пароль
        return jsonify({'success': False, 'message': 'Неверный логин или пароль'})


# Обработка регистрации
@app.route('/register', methods=['POST'])
def register():
    db = get_db()
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        # Пользователь с таким логином или почтой уже существует
        return jsonify({'success': False, 'message': 'Пользователь с таким логином или почтой уже существует'})
    else:
        try:
            cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
            db.commit()
            return jsonify({'success': True, 'message': 'Регистрация прошла успешно'})
        except sqlite3.IntegrityError:
            # Ошибка при вставке данных (например, дубликат)
            return jsonify({'success': False, 'message': 'Ошибка при регистрации'})


# Обработка запроса на анализ видео
@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    db = get_db()
    user_id = request.form.get('user_id')
    video_data = request.form.get('video_data')
    network = request.form.get('network')

    # Проверка баланса пользователя
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = cursor.fetchone()[0]

    # Стоимость анализа
    analysis_cost = 1.0  # Задайте стоимость анализа

    if balance >= analysis_cost:
        # Достаточно средств
        # ... (Выполнить анализ видео с помощью выбранной нейронной сети)
        result = "Результат анализа" # Замените на фактический результат

        # Списать средства с баланса
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id=?", (analysis_cost, user_id))
        db.commit()

        return jsonify({'success': True, 'result': result, 'balance': balance - analysis_cost})
    else:
        # Недостаточно средств
        return jsonify({'success': False, 'message': 'Недостаточно средств'})


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"""
