
import os
from deepface.basemodels import (CustomFaceNet,Facenet)
from deepface import DeepFace

PATH = './dataset/trainset'
PATH_HAAR='./dataset/haarcascade_frontalface_default.xml'

reference_images=[]
selfies=[]
n_sub=0

for folder in os.listdir(PATH):
    subfolder=os.path.join(PATH,folder)
    for sub in os.listdir(subfolder):
        n_sub=n_sub+1
        img_dir=os.path.join(subfolder,sub)
        for img_raw in os.listdir(img_dir):
            if 'script' in img_raw:
                reference_images.append(img_raw)
            else :
                selfies.append(img_raw)

print("The total number of Folders in dataset : ",len(os.listdir(PATH)))
print("The total number of Employee in dataset : ",n_sub)
print("The total number of selfies are : ",len(selfies))
print("The total number of script images are : ",len(reference_images))

# train
CustomFaceNet.train(PATH,PATH_HAAR)
# model =CustomFaceNet.loadModel()
# print(model.summary())