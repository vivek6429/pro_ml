#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt,os
from scipy.spatial import distance
from mlxtend.image import extract_face_landmarks
from customcvfunc import getFrame,resize2SquareKeepingAspectRation,eye_aspect_ratio
from customcvfunc import mouth_aspect_ratio,circularity,boxpointsfinder,getmeta,writedata
from traversing_and_length import traversal,vidlength


# Load Haar cascade Models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# points index values of eyes on mlxtend.image.extract_face_landmarks
left_eye = np.array([36, 37, 38, 39, 40, 41])
right_eye = np.array([42, 43, 44, 45, 46, 47])

# in case we want to write somthing on image
org = (50, 50) 
color = (255, 0, 0) 
font = cv2.FONT_HERSHEY_SIMPLEX 
thickness = 2
fontScale=1


def parse(argv):
    global out_folder,vidfolder
    try:
        opts,args = getopt.getopt(argv,"hl:o:f:",["loc=","outputfile=","framerate="])
    except getopt.GetoptError:
        print("getdata.py -l <folder containing vids>  -o <output folder location> -f <frame-rate>")
        sys.exit("exiting")
    
    for opt,arg in opts:
        # print(opt," ",arg)
        if opt == '-h':
            print("getdata.py -l <folder containing vids>  -o <output folder location>")
            sys.exit()
        elif opt in ("-l","--loc"):
            vidfolder=arg  
        elif opt in ("-o","--outputfile"):            
            ofile=arg
        elif opt in ("-f","--framerate"):
            frameRate =1



if __name__ == "__main__":
   
    # setting default vals, easy for testing
    vidfolder="data/"
    frameRate = 1
    out_folder = "extracted_data/"
    # TODO clean this mess later
    if not (os.path.exists(out_folder)):
        os.makedirs(out_folder)  
    if not (os.path.exists(out_folder+"0")):
        os.makedirs(out_folder+"0")
    if not (os.path.exists(out_folder+"5")):
        os.makedirs(out_folder+"5")
    if not (os.path.exists(out_folder+"10")):
        os.makedirs(out_folder+"10")

    data_loc_info = traversal(vidfolder)
    for loc,label in data_loc_info:
        
        print(loc,"-->",label)
        print("processing  file :",loc)
        try :
            vidcap = cv2.VideoCapture(loc)
            print("video loaded to mem")
        except :
            print("!!error loading video, gonna move on (⊙_☉)")
            continue
    
        # now we gotta decide about things like frame rate
        h,m,s = vidlength(loc)
        s = s + m * 60 + h * 60 *60 # now we got length of video in secs
        # we are not gonna take frames from first and last 2 minutes
        s -= 240 
       
        # read rotation info from video metadata   
        rot = getmeta(loc) # this is finaly working
        print("Roation dat of image :",rot)

        for sec in range(s): 
            success,image = getFrame(sec,vidcap,seek=120)# seeked first  2 minutes
            
            # if success:
            # refer haar_landmarkon camera.py
            foundfase=False
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.03, 5)
            
            # looking for faces 
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
                        # THIS FOR LOOP ALSO ACTS AS A FAILSAFE ON TYPE ERROR , when no landmarks are detected
                        # copy=cv2.circle(copy,(points[0],points[1]),2,(255,255,255),-1)
                        print(".",end= "")  
                    print()
                    left_eye_center = np.mean(landmarks[left_eye], axis=0)
                    right_eye_center = np.mean(landmarks[right_eye], axis=0)
                    # print('Coordinates of the Left Eye: ', left_eye_center)
                    # print('Coordinates of the Right Eye: ', right_eye_center)
                    print("L_EYE at :",left_eye_center,"  R_EYE at :",right_eye_center)
                    
                    # box around eyes
                    succes,l_topl,l_botr,r_topl,r_botr = boxpointsfinder(landmarks,scalefactor=0.5)
                    bkp=np.copy(copy)
                    cv2.rectangle(copy, l_topl, l_botr, (0, 255, 0, 255), 2)
                    cv2.rectangle(copy, r_topl, r_botr, (0, 255, 0, 255), 2)
                    i_left = bkp[l_topl[1]:l_botr[1],l_topl[0]:l_botr[0]]                
                    i_right = bkp[r_topl[1]:r_botr[1],r_topl[0]:r_botr[0]]
                    # cv2.imshow("LEYE",i_left)
                    # cv2.imshow("leyesize",cv2.resize(i_left,(32,32)))
                    # cv2.imshow("REYE",i_right)
                    # cv2.imshow("eyes",cv2.hconcat([cv2.resize(i_left,(32,32)),cv2.resize(i_right,(32,32))]))
                    writedata(i_left,i_right,loc,label,sec+120)
                    # sys.exit(0)
                except TypeError:
                    print("found a none type")
                    cv2.imshow("DID NOT DETECT FACE",cv2.resize(image,(244,244)))
                    k = cv2.waitKey(30) & 0xff
                    if k == 27:
                        break
                    continue


                cv2.imshow(str(loc),cv2.resize(image,(244,244)))
                cv2.imshow("FACE HARCASCADE",roi_color)
                cv2.imshow("MLXTEND.landmarks",copy)

                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

            else :
                print("found face :",foundfase)
                continue
        
        vidcap.release()

    cv2.destroyAllWindows()
    pass




        

   