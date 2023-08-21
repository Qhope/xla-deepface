
import os
from deepface.basemodels import (CustomFaceNet,Facenet)
from deepface import DeepFace
import tensorflow as tf

print('test CUDA',tf.test.is_built_with_cuda())
print('GPU',tf.config.list_physical_devices('GPU'))

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

PATH = './dataset/trainset'
PATH_HAAR='./dataset/haarcascade_frontalface_default.xml'

tf.debugging.set_log_device_placement(True)

# Place tensors on the CPU
try:
  # Specify an invalid GPU device
  with tf.device('/device:GPU:0'):
    a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    c = tf.matmul(a, b)
except RuntimeError as e:
  print(e)

# train
CustomFaceNet.train(PATH,PATH_HAAR)
# model =CustomFaceNet.loadModel()
# print(model.summary())