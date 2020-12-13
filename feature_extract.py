#!/usr/bin/python3
# similar to image_data_process
# gonna do haaar cascade

from image_data_process import  resize2SquareKeepingAspectRation
import numpy as np
import cv2
import sys,getopt
import imageio
import matplotlib.pyplot as plt
from mlxtend.image import extract_face_landmarks
from scipy.spatial import distance
import math

# some global vals that we can use for now.........
fileloc="c.jpeg"
sec=0
ofile=''
# the Haar-cascade classifiers
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
# rtfm
#
# Instead of trying to figure out where the .xml files are
# and hard coding the values, I used a property given by cv2.
# from stack overflow
# https://stackoverflow.com/questions/30508922/error-215-empty-in-function-detectmultiscale
# second best answer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# image processing function defs
# gets required no of image rotation
# lets use this once for a data set
def rots(img):
    rots = 0
    while True:
       
        cv2.imshow("Decide  orientation ",img)
        k=cv2.waitKey(1) & 0xFF
        
        if k==27:
            cv2.destroyAllWindows()
            rots = int( input("enter number of 90 degree cw rots :") or "0")
            break

    return rots

##################################

if __name__ == "__main__":

    image=cv2.imread(fileloc,1)
    # image=cv2.resize(image,(224,224))
    # image=resize2SquareKeepingAspectRation(image,224,cv2.INTER_AREA)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('image',gray)
    cv2.waitKey(0)
    faces = face_cascade.detectMultiScale(gray, 1.03, 5)
    print(faces)
    xx=255
    yy=0
    if len(faces)==1:# we are looking for one face only , reduce any possible error
        for (x,y,w,h) in faces:
            img = cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            print("number of eyes==",len(eyes))
            if len(eyes) != 2:
                print(" we have some isuues here, found ",len(eyes),"(╯°□°）╯︵ ┻━┻")
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,xx,yy),2)
                    cv2.imshow('image',img)
                    cv2.waitKey(0)
                    break ;
            else :
                print("heloooo")
                eyes_roi=[]
                for (ex,ey,ew,eh) in eyes:
                    eye=roi_gray[ey:ey+eh,ex:ex+ew]
                    eyes_roi.append(eye)


    for i in range(len(eyes)):
        cv2.imshow(("eye "+str(i+1)),eyes_roi[i])
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass