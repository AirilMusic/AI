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

def detect_click(pos, player):
    column = pos[0] // 100
    if 600 <= pos[1] <= 650:
        place_a_tile(tablero_base, column, player)

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

tablero_base = [[0, 0, 0, 0, 0, 0, 0],
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
current_player = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > 600:
                detect_click(mouse_pos, current_player)
                current_player = 3 - current_player
    
    screen.fill((0,0,0))
    draw_board(tablero_base)
    pygame.display.flip()
    CLOCK.tick(60)
    
    jugador = random.choice([1,2])

pygame.quit()
