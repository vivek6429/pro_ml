import moviepy.editor
import os
from pathlib import Path

    
def vidlength(floc):
# Converts into more readable format
    def convert(seconds):
        hours = seconds // 3600
        seconds %= 3600

        mins = seconds // 60
        seconds %= 60

        return hours, mins, seconds


    # Create an object by passing the location as a string
    
    video = moviepy.editor.VideoFileClip(floc)

    # Contains the duration of the video in terms of seconds
    video_duration = int(video.duration)

    hours, mins, secs = convert(video_duration)
    return hours,mins,secs


def traversal(path):
   
    
    #finding the path of videos
    fpath = []
    for root,d_names,f_names in os.walk(path):
	    for f in f_names:
		    fpath.append(os.path.join(root, f))
    
    #finding the file name from the path
    # fname=[]
    # for i in fpath:
    #     fname.append(Path(i).stem)
    
    #finding the label from file name by removing underscore
    loc_n_labels=[]
    for i in fpath:
        fname=Path(i).stem
        split_string =fname.split("_", 1)
        substring = split_string[0]
        loc_n_labels.append((i,substring))
        # now we got full path and label
    return loc_n_labels



