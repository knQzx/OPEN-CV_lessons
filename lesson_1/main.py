import cv2


cap = cv2.VideoCapture(2)

face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(40) == 27:
        break


# cap.release()
cv2.destroyAllWindows()
