import numpy as np
import cv2
import sys,getopt

fileloc="/home/v/Projects/pro_ml/Fold5_part2/60"+"/10.mov"
sec = 120

def parse(argv):
    try:
        opts,args = getopt.getopt(argv,"hl:s:",["loc=","sec="])
    except getopt.GetoptError:
        print("viewframe.py -l <file location> -s <time in seconds>")
        sys.exit("exiting")
    for opt,arg in opts:
        if opt == '-h':
            print("viewframe.py -l <file location> -s <time in seconds>")
            sys.exit()
        elif opt in ("-l","--loc"):
            fileloc=arg
            
            print("file loc =",fileloc,type(arg))
        elif opt in ("-s","--time"):
            sec=int(arg)


def getFrame(sec,VidCapObj):
    start = 180000 # the 3 minute mark
    VidCapObj.set(cv2.CAP_PROP_POS_MSEC, start + sec*1000) # gets one frame ,frame at  3 minte mark+ sec
    hasFrames,image = vidcap.read()
    print("got a frame at",start + sec*1000,"sec mark , status :",hasFrames)
    return hasFrames, image


parse(sys.argv[1:])
vidcap=cv2.VideoCapture(fileloc)
print("loaded file :",fileloc)

success,image = getFrame(sec,vidcap)
print(success)
print(image)

if success == True:
    cv2.imshow("Frame",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else :
    print("start debugging LOL")
    print(type(image))
    print("\n\n",image)