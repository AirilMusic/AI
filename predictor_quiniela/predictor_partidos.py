import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

datos = []
with open('Match_Result_Prediction.txt', 'r') as f:
    for linea in f:
        partido = eval(linea.strip())
        datos.append(partido)

caracteristicas = []
etiquetas = []
for partido in datos:
    equipo1 = partido['team1']
    equipo2 = partido['team2']
    caracteristicas_partido = []
    caracteristicas_partido.extend([equipo1['total_victorias'], equipo1['total_derrotas'], equipo1['partido_temporada'], equipo1['victorias_temporada'], equipo1['derrotas_temporada'], equipo1['empates_temporada']])
    caracteristicas_partido.extend(equipo1['jugadores'])
    caracteristicas_partido.append(1 if equipo1['enCasa'] else 0)
    caracteristicas_partido.append(equipo1['media_posesion'])
    caracteristicas_partido.append(equipo1['media_tiros'])
    caracteristicas_partido.append(equipo1['goles_temporada'])
    caracteristicas_partido.append(equipo1['edad_media'])
    caracteristicas_partido.extend([equipo2['total_victorias'], equipo2['total_derrotas'], equipo2['partido_temporada'], equipo2['victorias_temporada'], equipo2['derrotas_temporada'], equipo2['empates_temporada']])
    caracteristicas_partido.extend(equipo2['jugadores'])
    caracteristicas_partido.append(1 if equipo2['enCasa'] else 0)
    caracteristicas_partido.append(equipo2['media_posesion'])
    caracteristicas_partido.append(equipo2['media_tiros'])
    caracteristicas_partido.append(equipo2['goles_temporada'])
    caracteristicas_partido.append(equipo2['edad_media'])
    caracteristicas_partido.extend([partido['temperatura'], 1 if partido['precipitaciones'] else 0, partido['altitud']])
    caracteristicas.append(caracteristicas_partido)
    etiquetas.append(partido['resultado'])

# Ampliacion de datos, para mejorar la precision
ad = preprocessing.MinMaxScaler()
ad.fit(caracteristicas)
caracteristicas_escaladas = ad.transform(caracteristicas)

# Dividir los datos en entrenamiento y prueba
x_entrenamiento, x_prueba, y_entrenamiento, y_prueba = train_test_split(
    caracteristicas_escaladas, etiquetas, test_size=0.2, random_state=42)

y_entrenamiento_categorico = tf.keras.utils.to_categorical(y_entrenamiento, num_classes=3)
y_prueba_categorico = tf.keras.utils.to_categorical(y_prueba, num_classes=3)

modelo = tf.keras.Sequential([ # tengo que poner esto bien, de momento solo esta como prueba, pero no lo voy a poner bien hasta hacer todo el dataset
    tf.keras.layers.Dense(32, input_dim=caracteristicas_escaladas.shape[1], activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

modelo.compile
