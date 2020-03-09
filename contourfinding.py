import cv2 
import numpy as np 
import os

num = 1
for filename in os.listdir("."):
    if filename.startswith("palm"):
        

        if not os.path.exists("Palms/"):
            os.mkdir("Palms")

        img=cv2.imread(filename)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 30, 200) 
        cv2.imwrite("Palms/palm"+str(num)+".jpg", edged)

    elif filename.startswith("fist"):
        
        if not os.path.exists("Fists/"):
            os.mkdir("Fists")

        img=cv2.imread(filename)
        edged = cv2.Canny(img, 30, 200) 
        cv2.imwrite("Fists/fist"+str(num)+".jpg", edged)
    else:
        print("Picture " + str(num) + " does not exist")
    num = num+1

cv2.waitKey(0)
cv2.destroyAllWindows()