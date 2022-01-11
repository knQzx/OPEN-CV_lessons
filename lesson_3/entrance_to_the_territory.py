import datetime
import os
import random
import time
import cv2
import telebot
from PIL import Image, ImageChops

vfc = cv2.VideoCapture(2)


def algorithm_similarities_faces(img: str, directory: str):  # algorithm similarities faces
    # check differences if there are any
    image_1 = Image.open(f'{directory}/{img}')
    # chdir to directory "photos"
    os.chdir(f'{directory}')
    # see all photos in the directory "photos"
    sp_nones = []
    sp_not_nones = []
    for images in os.listdir():
        # open image
        image_2 = Image.open(images)
        # check differences if there are any
        result = ImageChops.difference(image_1, image_2)
        # calculates the bounding box of non-zero regions in the image
        if result.getbbox() is None:
            sp_nones.append(None)
        else:
            sp_not_nones.append(True)
    # chdir to start directory
    os.chdir('..')
    # return send this photo if we didn't have similar photo
    if len(sp_not_nones) >= len(sp_nones):
        return 'Send this photo'


# load our haar cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# if cam if open
while vfc.isOpened():
    # read cam
    _, frame = vfc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # settings to face
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=2,
                                          minNeighbors=5,
                                          minSize=(60, 60),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, width, height) in faces:
        # delete files in the folder if there are more than 10 pieces (so as not to clog the memory)
        if 'photos' not in os.getcwd():
            os.chdir('photos')
        if len(os.listdir()) >= 10:
            for el in os.listdir():
                os.remove(el)
        if 'photos' in os.getcwd():
            os.chdir('..')
        # crop image to size face
        crop_img = frame[y:y + height, x:x + width]
        # write image to file
        name_file = f'photo{random.randrange(1111111, 99999999999)}.jpg'
        cv2.imwrite(f"photos/{name_file}", crop_img)
        # run algorithm similarities faces
        if 'photos' in os.getcwd():
            os.chdir('..')
        if name_file in os.listdir('photos'):
            result = algorithm_similarities_faces(name_file, 'photos')
        # if result "Send this photo", send this photo (logically)
        if result == 'Send this photo':
            # initialization bot
            bot = telebot.TeleBot('5007337097:AAGyi8zFBTPQzMY2r6Y_VDWglqte7FYluhM')
            # send photo with text
            if 'photos' in os.getcwd():
                os.chdir('..')
            bot.send_photo(763258583, photo=open(f'photos/{name_file}', 'rb'),
                           caption=f'На территорию вошел человек.\nВремя - {datetime.datetime.now()}')
            time.sleep(2)
    if cv2.waitKey(5) & 0xFF == 27:
        break
