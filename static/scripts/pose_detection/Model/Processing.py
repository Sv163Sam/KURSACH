import os
import cv2
import numpy as np
import mediapipe as mp
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

N = 90
T = 10
S = 2


def detect_pose():
    frames = 0
    source_filename = "static/scripts/pose_detection/Source/91.mp4"
    destination_filename = "static/scripts/pose_detection/Poses/90.txt"

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(source_filename)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and frames < 40:
            ret, frame = cap.read()

            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            with open(destination_filename, 'a') as file:
                file.write(str(frames + 1) + ': ')
                for inc, landmark in enumerate(results.pose_landmarks.landmark):
                    file.write(str(landmark.x) + ' ')
                    file.write(str(landmark.y) + ' ')

                file.write("\n")

            file.close()
            frames = frames + 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def processing():
    numbers = []
    result = []

    labels = np.zeros(1472, dtype=int)  # Вектор меток для обучения
    class_names = ["Бег(боковая проекция)", "Присяд", "Выпады", "Наклон туловища", "Ходьба(фронтальная проекция)",
                   "Ходьба(боковая проекция)", "Вертикальный прыжок"]  # Названия меток для вывода
    # Индексы меток
    Run_side = 0  # Бег(боковая проекция)
    Sitdown = 1  # Присяд
    Lunges = 2  # Выпады
    Torso_tilt = 3  # Наклон туловища
    Walk_front = 4  # Ходьба(фронтальная проекция)
    Walk_side = 5  # Ходьба(боковая проекция)
    Jump = 6  # Вертикальный прыжок

    def read_files():
        for file_index in range(0, N):
            filename = f'static/scripts/pose_detection/Poses/{file_index + 1}.txt'
            with open(filename, 'r') as file:
                data = file.readlines()
            for line in data:
                numbers.append([float(num) for num in line.split()[1:]])

    def create_res():
        for i in range(0, len(numbers) + 1 - T, S):
            if (i // 40) * 40 + 30 < i < (i // 40 + 1) * 40 + 40:
                continue
            window_matrix = np.array(numbers[i:i + T])
            result.append(window_matrix.flatten())

    def init_labels():
        labels[0:160] = Run_side
        labels[160:320] = Sitdown
        labels[320:480] = Lunges
        labels[480:640] = Torso_tilt
        labels[640:960] = Walk_front
        labels[960:1120] = Walk_side
        labels[1120:1424] = Jump

    def not_mixed_samples_train():
        user_vid = result[len(result) - 16:]
        res = result[:len(result) - 16]

        n_entities = len(res) // 16
        scaler = StandardScaler()
        scaler.fit(result)

        grouped_result = [result[i * 16:(i + 1) * 16] for i in range(n_entities)]
        grouped_labels = [labels[i * 16:(i + 1) * 16] for i in range(n_entities)]

        train_indices, test_indices = train_test_split(list(range(n_entities)), test_size=0.01, random_state=42)

        x_train = [grouped_result[i] for i in train_indices]
        x_test = [grouped_result[i] for i in test_indices]
        y_train = [grouped_labels[i] for i in train_indices]
        y_test = [grouped_labels[i] for i in test_indices]

        x_train = [item for sublist in x_train for item in sublist]
        x_test = [item for sublist in x_test for item in sublist]
        y_train = [item for sublist in y_train for item in sublist]
        y_test = [item for sublist in y_test for item in sublist]

        x_train = scaler.transform(x_train)
        x_test = user_vid
        x_test = scaler.transform(x_test)

        def rf():
            rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            rf_model.fit(x_train, y_train)
            return rf_model

        model = rf()

        y_pred = model.predict(x_test)

        return class_names[y_pred[0]]

    read_files()
    create_res()
    init_labels()
    pred = not_mixed_samples_train()

    return pred


def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Файл {file_path} успешно удален.')
        else:
            print(f'Файл {file_path} не найден.')
    except Exception as e:
        print(f'Ошибка при удалении файла {file_path}: {e}')


def neuro_processing():
    detect_pose()
    pred = processing()

    delete_file('static/scripts/pose_detection/Source/91.mp4')
    delete_file('static/scripts/pose_detection/Poses/90.txt')

    return pred
