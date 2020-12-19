# this file contains all of our functions
# image processing function defs


# we can do a lot of cool stuff here but for the time being lets keep it simple
# i will add comments for each functions in this file as i use them from now on
import numpy as np
import cv2
from scipy.spatial import distance
import subprocess
import os

left_eye = np.array([36, 37, 38, 39, 40, 41])
right_eye = np.array([42, 43, 44, 45, 46, 47])

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
def getFrame(sec,VidCapObj,seek=0):
    # the 3 minute mark
    # print("ok")
    VidCapObj.set(cv2.CAP_PROP_POS_MSEC, seek * 1000 + sec*1000) # gets one frame ,frame at  3 minte mark+ sec
    # print("here")
    hasFrames,image = VidCapObj.read()
    print("getFrame.log: got a frame at",seek * 1000+ sec*1000,"sec mark , status :",hasFrames)
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


# this function returns co-ordinates for drawing boxes for eyes
# inputs landmarks and % additional scaling
# returns 4 tuples (x,y) co-ordinates
# l-eye  : top left and bottom right
# r-eye  : top left and bottom right
def boxpointsfinder(landmarks,scalefactor=0.2):
    # we can later clean this ugly thing later
    # feel free to ping me for now 
    # remember this can also be a complete blunder

    def heightadjust(pts1,pts2):
        d=(distance.euclidean(pts1[0],pts1[1])+distance.euclidean(pts2[0],pts2[1])) /2.0
        d += scalefactor * d
        return d
    status = False
    try :
        h_l=heightadjust((landmarks[37],landmarks[41]),(landmarks[38],landmarks[40]))
        w_l=scalefactor * distance.euclidean(landmarks[36],landmarks[39]) # why ? cause we already have points on left and right center,
        #  only need to find the distance to add to what we have 
        h_l /=2.0 # why ? distance to move from where we are standing
        w_l /= 2.0
        # h_l = h_l //2
        # w_l =w_l // 2

        # remember remember the fifth of november, the gun powder treason and plot ....

        # remember
        # in opencv  
        # +x ---> direction
        # 
        # |
        # | +y direction
        # V

        l_topl=(int(landmarks[36][0]-w_l),int(landmarks[36][1]-h_l))   # u moved w_l distance left and h_l distance up from 36 (x,y)
        l_botr=(int(landmarks[39][0]+w_l),int(landmarks[39][1]+h_l))   # u moved w_l distance right and h_l distance down from 39 (x,y)

        # right eye 
        h_r=heightadjust((landmarks[43],landmarks[47]),(landmarks[44],landmarks[46]))
        w_r=scalefactor * distance.euclidean(landmarks[42],landmarks[45]) 
        h_r /=2.0
        w_r /=2.0
        r_topl=(int(landmarks[42][0]-w_l),int(landmarks[42][1]-h_l)) 
        r_botr=(int(landmarks[45][0]+w_l),int(landmarks[45][1]+h_l))
        succes =True
        
    except :
        succes =False
        print("just keeping it here")


    return succes,l_topl,l_botr,r_topl,r_botr


def getmeta(filename,exe="exiftool",all=False):
    # we might want to adjust it as per the os
    # can do a general one later
    process = subprocess.Popen([exe,filename],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    metadata={}
    
    try :
        for output in process.stdout:
            # print(output.strip())
            # info={}
            line = output.strip().split(":")
            metadata[line[0].strip()]=line[1].strip()
           
    except :
        print("NO METADATA")


    # just in case 
    try :    
        res = metadata['Rotation']
    except :
        res = 0

    if all == True:
        return metadata
    else :
        print("Rotation from meta:",res)
        return res

# needs work on setting path
def writedata(l_eye,r_eye,loc,label,append):
    img=cv2.hconcat([cv2.resize(l_eye,(32,32)),cv2.resize(r_eye,(32,32))])
    # writing to , extracted_data --> the label --> personid_sec.jpeg
    fname="extracted_data/"+label+"/"+str(os.path.basename(os.path.dirname(loc)))+"_"+str(append)+".jpeg"

    try:
        print(fname)
        cv2.imwrite(fname,img)
        print("wrote",fname)
    except:
        print("write FAILED")
        return None

def imagesplitter(img,x=0,y=0,h=32,w=32):
    img=cv2.resize(img,(64,32))
    crop_imgl = img[y:y+h, x:x+w] # 0 to 32 rows , 0 to 32 cols
    crop_imgr = img[y:y+h, x+w:x+w+w] # 0 to 32 rows , 32 to 64 cols
    return crop_imgl,crop_imgr




if __name__ == "__main__":

    

    pass