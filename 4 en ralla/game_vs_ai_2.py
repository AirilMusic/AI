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

def evaluate_subset(subset):
    count_player = subset.count(2)
    count_opponent = subset.count(1)

    if count_player and count_opponent:
        return 0

    if count_player == 3:
        return 50
    elif count_player == 2:
        return 10
    elif count_player == 1:
        return 1
    elif count_opponent == 3:
        return -50
    elif count_opponent == 2:
        return -10
    elif count_opponent == 1:
        return -1

    return 0

def evaluate_board(board):
    THREE_IN_ROW = 50
    TWO_IN_ROW = 10
    ONE_IN_ROW = 1

    value = 0

    for row in board:
        for i in range(len(row) - 3):
            subset = row[i:i+4]
            value += evaluate_subset(subset)

    for col in range(len(board[0])):
        column = [board[row][col] for row in range(len(board))]
        for i in range(len(column) - 3):
            subset = column[i:i+4]
            value += evaluate_subset(subset)

    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            subset = [board[row + i][col + i] for i in range(4)]
            value += evaluate_subset(subset)

    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            subset = [board[row - i][col + i] for i in range(4)]
            value += evaluate_subset(subset)

    return value

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or check_cuatrejo_en_rallejo(board, 1, column) or check_cuatrejo_en_rallejo(board, 2, column) or empate(board):
        return evaluate_board(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        for col in range(len(board[0])):
            if board[0][col] == 0:
                temp_board = [row[:] for row in board]
                place_a_tile(temp_board, col, 2)
                eval = minimax(temp_board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(len(board[0])):
            if board[0][col] == 0:
                temp_board = [row[:] for row in board]
                place_a_tile(temp_board, col, 1)
                eval = minimax(temp_board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board):
    depth = 4
    is_maximizing = True
    alpha = float('-inf')
    beta = float('inf')
    best_value = float('-inf')
    best_column = None
    
    for col in range(len(board[0])):
        if board[0][col] == 0:
            temp_board = [row[:] for row in board]
            place_a_tile(temp_board, col, 2)
            move_value = minimax(temp_board, depth-1, alpha, beta, not is_maximizing)
            if move_value > best_value:
                best_value = move_value
                best_column = col
            alpha = max(alpha, move_value)
    return best_column

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
            predicted_move = best_move(board)
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
