import cv2


# cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(r'C:\Users\User\PycharmProjects\pythonProject\haarcascade_frontalface_default.xml')
while True:
    #ret, frame = cap.read()
    frame = cv2.imread('people.png')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 15)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(40) == 27:
        break


# cap.release()
cv2.destroyAllWindows()