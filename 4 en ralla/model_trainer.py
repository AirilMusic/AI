# AlphaFir (Alpha Four In Row)
# Made by Airil/Ainhoa and IA based on AlphaZero algorithm

import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

partida = 1

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

    for i in range(len(tablero)):
        if tablero[i][column] == 0:
            numerajo_mas_bajo = i
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

# AHORA TOCA LA IA BAILONGA, AlphaFisting, osea, quiero decir, AlphaFir jajaja

# PRIMERO EL ARBOL DE PROBABILIDADES PARA EL HACER UN DATASET DE LA MEJOR JUGADA PARA CADA CASO

class Node: # un nodo del arbol de probabilidades
    def __init__(self, board, player, parent=None):
        self.board = board.copy()
        self.player = player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.expanded = False

    def expand(self):
        valid_moves = False
        for col in range(len(self.board[0])):
            if self.board[0][col] == 0:
                valid_moves = True
                new_board = place_a_tile(self.board, col, self.player)
                child_node = Node(new_board, 3 - self.player, self)
                self.children.append(child_node)
        if not valid_moves:
            self.expanded = True
            return False
        self.expanded = True
        return True

    def best_child(self, exploration_weight=1.):
        if not self.children:
            return None

        scores = [(child.value / (child.visits + 1e-7)) + exploration_weight * np.sqrt(np.log(self.visits + 1) / (child.visits + 1e-7)) for child in self.children]
        return self.children[np.argmax(scores)]

training_data = []

def MCTS(root, simulations=1000):
    for i in range(simulations):
        node = root

        while node.expanded and node.children:
            node = node.best_child()

        if not node.expanded:
            node.expand()

        outcome = random_simulation(node.board, node.player)

        while node:
            node.visits += 1
            node.value += outcome
            training_data.append((node.board, best_move(node)))
            node = node.parent

def empate(board):
    for columna in board:
        if 0 in columna:
            return False
    return True

def random_simulation(board, player):
    while True:
        if empate(board):
            return 0
        col = random.choice(range(len(board[0])))
        if board[0][col] == 0:
            board = place_a_tile(board, col, player)
            if check_cuatrejo_en_rallejo(board, player, col):
                return 1 if player == 1 else -1
            player = 3 - player
        else:
            continue

def best_move(root):
    child = root.best_child(exploration_weight=0)
    if child is None:
        return None
    return root.children.index(child)

# Y AHORA UN MODELO QUE APRENDE CON ESE DATASET A PREDECIR LA MEJOR JUGADA (no se hace un dataset entero sino que varios pequeños con los que se va entrenando poquito a poquito)

model = keras.models.Sequential([
    keras.layers.InputLayer(input_shape=(6, 7, 1)),

    keras.layers.Conv2D(32, (3, 3), padding="same", activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu"),

    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(400, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(600, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(600, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(600, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(600, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(600, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(400, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(128, activation="relu"),

    keras.layers.Dense(7, activation="softmax")
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

while True:
    movimiento = 1
    board = tablero_base.copy()
    column = 0
    root = Node(board, 1)

    while True: # comienza la partida: ave cesar, gallina tu madre
        print("\n[+] Partida: " + str(partida))

        if movimiento % 2 == 0:
            player = 2
        else:
            player = 1

        if player == 1:
            print("\n[!] MCTS start")
            MCTS(root, simulations=1000)
            print("[!] MCTS finished")
            column = best_move(root)

            if column is None:
                print("No valid moves available!")
                partida += 1
                break
            else:
                board = place_a_tile(board, column, player)

        else:
            column = random.choice(range(7))
            undescartau = [0, 1, 2, 3, 4, 5, 6]
            while True:
                column = random.choice(undescartau)
                undescartau.remove(column)
                
                if board[0][column] == 0 or undescartau == []:
                    break

            board = place_a_tile(board, column, player)

        if movimiento > 6: # ckeckea si hay 4 en ralla (los primeros 6 movimientos no porque es imposible y asi es un poquito mas eficiente)
            if check_cuatrejo_en_rallejo(board, player, column):
                partida += 1
                break

        movimiento += 1

    if partida % 1000 == 0:
        boards, moves = zip(*[(board, move) for board, move in training_data if move is not None])
        if any(move is not None for _, move in training_data):
            boards, moves = zip(*[(board, move) for board, move in training_data if move is not None])
            boards_np = np.array(boards).reshape(-1, 6, 7, 1)
            moves_np = keras.utils.to_categorical(moves, 7)

            model.fit(boards_np, moves_np, epochs=100, batch_size=32)
            training_data.clear()

            save_network(model, "AlphaFir")
