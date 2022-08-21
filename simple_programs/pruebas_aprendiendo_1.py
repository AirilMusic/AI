#lo primero, no se que coño hacer asi que a pensar algo XD
#ya se, una IA que te diga el precio de un videojuego segun varias caracteristicas que tengan y que aprenda con ejemplos de otros juegos que ya estan en venta
import tensorflow as tf
import numpy as np

#el 80% sera para train y el 20 para test
#los datos los he cojido de juegos que he escojido de steam de forma aleatoria
horas_de_juego = [12, 30, 20, 150, 36, 20, 16, 20, 4, 3]
calidad_grafica = [10, 10, 6, 10, 9, 10, 5, 6, 6, 8] # del 1 al 10
multijugador = [0, 1, 1, 1, 0, 1, 0, 1, 1, 0] #1 = si, 0 = no
categoria = [1, 0, 3, 5, 1, 2, 5, 4, 0, 5] #0 = accion, 1 = aventura, 2 = rpg, 3 = sandbox, 4 = simulador, 5 = otros
actualizaciones_gratuitas = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1] #1 = si, 0 = no
edad_minima = [12, 18, 10, 12, 16, 18, 6, 12, 10, 10] #años
otros_idiomas = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1] #1 = si, 0 = no

datos1 = []
for i in range(len(horas_de_juego)):
    lista = [horas_de_juego[i], calidad_grafica[i], multijugador[i], categoria[i], actualizaciones_gratuitas[i], edad_minima[i], otros_idiomas[i]]
    datos1.append(lista)

datos = np.array(datos1)

precio = np.array([20, 30, 24, 30, 10, 25, 20, 12, 6, 8], dtype=int) #en euros

#Estructura de la red:
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[7]), #input = variables
    tf.keras.layers.Dense(1000, activation = tf.nn.relu), #hidden layer 1
    tf.keras.layers.Dense(1000, activation = tf.nn.relu), #hidden layer 2
    tf.keras.layers.Dense(1000, activation = tf.nn.relu), #hidden layer 3
    tf.keras.layers.Dense(100, activation = tf.nn.relu), #hidden layer 4
    tf.keras.layers.Dense(1, activation = tf.nn.relu) #output = price
])

model.compile(optimizer = tf.keras.optimizers.Adam(0.1), loss = 'mean_squared_error')

#Entrenamiento:
print("Comenzando entrenamiento...")
historial = model.fit(datos, precio, epochs = 100, verbose=False)
print("Entrenamiento finalizado uwu")

#Predicciones:
horas = int(input("Cuantas horas de gamplay hay (ejemplo: 4): "))
calidad = int(input("Del 1 al 10 como valorarias la calidad gráfica (ejemplo: 7): "))
multi = int(input("Tiene multijugador (1 = si, 0 = no): "))
categ = int(input("Categoria del juego (0 = accion, 1 = aventura, 2 = rpg, 3 = sandbox, 4 = simulador, 5 = otros): "))
actualizaciones = int(input("Tiene actualizaciones gratuitas (1 = si, 0 = no): "))
edad = int(input("Edad minima para jugar (ejemplo: 18): "))
idiomas = int(input("Tiene varios idiomas (1 = si, 0 = no): "))

condiciones = np.array([horas, calidad, multi, categ, actualizaciones, edad, idiomas], dtype=int)
print(condiciones)

resultado = model.predict([condiciones])
print("El precio recomendado para el juego es: ", resultado, " €")
