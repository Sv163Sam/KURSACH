from flask import Flask, render_template, request, jsonify
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
    analysis_cost = 1.0 # Задайте стоимость анализа

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
