#lo primero que hay que aclarar es que si se cambian los datos sirve para cualquier otro tipo de moneda
#los datos estan tomados desde el 2022-06-16 hasta el 2022-08-21

import tensorflow as tf
import numpy as np

day = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66], dtype=int)
price = np.array([20386.6, 20444.6, 18986.5, 20577.2, 20572.3, 20720.4, 19965.8, 21100.7, 21226.9, 21489.9, 21043.5, 20730.2, 20278.0, 20111.3,	19926.6, 19262.9, 19243.2, 19309.9, 20215.8, 20200.6, 20561.1, 21637.8, 21611.2, 21587.5, 20847.4, 19963.2, 19330.9, 20250.0, 20586.0, 20825.1, 21209.9, 20785.6, 22525.8, 23410.2, 23215.2, 23153.0, 22675.2, 22460.4, 22582.1, 21301.9, 21248.7, 22958.3, 23850.0, 23774.3, 23634.2, 23303.4, 23271.2, 22988.6, 22820.8, 22612.1, 23308.2, 22944.2, 23175.3, 23816.3, 23146.7, 23962.9, 23935.3, 24398.7, 24442.5, 24302.8, 24101.7, 23856.8, 23338.0, 23203.6, 20831.3, 21138.9], dtype=float)

trainDay = np.array([7,16,22,41,60], dtype=int)
trainPrice = np.array([19965.8, 19262.9, 21637.8, 21248.7, 24302.8], dtype=int)

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[1]),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dense(1500, activation = tf.nn.relu),
    tf.keras.layers.Dense(1500, activation = tf.nn.relu),
    tf.keras.layers.Dense(1500, activation = tf.nn.relu),
    tf.keras.layers.Dense(1500, activation = tf.nn.relu),
    tf.keras.layers.Dense(1000, activation = tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer = tf.keras.optimizers.Adam(0.1), loss = 'mean_squared_error')

print("\nStarting training...")
historyR = model.fit(day, price, epochs = 1000, verbose=False)
print("Trainning ended uwu")

print("Predicting...")
newday = int(input("Day (next to 2022-06-16, example: 63): "))
resultado = model.predict([newday])
print("Es probable que el precio ronde los: ", resultado, " $")
