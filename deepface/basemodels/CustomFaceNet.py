import tensorflow as tf 
import numpy as np
import os
# from keras.layers import Conv2D, Activation, AveragePooling2D, MaxPooling2D, ZeroPadding2D, Input, concatenate, Lambda, Dense, Flatten,BatchNormalization
from numpy import genfromtxt
import cv2
from keras import backend as K
from keras.layers import *
from keras.models import Model

# K.set_image_data_format('channels_last')
import random
# import matplotlib.pyplot as plt
import keras
from keras.utils import plot_model
import sys
tf_version = int(tf.__version__.split(".", maxsplit=1)[0])
print(tf_version)

if tf_version == 1:
    from keras.models import Model
    from keras.layers import Activation
    from keras.layers import BatchNormalization
    from keras.layers import Concatenate
    from keras.layers import Conv2D
    from keras.layers import Dense
    from keras.layers import Dropout
    from keras.layers import GlobalAveragePooling2D
    from keras.layers import Input
    from keras.layers import Lambda
    from keras.layers import MaxPooling2D
    from keras.layers import add
    from keras import backend as K
else:
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Activation
    from tensorflow.keras.layers import BatchNormalization
    from tensorflow.keras.layers import Concatenate
    from tensorflow.keras.layers import Conv2D
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import Dropout
    from tensorflow.keras.layers import GlobalAveragePooling2D
    from tensorflow.keras.layers import Input
    from tensorflow.keras.layers import Lambda
    from tensorflow.keras.layers import MaxPooling2D
    from tensorflow.keras.layers import add
    from tensorflow.keras import backend as K
# --------------------------------

def inception_block_1a(X):
    X_3=Conv2D(96,(1,1),data_format='channels_last',name='inception_3a_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3a_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(128,(3,3),data_format='channels_last',name='inception_3a_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3a_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    X_5=Conv2D(16,(1,1),data_format='channels_last',name='inception_3a_5x5_conv1')(X)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3a_5x5_bn1')(X_5)
    X_5=Activation('relu')(X_5)
    X_5=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_5)
    X_5=Conv2D(32,(5,5),data_format='channels_last',name='inception_3a_5x5_conv2')(X_5)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3a_5x5_bn2')(X_5)
    X_5=Activation('relu')(X_5)
    
    X_pool = MaxPooling2D(pool_size=3, strides=2, data_format='channels_last')(X)
    X_pool = Conv2D(32, (1, 1), data_format='channels_last', name='inception_3a_pool_conv')(X_pool)
    X_pool = BatchNormalization(axis=3, epsilon=0.00001, name='inception_3a_pool_bn')(X_pool)
    X_pool = Activation('relu')(X_pool)
    X_pool = ZeroPadding2D(padding=((3, 4), (3, 4)), data_format='channels_last')(X_pool)
    
    X_1=Conv2D(64,(1,1),data_format='channels_last',name='inception_3a_1x1_conv')(X)
    X_1=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3a_1x1_bn')(X_1)
    X_1=Activation('relu')(X_1)
    
    inception=concatenate([X_3,X_5,X_pool,X_1],axis=3)
    return inception

def inception_block_1b(X):
    X_3=Conv2D(96,(1,1),data_format='channels_last',name='inception_3b_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(128,(3,3),data_format='channels_last',name='inception_3b_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    X_5=Conv2D(32,(1,1),data_format='channels_last',name='inception_3b_5x5_conv1')(X)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_5x5_bn1')(X_5)
    X_5=Activation('relu')(X_5)
    X_5=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_5)
    X_5=Conv2D(64,(5,5),data_format='channels_last',name='inception_3b_5x5_conv2')(X_5)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_5x5_bn2')(X_5)
    X_5=Activation('relu')(X_5)
    
    X_P=AveragePooling2D(pool_size=(3,3),strides=(3,3),data_format='channels_last')(X)
    X_P=Conv2D(64,(1,1),data_format='channels_last',name='inception_3b_pool_conv')(X_P)
    X_P=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_pool_bn')(X_P)
    X_P=Activation('relu')(X_P)
    X_P=ZeroPadding2D(padding=(4,4),data_format='channels_last')(X_P)
    
    X_1=Conv2D(64,(1,1),data_format='channels_last',name='inception_3b_1x1_conv')(X)
    X_1=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3b_1x1_bn')(X_1)
    X_1=Activation('relu')(X_1)
    
    inception=concatenate([X_3,X_5,X_P,X_1],axis=3)
    return inception

def inception_block_1c(X):
    X_3=Conv2D(128,(1,1),data_format='channels_last',name='inception_3c_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3c_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(256,(3,3),strides=(2,2),data_format='channels_last',name='inception_3c_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3c_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    X_5=Conv2D(32,(1,1),data_format='channels_last',name='inception_3c_5x5_conv1')(X)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3c_5x5_bn1')(X_5)
    X_5=Activation('relu')(X_5)
    X_5=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_5)
    X_5=Conv2D(64,(5,5),strides=(2,2),data_format='channels_last',name='inception_3c_5x5_conv2')(X_5)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_3c_5x5_bn2')(X_5)
    X_5=Activation('relu')(X_5)
    
    X_P=MaxPooling2D(pool_size=3,strides=2,data_format='channels_last')(X)
    X_P=ZeroPadding2D(padding=((0,1),(0,1)),data_format='channels_last')(X_P)
    

    inception=concatenate([X_3,X_5,X_P],axis=3)
    return inception

def inception_block_2a(X):
    X_3=Conv2D(96,(1,1),data_format='channels_last',name='inception_4a_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(192,(3,3),data_format='channels_last',name='inception_4a_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    X_5=Conv2D(32,(1,1),data_format='channels_last',name='inception_4a_5x5_conv1')(X)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_5x5_bn1')(X_5)
    X_5=Activation('relu')(X_5)
    X_5=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_5)
    X_5=Conv2D(64,(5,5),data_format='channels_last',name='inception_4a_5x5_conv2')(X_5)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_5x5_bn2')(X_5)
    X_5=Activation('relu')(X_5)
    
    X_P=AveragePooling2D(pool_size=(3,3),strides=(3,3),data_format='channels_last')(X)
    X_P=Conv2D(128,(1,1),data_format='channels_last',name='inception_4a_pool_conv')(X_P)
    X_P=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_pool_bn')(X_P)
    X_P=Activation('relu')(X_P)
    X_P=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_P)
    
    X_1=Conv2D(256,(1,1),data_format='channels_last',name='inception_4a_1x1_conv')(X)
    X_1=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4a_1x1_bn')(X_1)
    X_1=Activation('relu')(X_1)
    
    inception=concatenate([X_3,X_5,X_P,X_1],axis=3)
    return inception

def inception_block_2b(X):
    X_3=Conv2D(160,(1,1),data_format='channels_last',name='inception_4e_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4e_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(256,(3,3),strides=(2,2),data_format='channels_last',name='inception_4e_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4e_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    X_5=Conv2D(64,(1,1),data_format='channels_last',name='inception_4e_5x5_conv1')(X)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4e_5x5_bn1')(X_5)
    X_5=Activation('relu')(X_5)
    X_5=ZeroPadding2D(padding=(2,2),data_format='channels_last')(X_5)
    X_5=Conv2D(128,(5,5),strides=(2,2),data_format='channels_last',name='inception_4e_5x5_conv2')(X_5)
    X_5=BatchNormalization(axis=3,epsilon=0.00001,name='inception_4e_5x5_bn2')(X_5)
    X_5=Activation('relu')(X_5)
    
    X_P=MaxPooling2D(pool_size=3,strides=2,data_format='channels_last')(X)
    X_P=ZeroPadding2D(padding=((0,1),(0,1)),data_format='channels_last')(X_P)

    inception=concatenate([X_3,X_5,X_P],axis=3)
    return inception

def inception_block_3a(X):
    X_3=Conv2D(96,(1,1),data_format='channels_last',name='inception_5a_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5a_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(384,(3,3),data_format='channels_last',name='inception_5a_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5a_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)

    
    X_P=AveragePooling2D(pool_size=(3,3),strides=(3,3),data_format='channels_last')(X)
    X_P=Conv2D(96,(1,1),data_format='channels_last',name='inception_5a_pool_conv')(X_P)
    X_P=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5a_pool_bn')(X_P)
    X_P=Activation('relu')(X_P)
    X_P=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_P)
    
    X_1=Conv2D(256,(1,1),data_format='channels_last',name='inception_5a_1x1_conv')(X)
    X_1=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5a_1x1_bn')(X_1)
    X_1=Activation('relu')(X_1)
    
    inception=concatenate([X_3,X_P,X_1],axis=3)
    return inception
def inception_block_3b(X):
    X_3=Conv2D(96,(1,1),data_format='channels_last',name='inception_5b_3x3_conv1')(X)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5b_3x3_bn1')(X_3)
    X_3=Activation('relu')(X_3)
    X_3=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_3)
    X_3=Conv2D(384,(3,3),data_format='channels_last',name='inception_5b_3x3_conv2')(X_3)
    X_3=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5b_3x3_bn2')(X_3)
    X_3=Activation('relu')(X_3)
    
    
    X_P=MaxPooling2D(pool_size=(3,3),strides=2,data_format='channels_last')(X)
    X_P=Conv2D(96,(1,1),data_format='channels_last',name='inception_5b_pool_conv')(X_P)
    X_P=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5b_pool_bn')(X_P)
    X_P=Activation('relu')(X_P)
    X_P=ZeroPadding2D(padding=(1,1),data_format='channels_last')(X_P)
    
    X_1=Conv2D(256,(1,1),data_format='channels_last',name='inception_5b_1x1_conv')(X)
    X_1=BatchNormalization(axis=3,epsilon=0.00001,name='inception_5b_1x1_bn')(X_1)
    X_1=Activation('relu')(X_1)
    
    inception=concatenate([X_3,X_P,X_1],axis=3)
    return inception


def FinalModel(input_shape):
    
    X_input=Input(input_shape)
    
    X=ZeroPadding2D(padding=(3,3))(X_input)
    X=Conv2D(64,(7,7),strides=(2,2),name='conv1')(X)
    X=BatchNormalization(axis=3,name='bn1')(X)
    X=Activation('relu')(X)
    
    X=ZeroPadding2D((1,1))(X)
    X=MaxPooling2D((3,3),strides=2)(X)
    
    X=Conv2D(64,(1,1),strides=(1,1),name='conv2')(X)
    X=BatchNormalization(axis=3,epsilon=0.00001,name='bn2')(X)
    X=Activation('relu')(X) 
    
    X=ZeroPadding2D(padding=(1,1))(X)
    
    X=Conv2D(192,(3,3),strides=(1,1),name='conv3')(X)
    X=BatchNormalization(axis=3,epsilon=0.00001,name='bn3')(X)
    X=Activation('relu')(X)
    
    X=ZeroPadding2D(padding=(1,1))(X)
    X=MaxPooling2D(pool_size=(3,3),strides=(2,2))(X)
    
    X=inception_block_1a(X)
    X=inception_block_1b(X)
    X=inception_block_1c(X)
    
    X=inception_block_2a(X)
    X=inception_block_2b(X)
    
    X=inception_block_3a(X)
    X=inception_block_3b(X)
    
    X=AveragePooling2D(pool_size=(3,3),strides=(1,1),data_format='channels_last')(X)
    X=Flatten()(X)
    X=Dense(128,activation='relu',kernel_initializer='glorot_normal',name='dense_layer')(X)
    X=Lambda(lambda x:K.l2_normalize(x,axis=1),name='lambda_1')(X)
    
    model=Model(inputs=X_input,outputs=X,name='FaceRecognotionModel')
    return model    
def triplet_loss_t(y_true,y_pred):
    #print(y_pred)
    anchor=y_pred[:,0:128]
    pos=y_pred[:,128:256]
    neg=y_pred[:,256:384]
    
    positive_distance = K.sum(K.abs(anchor-pos), axis=1)
    negative_distance = K.sum(K.abs(anchor-neg), axis=1)
    probs=K.softmax([positive_distance,negative_distance],axis=0)
    #loss = positive_distance - negative_distance+alpha
    loss=K.mean(K.abs(probs[0])+K.abs(1.0-probs[1]))
    return loss

def localize_resize(path_image,path_haar='../input/haar-cascade/haarcascade_frontalface_default.xml'):
    image=cv2.imread(path_image)
    
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    classifier=cv2.CascadeClassifier(path_haar)
    faces=classifier.detectMultiScale(gray,1.1,6)
    if len(faces) != 1:#condition if we dont have any faces or cant be detected y haar cascade we will skip those
        return -1
    
    x,y,w,h=faces.squeeze()
    crop=image[y:y+h,x:x+w]
    image=cv2.resize(crop,(96,96))
    # image=np.transpose(image,(2,0,1))
    image=image.astype('float32')/255.0
    return image

def data_gen(batch_size=32,PATH='./dataset/trainset', PATH_HAAR='./dataset/haarcascade_frontalface_default.xml'):
    while True:
        i=0
        positive=[]
        anchor=[]
        negative=[]    
        

        while(i<batch_size):
            r=random.choice(os.listdir(PATH))
            p=PATH+'/'+ r
            id=os.listdir(p)
            ra=random.sample(id,2)
            pos_dir=p+'/'+ra[0]
            neg_dir=p+'/'+ra[1]
            pos=pos_dir+'/'+random.choice(os.listdir(pos_dir))
            anc=pos_dir+'/'+random.choice([x for x in os.listdir(pos_dir) if 'script' in x])
            neg=neg_dir+'/'+random.choice(os.listdir(neg_dir))
            pos_img=localize_resize(pos,PATH_HAAR)
                    #print(pos+anc+neg)
            if pos_img is -1:
                continue
            neg_img=localize_resize(neg,PATH_HAAR)
            if neg_img is -1:
                continue
            anc_img=localize_resize(anc,PATH_HAAR)
            if anc_img is -1:
                continue
            positive.append(list(pos_img))
                #print('positive{0}'.format(i))
            negative.append(list(neg_img))
                #print('negative{0}'.format(i))
            anchor.append(list(anc_img))
                #print('anchor{0}'.format(i))
            i=i+1
        #return anchor,positive,negative
        yield ([np.array(anchor),np.array(positive),np.array(negative)],np.zeros((batch_size,1)).astype("float32"))

def train(PATH, PATH_HAAR):
    try:
        with tf.device('/device:GPU:0'):
            model = FinalModel(input_shape=(96,96,3))

            triplet_model_a=Input((96,96,3))
            triplet_model_n=Input((96,96,3))
            triplet_model_p=Input((96,96,3))
            triplet_model_out=Concatenate()([model(triplet_model_a),model(triplet_model_p),model(triplet_model_n)])
            triplet_model=Model([triplet_model_a,triplet_model_p,triplet_model_n],triplet_model_out)

            triplet_model.compile(optimizer='adam',loss=triplet_loss_t)
            triplet_model.fit(data_gen(32,PATH, PATH_HAAR),steps_per_epoch=100,epochs=20)
            triplet_model.save('triplet_model.h5')
    except RuntimeError as e:
        print('error',e)

def loadModel():
    print('load model')
    triplet_model=keras.saving.load_model('./checkpoint/triplet_model.h5',custom_objects={'triplet_loss_t':triplet_loss_t})

    return triplet_model.layers[3]

