###### WORK IN PROGRESS ######

import tensorflow as tf
import tensorflow_datasets as ds
import numpy as np

import matplotlib.pyplot as plt
import cv2

data, metadata = ds.load('caltech_birds2011', as_supervised=True, with_info=True)

plt.figure(figsize=(20,20))

img_size = 160

for i, (image, tag) in enumerate(data['train'].take(25)):
  image = cv2.resize(image.numpy(),(img_size, img_size))
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.imshow(image)
  
training_data = []  
  
for i, (image, tag) in enumerate(data['train']):
      image = cv2.resize(image.numpy(),(img_size, img_size))
      training_data.append([image, tag])

#print(training_data[0]) para ver los datos de la primera foto

X = [] #fotos
Y = [] #tags

for image, tag in training_data:
  X.append(image)
  Y.append(tag)

Y = np.array(Y)
#print(Y)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(100,100,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(250,activation='relu'),
    tf.keras.layers.Dense(199,activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

tensorboardModel = tf.keras.callbacks.TensorBoard(log_dir='logs/training')
model.fit(X, Y, batch_size=32, validation_split=0.15,epochs=400,callbacks=[tensorboardModel]) ### aqui peta y no se porque 
