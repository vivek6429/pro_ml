import moviepy.editor
import os
from pathlib import Path

    
def vidlength():
# Converts into more readable format
    def convert(seconds):
        hours = seconds // 3600
        seconds %= 3600

        mins = seconds // 60
        seconds %= 60

        return hours, mins, seconds


    # Create an object by passing the location as a string
    
    video = moviepy.editor.VideoFileClip("D:\path\to\video.mp4")

    # Contains the duration of the video in terms of seconds
    video_duration = int(video.duration)

    hours, mins, secs = convert(video_duration)
    return hours,mins,secs


def traversal():
    path = "D:\series\see"
    
    #finding the path of videos
    fpath = []
    for root,d_names,f_names in os.walk(path):
	    for f in f_names:
		    fpath.append(os.path.join(root, f))
    
    #finding the file name from the path
    fname=[]
    for i in fpath:
        fname.append(Path(i).stem)
    
    #finding the label from file name by removing underscore
    label=[]
    for i in fname:
        split_string =i.split("_", 1)
        substring = split_string[0]
        label.append(substring)
    return (fname,label)


if __name__ == "__main__":


