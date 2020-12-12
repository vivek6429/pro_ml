#!/usr/bin/python3
import numpy as np
import cv2
import sys,getopt

fileloc="/home/v/Projects/pro_ml/Fold5_part2/60"+"/10.mov"
sec = 120
ofile=''

def parse(argv):
    global sec,ofile,fileloc
    try:
        opts,args = getopt.getopt(argv,"hl:s:o:",["loc=","sec=","outputfile="])
    except getopt.GetoptError:
        print("viewframe.py -l <file location> -s <time in seconds> -o <output file name>")
        sys.exit("exiting")
    for opt,arg in opts:
        # print(opt," ",arg)
        if opt == '-h':
            print("viewframe.py -l <file location> -s <time in seconds> -o <output file location(optional)")
            sys.exit()
        elif opt in ("-l","--loc"):
            fileloc=arg  
        elif opt in ("-s","--time"):
            sec=int(arg)
        elif opt in ("-o","--outputfile"):            
            ofile=arg





def getFrame(sec,VidCapObj):
    start = 180000 # the 3 minute mark
    VidCapObj.set(cv2.CAP_PROP_POS_MSEC, start + sec*1000) # gets one frame ,frame at  3 minte mark+ sec
    hasFrames,image = vidcap.read()
    print("got a frame at",start + sec*1000,"sec mark , status :",hasFrames)
    return hasFrames, image


parse(sys.argv[1:])
print("\n\n")
print("o:",ofile)
print("sec:",sec)
print("fileloc:",fileloc)


vidcap=cv2.VideoCapture(fileloc)
print("loaded file :",fileloc)

success,image = getFrame(sec,vidcap)
print(success)
print(image.shape)
print("PRESS Q to quit")


if success == True:
    cv2.imshow("Frame",image)
    cv2.waitKey(0)
    if ofile != '':
        cv2.imwrite(ofile,image)
        print("file written")
    cv2.destroyAllWindows()
else :
    print("start debugging LOL")
    print(type(image))
    print("\n\n",image)