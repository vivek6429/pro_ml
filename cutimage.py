# testing stuff
import cv2
from customcvfunc import imagesplitter

img2 = cv2.imread("extracted_data/10/55_120.jpeg",0)
img = cv2.imread("/home/v/Projects/pro_ml/aaaaaaaa.jpeg",1)

y=0
x=0
h=32
w=32
img=cv2.resize(img,(64,32))
crop_imgl = img[y:y+h, x:x+w] # 0 to 32 rows , 0 to 32 cols
crop_imgr = img[y:y+h, x+w:x+w+w] # 0 to 32 rows , 0 to 32 cols
# print(crop_img.shape)
# print(img.shape)

crop_imgl,crop_imgr = imagesplitter(img2)

cv2.imshow("e",img2)
cv2.imshow("image",img)
cv2.imshow("image",crop_imgl)
cv2.imshow("imagssse",crop_imgr)
cv2.waitKey(0)
cv2.destroyAllWindows()