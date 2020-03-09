import cv2
import numpy as np

cap = cv2.VideoCapture(0)
num = 1
palm = cv2.CascadeClassifier('cascade.xml')

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.resize(frame, (300, 178), interpolation=cv2.INTER_AREA)
    
    gesture = palm.detectMultiScale(edges, scaleFactor = 1.4, minNeighbors = 6)
    for(x, y, w, h) in gesture:
        gesture = edges[y:y+h, x:x+w]

        gesture = cv2.Canny(gesture, 100, 200)
        cv2.imshow('edges', gesture)
        cv2.imwrite('images/' + str(num) + '.jpg', gesture)
        num += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.release()
cv2.destroyAllWindows()