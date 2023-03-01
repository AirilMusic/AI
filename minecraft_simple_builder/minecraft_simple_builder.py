import tensorflow as tf
import numpy as np

# Definimos el dataset de bloques para entrenar al modelo
examples = [[[[1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1]]], 
                       [[[1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1]]]] #[z[y[x]]]

dataset = [] # aqui se generan mas ejemplos cambiandole colores (de forma ordenada, no genera todas las combinaciones) a los ejemplos
for i in examples:
    dataset.append(i)

for i in range(1, 200):
    arr = []
    for z in examples:
        arrz = []
        for y in z:
            arry = []
            for x in y:
                if x <= 200 and x >= 1:
                    if x + i <= 200:
                        arry.append(x + i)
                    else:
                        arry.append(200 - x + i)
                else:
                    arry.append(x)
        arr.append(arrz)  
    dataset.append(arr) 
            
blockArray = np.array(dataset)
# Cada bloque puede tener un valor de 0 a 255, donde 0 es aire y los demás valores son bloques, de 201 a 230 son slabs y de 231 a 255 son escaleras

# Dividimos el dataset en entrenamiento, validación y prueba
entrenamiento, validacion, prueba = np.split(blockArray, [int(0.6*len(blockArray)), int(0.8*len(blockArray))])

# Creamos el modelo de red neuronal
modelo = tf.keras.Sequential([
    tf.keras.layers.Conv3D(32, (3, 3, 3), activation='relu', input_shape=(2, 2, 2, 1)),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu'),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Conv3D(128, (3, 3, 3), activation='relu'),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(256, activation='softmax')
])

# Compilamos el modelo
modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenamos el modelo
print("Comenzando entrenamiento...")
modelo.fit(entrenamiento, epochs=10, validation_data=validacion)
print("Entrenamiento finalizado")

# Evaluamos el modelo con el conjunto de prueba
resultado = modelo.evaluate(prueba)
print('Pérdida (loss) en el conjunto de prueba:', resultado[0])
print('Precisión (accuracy) en el conjunto de prueba:', resultado[1])

# Generamos un nuevo conjunto de entrada aleatorio para la red neuronal
nuevo_input = np.random.randint(0, 255, size=(1, 2, 2, 2, 1))

# Generamos una nueva construcción utilizando el modelo de red neuronal entrenado
nueva_construccion = modelo.predict(nuevo_input)

# Imprimimos la nueva construcción generada
print(nueva_construccion)