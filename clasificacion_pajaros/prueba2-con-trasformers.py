### WORK IN PROGRESS ###

# Una forma de mejorar este modelo de clasificación de imágenes utilizando transformers sería reemplazar la arquitectura de red neuronal convolucional (ConvNet) por un modelo de transformers pre-entrenado como BERT o ViT. Este tipo de modelos son muy eficaces para la tarea de clasificación de imágenes a nivel de pixels utilizando una técnica conocida como patch embeddings.

#! pip install transformers
#! pip install opencv-python

import tensorflow as tf
import tensorflow_datasets as ds
import numpy as np
import transformers
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
  
# Transformar las imágenes en patches
patches = []
for img in x:
    patch = tf.image.extract_patches(
        images=[img],
        sizes=[1, img_size//16, img_size//16, 1],
        strides=[1, img_size//16, img_size//16, 1],
        rates=[1, 1, 1, 1],
        padding='VALID'
    )
    patch = tf.reshape(patch, [img_size//16, img_size//16, -1, 3])
    patch = tf.transpose(patch, [2, 0, 1, 3])
    patches.append(tf.reshape(patch, [-1, img_size//16, img_size//16, 3]))
    patches.append(patch)

x = tf.stack(patches, axis=0)
x = tf.reshape(x, [-1, img_size, img_size, 3])
x = tf.cast(x, tf.float32)
x = x / 255.
y = np.array(y)

# Cargar un modelo ViT pre-entrenado
model = transformers.TFViT.from_pretrained('vit-base')

# Obtener las representaciones de los patches
patches_embeddings = model(x)
patches_embeddings = patches_embeddings[0]

# Media pooling para obtener la representación de la imagen completa
patches_embeddings = tf.reshape(patches_embeddings, [-1, img_size//16*img_size//16, model.config.hidden_size])
img_embeddings = tf.reduce_mean(patches_embeddings, axis=1)

# Capa densa para realizar la clasificación
classifier = tf.keras.layers.Dense(metadata.features['label'].num_classes, activation='softmax')
logits = classifier(img_embeddings)

model = tf.keras.Model(inputs=model.inputs, outputs=logits)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x, y, epochs=5, batch_size=32)
