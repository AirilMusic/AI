import tensorflow as tf
import numpy as np

pid0 = ["AB871800","AB871800","AB871800","AB871800","AB871800","AB871800","AB871800","AB871800","AB871800","AB871800"]#,"D0B50704","D0B50704","D0B50704","D0B50704","D0B50704","D0B50704","D0B50704","D0B50704","D0B50704","D0B50704"
tid = [32,50,99,133,12,378,44,567,5742,8732]

x1 = []
for i in range(len(pid0)):
  pid=bin(int(pid0[i], 16))
  n00 = 0
  pid1 = ""
  for a in pid:
    if n00 > 1:
      pid1 += a
    n00 += 1
  while len(pid1)/2 < 16 or len(pid1)%2 != 0:
    pid1 = "0" + pid1
  x1.append([int(pid1), tid[i]])


x = np.array([x1])
y = np.array([45991,46005,46052,45826,45963,45821,45995,45488,42473,37275])

x_training = x[:int(len(x1)*0.5)]
x_test = x[int(len(x1)*0.5):]

y_training = y[:int(len(x1)*0.5)]
y_test = y[int(len(x1)*0.5):]

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(2, activation='relu'),
    tf.keras.layers.Dense(200, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(200, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1, activation='relu')
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

model.fit(
    x, y,
    epochs=1000, batch_size=32,
    validation_data=(x_test, y_test))