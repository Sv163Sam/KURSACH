document.addEventListener('DOMContentLoaded', function (message) {
    const uploadButton = document.querySelector('.upload-button');
    const videoFile = document.getElementById('video-file');
    const resultContainer = document.querySelector('.result-container');
    const resultText = document.querySelector('.result-text');
    const resultImage = document.querySelector('.result-image');
    const balanceContainer = document.querySelector('.balance-container');
    const balanceText = document.querySelector('.balance-text');
    const errorContainer = document.querySelector('.error-container');
    const errorMessage = document.querySelector('.error-message');
    const authButton = document.querySelector('.auth-button');
    const authPopup = document.querySelector('.auth-popup');
    const closeButton = document.querySelector('.close-button');
    const authForm = document.querySelector('.auth-form');
    const authSubmitButton = document.querySelector('.auth-submit');
    const loginRadio = document.getElementById('login');
    const registerRadio = document.getElementById('register');
    const registerFields = document.getElementById('register-fields');
    const userButton = document.querySelector('.user-button'); // Добавлен элемент userButton
    const userMenu = document.querySelector('.user-menu'); // Добавлен элемент userMenu

    // Обработчик клика на кнопку загрузки
    uploadButton.addEventListener('click', function() {
        videoFile.click();
    });

    // Обработчик выбора файла
    videoFile.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('video-file', file);

        // Отправка запроса на сервер
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.image) {
                    resultImage.src = data.image;
                    resultImage.style.display = 'block';
                    resultContainer.style.display = 'block';
                    resultText.style.display = 'none';
                } else {
                    resultText.textContent = data.message;
                    resultText.style.display = 'block';
                    resultContainer.style.display = 'block';
                    resultImage.style.display = 'none';
                }
                errorContainer.style.display = 'none';
            } else {
                errorMessage.textContent = data.message;
                errorContainer.style.display = 'block';
                resultContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            errorMessage.textContent = 'Произошла ошибка!';
            errorContainer.style.display = 'block';
            resultContainer.style.display = 'none';
        });
    });

    // Авторизация
    authButton.addEventListener('click', function() {
        authPopup.style.display = 'block';
    });

    closeButton.addEventListener('click', function() {
        authPopup.style.display = 'none';
    });

    // Обработчик для формы авторизации/регистрации
    authForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        const authType = document.querySelector('input[name="auth-type"]:checked').value;
        alert(authType);
        const formData = new FormData(authForm);
        formData.append('auth-type', authType);

        fetch('/auth', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновляем UI при успешной авторизации
                authPopup.style.display = 'none';
                authButton.style.display = 'none'; // Скрываем кнопку входа
                userButton.textContent = data.username; // Устанавливаем текст кнопки пользователя
                userButton.style.display = 'block'; // Отображаем кнопку пользователя
                balanceContainer.style.display = 'block';
                balanceText.textContent = `Баланс: ${data.balance}`;
            } else {
                // Отображение ошибок
                authForm.querySelectorAll('.error-message').forEach(message => {
                    message.textContent = data.message;
                    message.style.display = 'block';
                });
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });

    // Переключение между входом и регистрацией
    loginRadio.addEventListener('change', function() {
        registerFields.style.display = 'none';
        authSubmitButton.textContent = 'Войти';
    });

    registerRadio.addEventListener('change', function() {
        registerFields.style.display = 'block';
        authSubmitButton.textContent = 'Зарегистрироваться';
    });

    // Выпадающее меню пользователя
    userButton.addEventListener('click', function() {
        userMenu.style.display = 'block';
    });

    document.addEventListener('click', function(event) {
        if (!userButton.contains(event.target) && !userMenu.contains(event.target)) {
            userMenu.style.display = 'none';
        }
    });
});
