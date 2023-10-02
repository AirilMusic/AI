# AlphaFir (Alpha Four In Row)
# Made by Airil/Ainhoa and IA based on AlphaZero algorithm

import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import pygame
import time

pygame.init()
WIDTH, HEIGHT = 700, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('4 en ralla')
CLOCK = pygame.time.Clock()

def draw_board(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            pygame.draw.rect(screen, (50,50,50), (col*100, row*100, 100, 100))
            pygame.draw.line(screen, (0,0,0), (col*100, row*100), ((col+1)*100, row*100), 3)
            pygame.draw.line(screen, (0,0,0), (col*100, row*100), (col*100, (row+1)*100), 3)
            if board[row][col] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (int(col*100 + 50), int(row*100 + 50)), 40)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, (0, 0, 255), (int(col*100 + 50), int(row*100 + 50)), 40)
    
    for col in range(len(board[0])):
        pygame.draw.rect(screen, (145, 244, 237), (col*100, 600, 100, 50))
        pygame.draw.rect(screen, (0,0,0), (col*100, 600, 100, 50), 2)

column = 0
predicted_move = 0

def detect_click(pos, player):
    global column
    column = pos[0] // 100
    if 600 <= pos[1] <= 650 and board[0][column] == 0:
        place_a_tile(board, column, player)
        return True
    return False

def load_network():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'networks')
    model_path = os.path.join(save_path, "AlphaFir")
    
    if os.path.exists(model_path):
        loaded_model = keras.models.load_model(model_path)
        print("[+] Loaded network from", model_path)
        return loaded_model
    else:
        print("[-] Model not found at", model_path)
        return None

def predict_move(board, model):
    board_np = np.array(board).reshape(1, 6, 7, 1)
    
    predictions = model.predict(board_np)[0]
    best_move = np.argmax(predictions)

    while board[0][best_move] != 0:
        predictions[best_move] = -1
        best_move = np.argmax(predictions)

    return best_move

board = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]

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

def empate(board):
    for columna in board:
        if 0 in columna:
            return False
    return True

model = load_network()

running = True

while True:
    board = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    
    jugador_precoz = random.choice([1,2]) # jeje no dura ni 10 segundos
    screen.fill((0,0,0))
    draw_board(board)
    pygame.display.flip()

    while running:
        column = predicted_move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and jugador_precoz == 1:
                mouse_pos = pygame.mouse.get_pos()
                if detect_click(mouse_pos, jugador_precoz):
                    jugador_precoz = 3 - jugador_precoz
                    screen.fill((0,0,0))
                    draw_board(board)
                    pygame.display.flip()
                    time.sleep(random.choice([0.3, 0.5, 0.7, 0.1, 0.8, 1.2, 0.4]))

        if check_cuatrejo_en_rallejo(board, 1, column) or empate(board):
            time.sleep(5)
            break

        if jugador_precoz == 2:  # IA
            predicted_move = predict_move(board, model)
            place_a_tile(board, predicted_move, jugador_precoz)
            time.sleep(1)
            jugador_precoz = 3 - jugador_precoz

        screen.fill((0,0,0))
        draw_board(board)
        pygame.display.flip()
        CLOCK.tick(60)

        if check_cuatrejo_en_rallejo(board, 2, predicted_move) or empate(board):
            time.sleep(5)
            break
