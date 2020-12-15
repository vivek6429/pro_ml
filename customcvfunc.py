# this file contains all of our functions
# image processing function defs


# we can do a lot of cool stuff here but for the time being lets keep it simple
# i will add comments for each functions in this file as i use them from now on
import numpy as np
import cv2
from scipy.spatial import distance
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



#A function from stack over flow that keeps aspect ratio when resizing to a square
# got it from stack over flow
# havent dived into it
# went through some ...
#https://stackoverflow.com/questions/47697622/cnn-image-resizing-vs-padding-keeping-aspect-ratio-or-not
# therefore not using this for time being........
def resize2SquareKeepingAspectRation(img, size, interpolation):
  h, w = img.shape[:2]
  c = None if len(img.shape) < 3 else img.shape[2]
  if h == w: return cv2.resize(img, (size, size), interpolation)
  if h > w: dif = h
  else:     dif = w
  x_pos = int((dif - w)/2.)
  y_pos = int((dif - h)/2.)
  if c is None:
    mask = np.zeros((dif, dif), dtype=img.dtype)
    mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
  else:
    mask = np.zeros((dif, dif, c), dtype=img.dtype)
    mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
  return cv2.resize(mask, (size, size), interpolation)
# image_keep_aspect=resize2SquareKeepingAspectRation(image,224,cv2.INTER_AREA)



# important NOTE  here a 3sec skip is already there 
# this will affect  other files
# TODO REPAIR THIS ADD AN OPTIONAL START PARAMETER WITH DEFAULT 3 MIN
# IF REQUIRED ADD MIN ALSO 
# NOTE GET BACK TO THIS LATER
def getFrame(sec,VidCapObj):
    start = 180000 # the 3 minute mark
    VidCapObj.set(cv2.CAP_PROP_POS_MSEC, start + sec*1000) # gets one frame ,frame at  3 minte mark+ sec
    hasFrames,image = VidCapObj.read()
    print("getFrame.log: got a frame at",start + sec*1000,"sec mark , status :",hasFrames)
    return hasFrames, image



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




if __name__ == "__main__":


    pass