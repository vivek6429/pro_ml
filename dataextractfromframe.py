#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt
import imageio
import matplotlib.pyplot as plt
from mlxtend.image import extract_face_landmarks

fileloc="aaaaaaaa.jpeg"
sec=0
ofile=''

def parse(argv):
    global sec,ofile,fileloc
    try:
        opts,args = getopt.getopt(argv,"hl:o:",["loc=","outputfile="])
    except getopt.GetoptError:
        print("viewframe.py -l <file location>  -o <output file name>")
        sys.exit("exiting")
    for opt,arg in opts:
        # print(opt," ",arg)
        if opt == '-h':
            print("viewframe.py -l <file location>  -o <output file location(optional)")
            sys.exit()
        elif opt in ("-l","--loc"):
            fileloc=arg  
        elif opt in ("-s","--time"):
            sec=int(arg)
        elif opt in ("-o","--outputfile"):            
            ofile=arg



parse(sys.argv[1:])
print("\n\n")
print("o:",ofile)
print("sec:",sec)
print("fileloc:",fileloc)
# now we have the params 







###############################################f
# functions
# for calculating those required features
def eye_aspect_ratio(eye,show=True):
    A = distance.euclidean(eye[1],eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A+B)/(2.0 * C)
    if show == True :
        print("EAR :",ear)
    return ear # WE GOT THE EAR VALUE NOW

def mouth_aspect_ratio(mouth,show=True):
    A = distance.euclidean(mouth[14], mouth[18])
    C = distance.euclidean(mouth[12], mouth[16])
    if show == True:
        print("mar :",(A/C))
    return A/C  # we got mar value now

def mouth_over_eye(eye,show=True):
    ear = eye_aspect_ratio(eye,False)
    mar = mouth_aspect_ratio(eye,False)
    mouth_eye = mar/ear
    if show == True:
        print("mouth_eye :",mouth_eye)
    return mouth_eye

def circularity(eye): # PUC 
    # puc = (4 pi area)/(perimeter sq)
    
    A = distance.euclidean(eye[1], eye[4])
    radius  = A/2.0
    Area = math.pi * (radius ** 2)
    p = 0 # perimeter
    p += distance.euclidean(eye[0], eye[1])
    p += distance.euclidean(eye[1], eye[2])
    p += distance.euclidean(eye[2], eye[3])
    p += distance.euclidean(eye[3], eye[4])
    p += distance.euclidean(eye[4], eye[5])
    p += distance.euclidean(eye[5], eye[0])
    puc = (4 * math.pi * Area) /(p**2)
    print("puc :",puc)
    
    return (puc)



###########################################################end 


image=cv2.imread(fileloc,1)
print("loaded file :",fileloc)
# print(image)
print("PRESS Q to quit")

print(image[0])

cv2.imshow("Frame",image)
cv2.waitKey(0)
landmarks = extract_face_landmarks(image)

print(landmarks[0])
print(type(landmarks[0]))
x=landmarks[0]
print(x[0])
print(x[1])

for points in landmarks:
    print(points[0],",",points[1])
    image[points[1],points[0],0]=255
    image[points[1],points[0],1]=255
    image[points[1],points[0],2]=255
    image=cv2.circle(image,(points[0],points[1]),5,(255,255,255),-1)
    

cv2.imshow("Frame",image)
# cv2.waitKey(0)

K = cv2.waitKey(0) & 0xFF  # use the mask in 64 bit machine if error
if K == 27:
    cv2.destroyAllWindows()



cv2.destroyAllWindows()