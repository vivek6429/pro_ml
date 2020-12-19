#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt
from scipy.spatial import distance
from mlxtend.image import extract_face_landmarks
from customcvfunc import getFrame,resize2SquareKeepingAspectRation,eye_aspect_ratio
from customcvfunc import mouth_aspect_ratio,circularity,boxpointsfinder



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
left_eye = np.array([36, 37, 38, 39, 40, 41])
right_eye = np.array([42, 43, 44, 45, 46, 47])

# in case we want to write somthing on image
org = (50, 50) 
color = (255, 0, 0) 
font = cv2.FONT_HERSHEY_SIMPLEX 
thickness = 2
fontScale=1


if __name__ == "__main__":
   
    fold="Fold5_part1/52/"
    loc=fold+"10.MOV"
    vidcap = cv2.VideoCapture(0)
    
    print("ENTERING INFINITE TSUKIYOMI")
    
    while True :

  
        succes,image = vidcap.read()
        if(image.shape == (1080,1920,3)):
            image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE) 
        # image = cv2.resize(image,(244,244))
        foundfase=False
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.03, 5)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            foundfase=True
        
        if foundfase:
            copy=np.copy(roi_color)
            landmarks = extract_face_landmarks(copy)

            try :

                for points in landmarks:
                    # copy=cv2.circle(copy,(points[0],points[1]),2,(255,255,255),-1)
                    # print(i," ",points)
                    print(".")        
                    # THIS FOR LOOP ALSO ACTS AS A FAILSAFE ON TYPE ERROR , when no landmarks are detected
                
                # lets start cropping eye
  

                left_eye_center = np.mean(landmarks[left_eye], axis=0)
                right_eye_center = np.mean(landmarks[right_eye], axis=0)
                print('Coordinates of the Left Eye: ', left_eye_center)
                print('Coordinates of the Right Eye: ', right_eye_center)


                # left_eye_top_left=tuple(landmarks[36])
                # left_eye_bottom_right=tuple(landmarks[39])
                # right_eye_top_left=tuple(landmarks[42])
                # right_eye_bottom_right=tuple(landmarks[45])

                # left_eye_top_left=(landmarks[36][0]-5,landmarks[38][1]-99)
                # left_eye_bottom_right=(landmarks[39][0]+14,landmarks[41][1]+14)
                # right_eye_top_left=(landmarks[42][0]-14,landmarks[44][1]-14)
                # right_eye_bottom_right=(landmarks[45][0]+14,landmarks[47][1]+14)
                # cv2.rectangle(copy, left_eye_top_left, left_eye_bottom_right, (0, 255, 0, 255), 2)
                # cv2.rectangle(copy, right_eye_top_left, right_eye_bottom_right, (0, 255, 0, 255), 2)
                
                succes,l_topl,l_botr,r_topl,r_botr = boxpointsfinder(landmarks,scalefactor=0.5)
                print("i am here")
                print(l_topl)
                # print(lef)

                bkp=np.copy(copy)
                cv2.rectangle(copy, l_topl, l_botr, (0, 255, 0, 255), 2)
                cv2.rectangle(copy, r_topl, r_botr, (0, 255, 0, 255), 2)
                i_left = bkp[l_topl[1]:l_botr[1],l_topl[0]:l_botr[0]]                
                i_right = bkp[r_topl[1]:r_botr[1],r_topl[0]:r_botr[0]]
                cv2.imshow("LEYE",i_left)
                cv2.imshow("leyesize",cv2.resize(i_left,(32,32)))
                cv2.imshow("REYE",i_right)
            except TypeError:
                print("found a none type")
                cv2.imshow("DID NOT DETECT FACE",image)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break
                continue

        
            cv2.imshow("STREAM",image)
            cv2.imshow("FACE HARCASCADE",roi_color)
            cv2.imshow("MLXTEND.landmarks",copy)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        else :
            print("found face :",foundfase)
            continue

    cv2.destroyAllWindows()
    pass