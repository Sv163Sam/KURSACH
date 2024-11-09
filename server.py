from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)  # Замените на секретный ключ

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}
app.config['DATABASE'] = 'users.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
os.makedirs('static/uploads', exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('user.html')


@app.route('/upload', methods=['GET', 'POST'])
def process_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('Нет файла для загрузки.')

        file = request.files['file']

        if file.filename == '':
            print('файл не выбран')

        file.save(f'static/uploads/{file.filename}')  # Убедитесь, что папка uploads существует

        print('файл успешно загружен')

    result_image_exists = os.path.exists(os.path.join(app.root_path, 'static', 'imgs', 'result.png'))
    return render_template('guest.html', result_image_exists=result_image_exists)


@app.route('/upload_a', methods=['GET', 'POST'])
def process_video_a():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('Нет файла для загрузки.')

        file = request.files['file']

        if file.filename == '':
            print('файл не выбран')

        file.save(f'static/uploads/{file.filename}')  # Убедитесь, что папка uploads существует

        print('файл успешно загружен')

    result_image_exists = os.path.exists(os.path.join(app.root_path, 'static', 'imgs', 'result.png'))
    return render_template('guest.html', result_image_exists=result_image_exists)

@app.route('/auth', methods=['GET', 'POST'])
def show_redirect_page():
    show_register_fields = False
    if request.method == 'POST':
        print(request.form)
        show_register_fields = True

    return render_template('auth.html', show_register_fields=show_register_fields)


if __name__ == '__main__':
    app.run(debug=True)

