
import numpy as np
import cv2
import sys,getopt
from scipy.spatial import distance
from viewframe import getFrame
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# in case we want to write somthing on image
org = (50, 50) 
color = (255, 0, 0) 
font = cv2.FONT_HERSHEY_SIMPLEX 
thickness = 2
fontScale=1

# def getFrame(sec,VidCapObj):
#     start = 180000 # the 3 minute mark
#     VidCapObj.set(cv2.CAP_PROP_POS_MSEC, start + sec*1000) # gets one frame ,frame at  3 minte mark+ sec
#     hasFrames,image = VidCapObj.read()
#     print("got a frame at",start + sec*1000,"sec mark , status :",hasFrames)
#     return hasFrames, image

if __name__ == "__main__":
    fold="Fold5_part1/52/"
    loc=fold+"10.MOV"
    vidcap = cv2.VideoCapture(loc)
    sec = 25
    frameRate = 1

    success,image = getFrame(sec,vidcap)
    
    shape= image.shape
    print(type(shape))
    count =55 # this is better
    print("ENTERING INFINITE TSUKIYOMI")
    
    while success :
  
        if(image.shape == (1080,1920,3)):
            image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE) 
        # try:
        gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.03, 5)
        print("i am here")
        # we are looking for one face only , reduce any possible error
        if len(faces)==1: 
            for (x,y,w,h) in faces:
                img = cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)# draws a white rectangle
                roi_gray = gray[y:y+h, x:x+w]
                roi_color= img[y:y+h, x:x+w]
                # now get eyes
                eyes = eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) !=2: # lost a data point 
                    # lets try to save all the images where everything went wrong
                    try : 
                        print(" we have some isuues here, found ",len(eyes),"(╯°□°）╯︵ ┻━┻")
                        for (ex,ey,ew,eh) in eyes:# draws rectangle for the ones detected
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
                        cv2.putText(roi_color,str(image.shape), org, font,fontScale, color, thickness, cv2.LINE_AA)
                        cv2.imwrite(fold+"eyes/mult/"+str(sec)+"-"+"error_mult.jpeg",roi_color)
                        print("wrote a file with MULTIPLE faces")
                        sec += frameRate # moving on to next frame 
                        success,image = getFrame(sec,vidcap)
                    except :
                        print("NO eye HERE")
                        cv2.imwrite(fold+"eyes/no/"+str(sec)+"-"+"foundnone.jpeg",eye)
                        print("wrote a file NOEYE")
                        sec += frameRate # moving on to next frame
                        success,image = getFrame(sec,vidcap)


                else : # only 2 eyes dtected TODO we gonna find left and right
                    eyes=[]# left eye , right eye
                    for count,(ex,ey,ew,eh) in enumerate(eyes):
                        eye=roi_gray[ey:ey+eh,ex:ex+ew]
                        cv2.imwrite(fold+"eyes/ok/"+str(sec)+"-"+str(count)+".jpeg",eye)
                        print("wrote a CORRECT ----------------file")
                    
                    sec += frameRate # moving on in case of ok
                    success,image = getFrame(sec,vidcap)
        else :
            # we gonna skip this 
            
            image = cv2.putText(image,str(image.shape), org, font,fontScale, color, thickness, cv2.LINE_AA)
            cv2.imwrite(fold+"eyes/err/"+str(sec)+"-"+"FACEerror.jpeg",image)
            print("wrote a file with FACEERROR")

            sec = sec + frameRate # moving on incase of multiple or none face detection
            success,image = getFrame(sec,vidcap)
        # except :
        #     print("was unable to get image")
        #     # lets retry and run an infinite loop
        #     sec = sec + frameRate # 


    # for i in range(len(eyes)):
    #     cv2.imshow(("eye "+str(i+1)),eyes_roi[i])
    cv2.destroyAllWindows()
    pass