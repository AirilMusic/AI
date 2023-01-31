### WORK IN PROGRESS ###

import tensorflow as tf
import tensorflow_datasets as ds
import numpy as np

import matplotlib.pyplot as plt
import cv2

data, metadata = ds.load('caltech_birds2011', as_supervised=True, with_info=True)
img_size = 170

training_data = []

for i, (image, tag) in enumerate(data['train']):
  image = cv2.resize(image.numpy(),(img_size, img_size))  
  training_data.append([image, tag])

x = [] #fotos
y = [] #tags

for image, tag in training_data:
  x.append(image)
  y.append(tag)
  
#DATA GENERATOR (modifica las fotos del dataset para generar el doble de fotos; rotandolas, desplazandolas...)
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=15,
    zoom_range=[0.7, 1.4],
    horizontal_flip=True,
    vertical_flip=True
)

x2 = x
x3 = x

datagen.fit(x2)
datagen.fit(x3)

for i in range(len(x)): #añade las fotos modificadas al las del dataset
  x.append(x2[i])
  y.append(y[i])
  x.append(x3[i])
  y.append(y[i])
  
x = np.array(x)
y = np.array(y)

def PositionalEncoding(inputs, maxlen=None):
    """
    Compute the positional encodings for a batch of sequences
    """
    E = inputs.shape[-1]
    N, T = tf.shape(inputs)[0], tf.shape(inputs)[1]
    if maxlen is None:
        maxlen = T
    pe = np.zeros((N, maxlen, E))
    position = np.arange(0, maxlen)[np.newaxis, :]
    div_term = np.exp(np.arange(0, E, 2) * -(np.log(10000.0) / E))
    pe[:, :, 0::2] = np.sin(position * div_term)
    pe[:, :, 1::2] = np.cos(position * div_term)
    return tf.cast(pe, tf.float32)

def transformer_block(inputs,
                      num_heads,
                      feed_forward_hidden,
                      activation,
                      dropout_rate=0.1,
                      train=True,
                      use_b
