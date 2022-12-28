###### WORK IN PROGRESS ######

import tensorflow as tf
import tensorflow_datasets as ds
import numpy as np

import matplotlib.pyplot as plt
import cv2

data, metadata = ds.load('caltech_birds2011', as_supervised=True, with_info=True)
plt.figure(figsize=(20,20))
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

datagen.fit(x2)

for i in range(len(x)): #añade las fotos modificadas al las del dataset
  x.append(x2[i])
  y.append(y[i])
  
x = np.array(x)
y = np.array(y)

modeloAD = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(170, 170, 3)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2, 2),

  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(300, activation='relu'),
  tf.keras.layers.Dense(250, activation='relu'),
  tf.keras.layers.Dense(1, activation='relu')
])

modeloAD.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

x_training = x[:9000]
x_test = x[9000:]

y_training = y[:9000]
y_test = y[9000:]

data_gen_entrenamiento = datagen.flow(x_training, y_training, batch_size=32)

modeloAD.fit(
    data_gen_entrenamiento,
    epochs=100, batch_size=32,
    validation_data=(x_test, y_test),
    steps_per_epoch=int(np.ceil(len(x_training) / float(32))),
    validation_steps=int(np.ceil(len(y_training) / float(32))))
