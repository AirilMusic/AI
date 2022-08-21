#De momento no he conseguido datos de las bajas por semana asi que no puedo terminar esta IA :(
#Pero creo que ya estaria terminada la parte de programaccion

import tensorflow as tf
import numpy as np

weeks = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26], dtype=int)
russianDeads = np.array([], dtype=int)
ukranianDeads = np.array([], dtype=int)

trainWeeks = np.array([], dtype=int)
trainRussianDeads = np.array([], dtype=int)
trainUkranianDeads = np.array([], dtype=int)

modelR = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[1]),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1)
])

modelU = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[1]),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1)
])

modelR.compile(optimizer = tf.keras.optimizers.Adam(0.1), loss = 'mean_squared_error')
modelU.compile(optimizer = tf.keras.optimizers.Adam(0.1), loss = 'mean_squared_error')

print("Starting training...")
historyR = modelR.fit(weeks, russianDeads, epochs = 500, verbose=False)
historyU = modelU.fit(weeks, ukranianDeads, epochs = 500, verbose=False)
print("Trainning ended uwu")

print("Russian model acuracy: ", modelR.evaluate(trainWeeks, trainRussianDeads))
print("Ukranian model acuracy: ", modelU.evaluate(trainWeeks, trainUkranianDeads))

print("Predicting...")
week = int(input("Week: "))
resultadoR = modelR.predict([week])
resultadoU = modelU.predict([week])
print("Russian deads in the week ", week, " will be probaly ", resultadoR, " soldiers, and Ukranian deads will be probably ", resultadoU, " soldiers")

