#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt
from scipy.spatial import distance
from mlxtend.image import extract_face_landmarks
from customcvfunc import getFrame,resize2SquareKeepingAspectRation,eye_aspect_ratio
from customcvfunc import mouth_aspect_ratio,circularity,boxpointsfinder,getmeta
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
    global ofile,vidfolder
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
    data_loc_info = traversal(vidfolder)
    locx=vidfolder+"10.MOV"
    for loc,label in data_loc_info:
        print(loc,"-->",label)
        print("processing  file :",loc)
        try :
            vidcap = cv2.VideoCapture(loc)
        except :
            print("!!error loading video, gonna move on (⊙_☉)")
            continue
    
        # now we gotta decide about things like frame rate
        h,m,s = vidlength(loc)
        s = s + m * 60 + h * 60 *60 # now we got length of video in secs
        # we are not gonna take frames from first and last 2 minutes
        s = s - 240 # seems fair        
        rot = getmeta(loc)
        

        for sec in range(s): 
            success,image = getFrame(sec,vidcap,seek=120)# seeked first  2 minutes
            # some 1080p vids get loaded in wrong orientation
            # sometimes specific frames get loaded in wrong orientation
            # i haven't went deep into this , will do later
            # DONE____________
            # for now this works.
            # if(image.shape == (1080,1920,3)):
            #     image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE) 
            if rot == "90":
                print("90")
                image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE) 
            if rot == "270":
                print("270")
                image = cv2.rotate(image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE) 
  
           
            image = cv2.putText(image,str(image.shape), org, font,fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow(str(loc),image)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        vidcap.release()

        print("done with image")
        cv2.destroyAllWindows()




        




pass