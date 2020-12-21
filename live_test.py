#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt,os
from scipy.spatial import distance
from mlxtend.image import extract_face_landmarks
from customcvfunc import getFrame,resize2SquareKeepingAspectRation,eye_aspect_ratio
from customcvfunc import mouth_aspect_ratio,circularity,boxpointsfinder
from tensorflow import keras
model = keras.models.load_model('model')



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
        p0=p5=p10=max_p = 0 # i have no idea now why i used these var names
        # these are probablity for each labes
        ps=[] # list of probablities
        maxpos = -1
        # TODO will clean this later
  
        succes,image = vidcap.read()
        if(image.shape == (1080,1920,3)):
            image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE) 
        # image = cv2.resize(image,(244,244))
        foundfase=False
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.03, 5)
        area=0
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            if area <= h*w:
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
                    # print(".",end=" ")    
                    pass    
                    # THIS FOR LOOP ALSO ACTS AS A FAILSAFE ON TYPE ERROR , when no landmarks are detected
                
                # lets start cropping eye


                succes,l_topl,l_botr,r_topl,r_botr = boxpointsfinder(landmarks,scalefactor=0.5)

                bkp=np.copy(copy)
                cv2.rectangle(copy, l_topl, l_botr, (0, 255, 0, 255), 2)
                cv2.rectangle(copy, r_topl, r_botr, (0, 255, 0, 255), 2)
                i_left = bkp[l_topl[1]:l_botr[1],l_topl[0]:l_botr[0]]                
                i_right = bkp[r_topl[1]:r_botr[1],r_topl[0]:r_botr[0]]
                try:
                    img=cv2.hconcat([cv2.resize(i_left,(32,32)),cv2.resize(i_right,(32,32))]) 
                    img_array =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    cv2.imshow("eyes l +r",img_array)
                    # sorry we need to do this neatly
                    # i am sleepy
                    T=[]
                    T.append(img_array)
                    T=np.array(T).reshape(-1,32,64)
                    T = T /255 # normalizing
                    T = T.reshape(T.shape[0], 32, 64, 1)
                    p=model.predict(T)
                    p0=p[0][0] 
                    p5=p[0][1] 
                    p10=p[0][2] 
                    ps=[p0,p5,p10]
                    maxpos = ps.index(max(ps)) 
                    print("sum = ",p0+p5 +p10)
                    print("Probablity label 0:",p0)
                    print("Probablity label 5:",p5)
                    print("Probablity label 10:",p10)

                except Exception as e:              
                    print(e)
                    print("concat failed")
            except Exception as e:
                print(e)
                print("found a none type")
                cv2.imshow("DID NOT DETECT FACE",cv2.resize(image,(244,244)))
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break
                continue

            image = cv2.putText(image,"p0 :"+str(p0), org, font,  
                   fontScale, color, thickness, cv2.LINE_AA)
            image = cv2.putText(image,"p5 :"+str(p5), (50,100), font,  
                   fontScale, color, thickness, cv2.LINE_AA)
            image = cv2.putText(image,"p10 :"+str(p10), (50,150), font,  
                   fontScale, color, thickness, cv2.LINE_AA)
             
            
            if maxpos==0:
                image = cv2.putText(image,"Alert", (300,300), font,  
                   fontScale,  (255,0,0), thickness, cv2.LINE_AA)
            if maxpos==1:
                image = cv2.putText(image,"Low vigilent", (300,300), font,  
                   fontScale,  (0,255,255), thickness, cv2.LINE_AA)
            if maxpos==2:
                image = cv2.putText(image,"Drowsy", (300,300), font,  
                   fontScale,  (0,0,255),thickness, cv2.LINE_AA)
            if maxpos==-1:
                image = cv2.putText(image,"No prediction", (300,300), font,  
                   fontScale,  (255,255,255),thickness, cv2.LINE_AA)


            cv2.imshow("STREAM",image)
            # cv2.imshow("FACE HARCASCADE",roi_color)
            cv2.imshow("MLXTEND.landmarks",copy)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        else :
            print("found face :",foundfase)
            continue

    cv2.destroyAllWindows()
    pass