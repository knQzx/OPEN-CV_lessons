import datetime
import os

import cv2


class Write_Faces:
    def __init__(self, class_photo_name: str):  # --> имя для изображения всего класса (cam.png)
        self.class_photo_name = class_photo_name

    def make_class_image(self):
        # Включаем первую камеру
        cap = cv2.VideoCapture(2)
        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()
        # Делаем снимок
        self.ret, self.frame = cap.read()
        # Записываем в файл
        cv2.imwrite(self.class_photo_name, self.frame)
        # Отключаем камеру
        cap.release()

    def pupils_faces(self):
        # Загрузка изображения
        image = cv2.imread(self.class_photo_name)
        # преобразуем изображение к оттенкам серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # инициализировать распознаватель лиц (каскад Хаара по умолчанию)
        face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        # обнаружение всех лиц на изображении
        faces = face_cascade.detectMultiScale(gray, 1.2, 2)
        print(f"{len(faces)} лиц обнаружено на изображении.")
        # для всех обнаруженных лиц рисуем синий квадрат
        time_write = datetime.datetime.now()
        if 'faces' not in os.listdir():
            os.mkdir('faces')
        for x, y, width, height in faces:
            cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
            crop_img = self.frame[y:y + height, x:x + width]
            # изображение в папку
            name_file = f'{time_write}_kid.png'
            cv2.imwrite(f"faces/{name_file}", crop_img)


# name of file
faces = Write_Faces('cam.png')
faces.make_class_image()
faces.pupils_faces()