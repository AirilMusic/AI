###### WORK IN PROGRESS ######

import tensorflow as tf
import tensorflow_datasets as ds
import numpy as np

import matplotlib.pyplot as plt
import cv2

data, metadata = ds.load('caltech_birds2011', as_supervised=True, with_info=True)
plt.figure(figsize=(20,20))
img_size = 160

training_data = []

for i, (image, tag) in enumerate(data['train']):
  image = cv2.resize(image.numpy(),(img_size, img_size))  
  training_data.append([image, tag])

x = [] #fotos
y = [] #tags

for image, tag in training_data:
  x.append(image)
  y.append(tag)

x = np.array(x)
y = np.array(y)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(160,160,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(250,activation='relu'),
    tf.keras.layers.Dense(1,activation='relu')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(x, y, batch_size=32, epochs=400, verbose=True, validation_split=0.15)
