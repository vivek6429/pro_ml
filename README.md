# Driver drowsiness detection 

## [Dataset](https://sites.google.com/view/utarldd/home) :sparkles:

~~features focused on -- ear,mar,puc ~~
features l_eye r_eye images ---> cnn model


### Tasks::coffee:
- [x] Extract images from dataset
    - [x] getframe function
    - [x] video orentation
- [x] data cleaning
- [x] pickle the data
- [x] train model
- [x] live working model
- [x] tinker with model hyper parameters
- [ ] tryout more model structures
- [ ] tryout stuff like dataaugmentaion
- [ ] create a better gui
- [ ] improve this readme

Haar cascade ---> tooo many issues on detecting eyes,while face detection is good
found out face landmarks does a good job

# Requirements:
1. Dlib
2. Tf
3. [Exiftool](https://exiftool.org/) for acessing video metadata
4. moviepy (used this during training to get vid length)

# NOTES:
- use live_test.py for a live Demo
- The pickle files contains extracted eye data
- model training on cnn.ipynb 
- trained model is the file called "model"
- dataextraction.py to extract the images from vids
- currently we are overfitting 
- need to try things like dataaugmentation also play with model hyperparametes 
