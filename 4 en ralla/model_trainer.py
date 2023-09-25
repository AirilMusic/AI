# AlphaFir (Alpha Four In Row)
# Made by Airil/Ainhoa and IA based on AlphaZero algorithm

import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

changes_ratio = 20 # a las x partidas baja a 10, y a las x partidas a 5 y asi hasta llegar a 2 o 1, si se carga un modelo ya entrenado empieza con 10 y con ese x de partidas
partida = 0

tablero_base = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]

def save_network(network, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    save_path = os.path.join(script_dir, 'networks')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    network.save(os.path.join(save_path, filename))
    print("[+] Saved network")

def place_a_tile(tablero, column, player):
    numerajo_mas_bajo = 0 # el numerajo mas bajo es el numero del bichajo
    unajo = 1

    for i in tablero:
        if tablero[column] == 0:
            nujmerajo_mas_bajo += unajo
        else:
            break

    # ya ta encontrado el numerajo mas bajo uwu
    # si, estoy programando a las 5am una ia que juega al 4 en ralla mientras veo un bollodrama, porfi no me juzguen

    tablero[numerajo_mas_bajo][column] = player # player son 1 o 2, porque ese es el numero de neuronas que tengo :)
    
    return tablero

def check_cuatrejo_en_rallejo(board, player, last_column):
    rallitas, columnitas = len(board), len(board[0])

    # ladajo
    for row in range(rallitas):
        for col in range(max(0, last_column - 3), min(columnitas - 3, last_column + 1)):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # arribajo
    for row in range(rallitas - 3):
        if all(board[row + i][last_column] == player for i in range(4)):
            return True

    # diagonal bajorriba
    for row in range(3, rallitas):
        for col in range(max(0, last_column - 3), min(columnitas - 3, last_column + 1)):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    # diagonal arribajo
    for row in range(rallitas - 3):
        for col in range(max(0, last_column - 3), min(columnitas - 3, last_column + 1)):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False

partida = 1

# AHORA TOCA LA IA BAILONGA, AlphaFisting, osea, quiero decir, AlphaFir jajaja

class AlphaFir:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.value = 0

def MCTS(root, model):
    for i in range(800):
        pass

def best_move(root):
    return max(root.children.items(), key=lambda item: item[1].visits)[0]

def build_model():
    board_input = tf.keras.layers.Input(shape=(6, 7, 1), name='board_input')
    x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu')(board_input)
    x = tf.keras.layers.Flatten()(x)
    policy_head = tf.keras.layers.Dense(7, activation='softmax', name='policy')(x)
    value_head = tf.keras.layers.Dense(1, activation='tanh', name='value')(x)

    model = tf.keras.models.Model(inputs=[board_input], outputs=[policy_head, value_head])
    model.compile(optimizer='adam', loss=['categorical_crossentropy', 'mean_squared_error'])

    return model

model = build_model()

while True:
    movimiento = 1
    board = tablero_base.copy()
    column = 0
    root = AlphaFir(board)

    while True: # comienza la partida: ave cesar, gallina tu madre
        if movimiento % 2 == 0:
            player = 2
        else:
            player = 1
        
        if movimiento > 6: # ckeckea si hay 4 en ralla (los primeros 6 movimientos no porque es imposible y asi es un poquito mas eficiente)
            if check_cuatrejo_en_rallejo(board, player, column):
                print("Ganador: " + player)
                partida += 1
                break
        
        movimiento += 1
