import cv2
import mediapipe as mp


# Инициализация методов библиотеки
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Определение поз
for i in range(1):
    # Счетчик кадров для записи в файл
    frames = 0

    # Чтение каждой видеозаписи и инициализация переменной для обработки
    source_filename = "../Source/" + str(i + 1) + ".mp4"
    cap = cv2.VideoCapture(source_filename)

    # Инициализация названия файла на запись результата
    destination_filename = "../Poses/" + str(i + 1) + ".txt"

    # Детектирование поз при помощи скелетной модели и запись в файл
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and frames < 40:
            ret, frame = cap.read()

            if not ret:
                break

            # Подготовка
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Детектирование
            results = pose.process(image)

            # Обратное преобразование после использования в детектировании
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Запись в файл
            with open(destination_filename, 'a') as file:
                # Запись номера кадра в файл
                file.write(str(frames + 1) + ': ')

                # Запись координат
                for inc, landmark in enumerate(results.pose_landmarks.landmark):
                    # print(f"Landmark {mp_pose.PoseLandmark(i).name}: {landmark.x}, {landmark.y}, {landmark.z}")
                    file.write(str(landmark.x) + ' ')
                    file.write(str(landmark.y) + ' ')

                # Новая строка
                file.write("\n")

            file.close()  # Завершение работы с файлом
            frames = frames + 1  # Инкремент кадра

            """
            print(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Video', image)
            """

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
