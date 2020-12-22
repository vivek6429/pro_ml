#Driver drowsiness detection 

#data set https://sites.google.com/view/utarldd/home

features focused on -- ear,mar,puc --- no 
features l_eye r_eye ---> cnn model

Haar cascade ---> tooo many issues on detecting, eyes while face detection is good
found out face landmarks does a good job

changing approach --<> 
    use haar cascade to detect  face on image = ok

    crop it                                   =ok

    use face landmarks on it                  =<->


use live_test.py for a live test

The pickle files contains images of eyes....

model tarining on cnn.ipynb

trained model is the file called "model"


dataextraction.py to extract the images from vids

currently we are overfitting 

need to try things like dataaugmentation also play with model hyperparametes 