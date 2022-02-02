from keras.models import load_model
from time import sleep
from cv2 import imshow
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

face_classification = cv2.CascadeClassifier(r'D:\Emotion Detector CNN\haarcascade_frontalface_default.xml')
classifier =load_model(r'D:\Emotion Detector CNN\model.h5')

emotion_types = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

camera = cv2.VideoCapture(0)



while True:
    _, frame = camera.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classification.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        region_gray = gray[y:y+h,x:x+w]
        region_gray = cv2.resize(region_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([region_gray])!=0:
            region_of_interest = region_gray.astype('float')/255.0
            region_of_interest = img_to_array(region_of_interest)
            region_of_interest = np.expand_dims(region_of_interest,axis=0)

            prediction = classifier.predict(region_of_interest)[0]
            label=emotion_types[prediction.argmax()]
            label_position = (x,y-10)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Face Detected',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('h'):
        break

camera.release()
cv2.destroyAllWindows()