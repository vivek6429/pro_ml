#Driver drowsiness detection 

#data set https://sites.google.com/view/utarldd/home

features focused on -- ear,mar,puc --- no 
features l_eye r_eye ---> cnn model

Haar cascade ---> tooo many issues on detecting, eyes while face detection is good
found out face landmarks does a good job

changing approach --<> 
    use haar cascade to detect  face on image = <done>
    crop it                                   =<done>
    use face landmarks on it                  =<->


Need to find a way to pass/pipe the image data to train the model...

