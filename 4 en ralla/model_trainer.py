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

def check_cuatrejo_en_rallejo(board, player):
    rallitas, columnitas = len(board), len(board[0])

    for row in range(rallitas): # ladajo
        for col in range(columnitas - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(columnitas): # arribajo
        for row in range(rallitas - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(3, rallitas): # diagonal bajorriba
        for col in range(columnitas - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    for row in range(rallitas - 3): # diagonal arribajo
        for col in range(columnitas - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False

partida = 1

while True:
    movimiento = 1
    board = tablero_base.copy()

    while True: # comienza la partida: ave cesar, gallina tu madre
        if movimiento % 2 == 0:
            player = 2
        else:
            player = 1
        
        if movimiento > 6: # ckeckea si hay 4 en ralla (los primeros 6 movimientos no porque es imposible y asi es un poquito mas eficiente)
            if check_cuatrejo_en_rallejo(board, player):
                print("Ganador: " + player)
                break
        
        movimiento += 1
