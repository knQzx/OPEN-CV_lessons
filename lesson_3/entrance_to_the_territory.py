import datetime
import os
import random
import cv2
import telebot

vfc = cv2.VideoCapture(2)

class Entrance_to_the_territory:
    def __init__(self):
        pass

    def algorithm_similarities_faces(self, img: str, directory: str):  # algorithm similarities faces
        # check differences if there are any
        hash1 = self.calculate_image_hash(f'{directory}/{img}')
        # chdir to directory "photos"
        os.chdir(f'{directory}')
        # see all photos in the directory "photos"
        for images in os.listdir():
            # open image
            hash2 = self.calculate_image_hash(images)
            # check differences if there are any
            result = int(self.compare_hash(hash1, hash2))
            print(result)
            # calculates the bounding box of non-zero regions in the image
            if result >= 22:
                # chdir to start directory
                os.chdir('..')
                return 'Send this photo'


    def calculate_image_hash(self, FileName: str):  # calculate image hash
        image = cv2.imread(FileName)  # Let's read the picture
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Reduce the picture
        gray_image = cv2.cvtColor(resized,
                                  cv2.COLOR_BGR2GRAY)  # We will translate it into black and white format
        avg = gray_image.mean()  # Average pixel value
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Binarization by threshold

        # Calculate the hash
        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash


    def compare_hash(self, hash1, hash2):  # compare hash
        l = len(hash1)
        i = 0
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        return count


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
        if len(os.listdir()) >= 30:
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
            result = Entrance_to_the_territory().algorithm_similarities_faces(name_file, 'photos')
        # if result "Send this photo", send this photo (logically)
        if result == 'Send this photo':
            # initialization bot
            bot = telebot.TeleBot('5007337097:AAGyi8zFBTPQzMY2r6Y_VDWglqte7FYluhM')
            # send photo with text
            if 'photos' in os.getcwd():
                os.chdir('..')
            bot.send_photo(763258583, photo=open(f'photos/{name_file}', 'rb'),
                           caption=f'На территорию вошел человек.\nВремя - {datetime.datetime.now()}')
    if cv2.waitKey(5) & 0xFF == 27:
        break
