import numpy as np
import cv2 as cv
import pickle
import os

from sklearn.preprocessing import StandardScaler


def preprocessing(file_name: str):
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        # Читаем содержимое файла
        imgray = cv.imread(file_name, cv.IMREAD_GRAYSCALE)
        imgray = cv.resize(imgray, (512, 512))
        dft_img = np.fft.fft2(imgray).real
        if np.max(dft_img.real) != 0:
            imgray = dft_img / np.max(dft_img.real)
        center = np.array(imgray.shape) // 2
        y, x = np.indices(imgray.shape)
        r = np.abs(x - center[0])
        r = r.astype(np.int32)
        tbin = np.bincount(r.ravel(), imgray.ravel())
        nr = np.bincount(r.ravel())
        radialprofile = tbin / nr
        nan_mask = np.isnan(radialprofile)
        radialprofile = radialprofile[~nan_mask]
        return radialprofile


def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Файл {file_path} успешно удален.')
        else:
            print(f'Файл {file_path} не найден.')
    except Exception as e:
        print(f'Ошибка при удалении файла {file_path}: {e}')


def predict(file: str):

    with open('static/scripts/img_detection/model.pkl', 'rb') as file_model:
        loaded_model = pickle.load(file_model)
        scaler = StandardScaler()
        X_train = np.load("static/scripts/img_detection/train.npy", allow_pickle=True)
        X_train = scaler.fit_transform(X_train)
        X_test = np.load("static/scripts/img_detection/test.npy", allow_pickle=True)
        x_test = preprocessing(file)
        x_test = np.array(x_test).reshape((1, len(x_test)))
        X_test[X_test.shape[0] - 1] = x_test
        X_test = scaler.transform(X_test)
        y_pred = loaded_model.predict(X_test)
        delete_file(file)
        return y_pred[len(y_pred)-1:]
