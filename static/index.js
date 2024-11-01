const authButton = document.querySelector('.auth-button');
const authPopup = document.querySelector('.auth-popup');
const closeButton = document.querySelector('.close-button');
const authForm = document.querySelector('.auth-form');
const loginRadio = document.querySelector('#login');
const registerRadio = document.querySelector('#register');
const registerFields = document.querySelector('#register-fields');
const authSubmitButton = document.querySelector('.auth-submit');
const videoUploadButton = document.querySelector('.upload-button');
const videoFile = document.querySelector('#video-file');
const networkSelect = document.querySelector('#network-select');
const resultContainer = document.querySelector('.result-container');
const balanceContainer = document.querySelector('.balance-container');
const errorContainer = document.querySelector('.error-container');
const usernameInput = document.querySelector('#username');
const passwordInput = document.querySelector('#password');
const emailInput = document.querySelector('#email');
const balanceText = document.querySelector('.balance-text');
const costText = document.querySelector('.cost-text');
const userProfile = document.querySelector('.user-profile');
const userProfileButton = document.querySelector('.user-profile button');
const userProfileMenu = document.querySelector('.user-profile ul');

// Установка обработчика для кнопки авторизации/регистрации
authButton.addEventListener('click', () => {
    authPopup.style.display = 'block';
});

// Установка обработчика для кнопки закрытия попапа
closeButton.addEventListener('click', () => {
    authPopup.style.display = 'none';
});

// Установка обработчиков для переключателя "Вход/Регистрация"
loginRadio.addEventListener('change', () => {
    registerFields.style.display = 'none';
    authSubmitButton.textContent = 'Войти';
});

registerRadio.addEventListener('change', () => {
    registerFields.style.display = 'block';
    authSubmitButton.textContent = 'Зарегистрироваться';
});

// Установка обработчика для кнопки загрузки видео
videoUploadButton.addEventListener('click', () => {
    videoFile.click();
});

// Установка обработчика для выбора нейронной сети
networkSelect.addEventListener('change', () => {
    // ... (Код для отправки запроса к нейронной сети)
});

// Установка обработчика для формы авторизации/регистрации
authForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const isLogin = loginRadio.checked;
    const username = usernameInput.value;
    const password = passwordInput.value;
    const email = emailInput.value;

    if (isLogin) {
        sendLoginRequest(username, password);
    } else {
        sendRegisterRequest(email, username, password);
    }
});

// Функции для отправки запросов к серверу (AJAX)
function sendLoginRequest(username, password) {
    const data = {
        username: username,
        password: password
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Успешная авторизация
            authPopup.style.display = 'none';
            updateBalance(data.balance);
            displayUserProfile(data.user_id, data.balance);
        } else {
            // Ошибка авторизации
            showError(data.message);
            usernameInput.classList.add('error');
            passwordInput.classList.add('error');
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
        showError('Ошибка при отправке запроса.');
    });
}

function sendRegisterRequest(email, username, password) {
    const data = {
        email: email,
        username: username,
        password: password
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Успешная регистрация
            authPopup.style.display = 'none';
            showError(data.message);
            // Переключиться на вкладку "Вход"
            loginRadio.checked = true;
            registerFields.style.display = 'none';
            authSubmitButton.textContent = 'Войти';
            // Очистить поля формы
            usernameInput.value = '';
            passwordInput.value = '';
            emailInput.value = '';
        } else {
            // Ошибка регистрации
            showError(data.message);
            emailInput.classList.add('error');
            usernameInput.classList.add('error');
            passwordInput.classList.add('error');
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
        showError('Ошибка при отправке запроса.');
    });
}

// Функция для отправки запроса на анализ видео (в этой функции потребуется
// отправить видео файл на сервер)
function sendVideoAnalysisRequest(videoData, network, user_id) {
    // Создайте FormData для передачи видео файла
    const formData = new FormData();
    formData.append('video_data', videoData);
    formData.append('network', network);
    formData.append('user_id', user_id);

    fetch('/analyze_video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Успешный анализ видео
            displayResult(data.result);
            updateBalance(data.balance);
        } else {
            // Ошибка анализа видео
            showError(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
        showError('Ошибка при отправке запроса.');
    });
}

// Функция для обновления баланса пользователя
function updateBalance(balance) {
    balanceText.textContent = `Баланс: ${balance} руб.`;
    costText.textContent = `Стоимость анализа: 1 руб.`;
}

// Функция для вывода результата анализа видео
function displayResult(result) {
    resultContainer.style.display = 'block';
    resultContainer.querySelector('.result-text').textContent = result;
}

// Функция для вывода сообщения об ошибке
function showError(message) {
    errorContainer.style.display = 'block';
    errorContainer.querySelector('.error-message').textContent = message;
}

// Функция для отображения профиля пользователя после входа в систему
function displayUserProfile(user_id, balance) {
    // Скрыть кнопку "Вход/Регистрация"
    authButton.style.display = 'none';

    // Отобразить кнопку "Профиль"
    userProfile.style.display = 'inline-block';

    // Установить имя пользователя в кнопку "Профиль"
    userProfileButton.textContent = 'Профиль';

    // Настройка выпадающего меню "Профиль"
    userProfileButton.addEventListener('click', () => {
        userProfileMenu.style.display = 'block';
    });

    // Закрытие выпадающего меню при клике вне его
    document.addEventListener('click', (event) => {
        if (!userProfileMenu.contains(event.target) && !userProfileButton.contains(event.target)) {
            userProfileMenu.style.display = 'none';
        }
    });

    // Добавить элементы в выпадающее меню
    userProfileMenu.innerHTML = `
        <li>Настройки</li>
        <li onclick="logout()">Выход</li>
    `;

    // Функция для выхода из системы
    function logout() {
        // Отправить запрос на сервер для выхода
        fetch('/logout', {
            method: 'POST'
        })
        .then(() => {
            // Скрыть кнопку "Профиль"
            userProfile.style.display = 'none';

            // Отобразить кнопку "Вход/Регистрация"
            authButton.style.display = 'inline-block';

            // Сбросить баланс
            balanceText.textContent = '';
            costText.textContent = '';

            // Скрыть результат анализа
            resultContainer.style.display = 'none';

            // Скрыть ошибку
            errorContainer.style.display = 'none';
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
            showError('Ошибка при выходе из системы.');
        });
    }
}

// Установка обработчика для загрузки видео файла
videoFile.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = (event) => {
            const videoData = event.target.result;
            const selectedNetwork = networkSelect.value;

            // Получение идентификатора пользователя из хранилища
            const user_id = localStorage.getItem('user_id');

            // Если пользователь авторизован, отправляем запрос на анализ видео
            if (user_id) {
                sendVideoAnalysisRequest(videoData, selectedNetwork, user_id);
            } else {
                // Если пользователь не авторизован, показываем ошибку
                showError('Необходимо авторизоваться для анализа видео.');
            }
        };

        reader.readAsDataURL(file);
    }
});

// Обработка ошибок ввода
usernameInput.addEventListener('input', () => {
    if (usernameInput.classList.contains('error')) {
        usernameInput.classList.remove('error');
    }
});

passwordInput.addEventListener('input', () => {
    if (passwordInput.classList.contains('error')) {
        passwordInput.classList.remove('error');
    }
});

emailInput.addEventListener('input', () => {
    if (emailInput.classList.contains('error')) {
        emailInput.classList.remove('error');
    }
});

// Загрузка баланса при загрузке страницы
window.onload = () => {
    const user_id = localStorage.getItem('user_id');
    if (user_id) {
        fetch(`/get_balance/${user_id}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            updateBalance(data.balance);
            displayUserProfile(data.user_id, data.balance);
        })
        .catch(error => {
            console.error('Ошибка при получении баланса:', error);
            showError('Ошибка при получении баланса.');
        });
    }
};
