import numpy as np
import cv2 as cv
import pickle
import os


def preprocessing(file_name: str):
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        # Читаем содержимое файла
        imgray = cv.imread(file_name, cv.IMREAD_GRAYSCALE)
        imgray = cv.resize(imgray, (512, 512))
        dft_img = np.fft.fft2(imgray).real
        # print(dft_img.shape)
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
    X_test = preprocessing(file)
    y_pred = loaded_model.predict(np.array(X_test).reshape((1, len(X_test))))
    delete_file(file)
    return y_pred
