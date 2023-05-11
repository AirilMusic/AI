import pygame # para la representacion visual del juego para humanos, para ver lo que hace la IA y en que vuelta va
import random
import time
import copy

import tensorflow as tf
from tensorflow import keras
import numpy as np

# hay comentarios que los he ido poniendo para acordarme de cosas... y no lo he terminado quitando porque me han hecho gracia :3

################################                AI                ################################
def mtx(tablero):
    matrix = []
    for i in tablero:
        line = []
        for a in i:
            if a == 0:
                line.append(a)
            elif a == 8:
                line.append(1)
            else:
                line.append(2)
        line = np.array(line)
        matrix.append(line)
    return matrix

def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(27, 10, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(4, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

model = create_model()

def q_learning_update(model, state, action, reward, next_state, discount_factor):
    q_values = model.predict(state[np.newaxis])
    next_q_values = model.predict(next_state[np.newaxis])
    q_values[0][action] = reward + discount_factor * np.max(next_q_values)
    model.train_on_batch(state[np.newaxis], q_values[np.newaxis])
    return model
    
    
def train(tablero, reward, model):
    matrix = mtx(tablero)
    state = np.array(matrix)
    action_map = {'Abajo': 0, 'Derecha': 1, 'Izquierda': 2, 'Rotar': 3}
    action = action_map[np.random.choice(['Abajo', 'Derecha', 'Izquierda', 'Rotar'])]
    next_state = np.array(tablero)
    discount_factor = 0.99

    model = q_learning_update(model, state, action, reward, next_state, discount_factor)
    
    if action == 0:
        action = "Abajo"
    elif action == 1:
        action = "Derecha"
    elif action == 2:
        action = "Izquierda"
    else:
        action = "Rotar"
        
    return action
################################                AI                ################################

reward = 0
game = 1
 
BLACK = (0, 0, 0)                    # 0
BLUE = (0, 0, 255)                   # 1
ORANGE = (255, 165, 0)               # 2
RED = (255, 0, 0)                    # 3
YELLOW = (255, 255, 0)               # 4
GREEN = (0, 255, 0)                  # 5
DARK_GREEN = (0, 124, 0)             # 6
PURPLE = (128, 0, 128)               # 7
SELECT = (255, 255, 255)             # 8 = pieza controlada
 
pygame.init()
screen = pygame.display.set_mode((200, 600)) # para solo el juego es y = 540
font = pygame.font.Font(None, 25)

speed =  0.00001

def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))

def draw_board(board, game, count):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 0:
                draw_cell(x, y, BLACK)
            elif cell == 1:
                draw_cell(x, y, BLUE)
            elif cell == 2:
                draw_cell(x, y, ORANGE)
            elif cell == 3:
                draw_cell(x, y, RED)
            elif cell == 4:
                draw_cell(x, y, YELLOW)
            elif cell == 5:
                draw_cell(x, y, GREEN)
            elif cell == 6:
                draw_cell(x, y, DARK_GREEN)
            elif cell == 7:
                draw_cell(x, y, PURPLE)
            elif cell == 8:
                draw_cell(x, y, SELECT)
                
    font = pygame.font.Font(None, 35)
    game_text = font.render("Game: " + str(game-1), True, (0, 0, 0))
    score_text = font.render("Score: " + str(count-1), True, (0, 0, 0))
    screen.blit(game_text, (10, 550))
    screen.blit(score_text, (10, 570))
    game_text = font.render("Game: " + str(game), True, (255, 255, 255))
    score_text = font.render("Score: " + str(count), True, (255, 255, 255))
    screen.blit(game_text, (10, 550))
    screen.blit(score_text, (10, 570))
               
def delet_last_text(game, count):
    font = pygame.font.Font(None, 35)
    last_game_text = font.render("Game: " + str(game), True, (0, 0, 0))
    last_score_text = font.render("Score: " + str(count-1), True, (0, 0, 0))
    screen.blit(last_game_text, (10, 550))
    screen.blit(last_score_text, (10, 570))

# Piezas:
#     1       2      3     4      5      6      7
#            
#    ####      #    #      ##     ##    ##      #
#            ###    ###    ##    ##      ##    ###

tablero_base = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # coordenadas: tablero[y[x]]
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # SI ALGUNA PIEZA TOCA ESTA LINEA DESPUES DE HABERSE COLOCADO = GAME OVER, estas dos lineas son como un buffer antes de hacer el primer movimiento
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

tablero = copy.deepcopy(tablero_base)
lty = len(tablero)
ltx = len(tablero[0])

acciones = ("Abajo", "Derecha", "Izquierda", "Rotar")

posicion_pieza = [[0,0], [0,0], [0,0], [0,0]] #[y,x]
rotacion = 0 #0, 1, 2, 3
fliped = False
pieza = 0
count = 0

def clean(tablero, posicion_pieza): # esto es para borrar lo blanco del tablero
    tablero[posicion_pieza[0][0]][posicion_pieza[0][1]] = 0
    tablero[posicion_pieza[1][0]][posicion_pieza[1][1]] = 0
    tablero[posicion_pieza[2][0]][posicion_pieza[2][1]] = 0
    tablero[posicion_pieza[3][0]][posicion_pieza[3][1]] = 0

def mover(lado, posicion_pieza, tablero, pieza, count, rotacion, reward, fliped):
    if lado == "izquierda": 
        if posicion_pieza[0][1] > 0 and posicion_pieza[1][1] > 0 and posicion_pieza[2][1] > 0 and posicion_pieza[3][1] > 0 and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]-1] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]-1] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]-1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]-1] == 8) and (tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 0 or tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][1] -= 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
    
    elif lado == "derecha": 
        if posicion_pieza[0][1] < ltx-1 and posicion_pieza[1][1] < ltx-1 and posicion_pieza[2][1] < ltx-1 and posicion_pieza[3][1] < ltx-1 and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[2][0]][posicion_pieza[2][1]+1] == 0 or tablero[posicion_pieza[2][0]][posicion_pieza[2][1]+1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][1] += 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
    
    elif lado == "abajo":
        if posicion_pieza[0][0] < lty-1 and posicion_pieza[1][0] < lty-1 and posicion_pieza[2][0] < lty-1 and posicion_pieza[3][0] < lty-1 and (tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]] == 0 or tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]] == 8) and (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 8) and (tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 0 or tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][0] += 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
        else:
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = pieza
            posicion_pieza, pieza, rotacion, reward, fliped = nueva_pieza(posicion_pieza, tablero, rotacion, reward, fliped)
            count += 1
                    
    elif lado == "rotar":
        try:
            rotated = False
            if pieza == 1:
                if rotacion == 0 or rotacion == 2:
                    if (posicion_pieza[3][1]+3) < ltx and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+3] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+3] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0], posicion_pieza[3][1]+1]
                        posicion_pieza[1] = [posicion_pieza[3][0], posicion_pieza[3][1]+2]
                        posicion_pieza[2] = [posicion_pieza[3][0], posicion_pieza[3][1]+3]
                        rotated = True
                
                else:
                    if (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]-3][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-3][posicion_pieza[3][1]] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]]
                        posicion_pieza[1] = [posicion_pieza[3][0]-2, posicion_pieza[3][1]]
                        posicion_pieza[2] = [posicion_pieza[3][0]-3, posicion_pieza[3][1]]
                        rotated = True
            
            elif pieza == 2:
                if rotacion == 0:
                    if (posicion_pieza[3][1]+2) < ltx and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8) and (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]+1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0], posicion_pieza[3][1]-1]
                        posicion_pieza[1] = [posicion_pieza[3][0], posicion_pieza[3][1]+1]
                        posicion_pieza[2] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]+1]
                        rotated = True
                
                elif rotacion == 1:
                    if (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8) and (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 8) and (tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0], posicion_pieza[3][1]-1]
                        posicion_pieza[1] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]-1]
                        posicion_pieza[2] = [posicion_pieza[3][0]-2, posicion_pieza[3][1]-1]
                        rotated = True
                
                elif rotacion == 2:
                    if (posicion_pieza[0][1]+2) < ltx and (tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]] == 0 or tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]] == 8) and (tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]+1] == 8) and (tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]+2] == 0 or tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]+2] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[1] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]]
                        posicion_pieza[2] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]+1]
                        posicion_pieza[3] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]+2]
                        rotated = True
                
                else:
                    if (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]]
                        posicion_pieza[1] = [posicion_pieza[3][0]+1, posicion_pieza[3][1]]
                        posicion_pieza[2] = [posicion_pieza[3][0]+1, posicion_pieza[3][1]-1]
                        rotated = True
            
            elif pieza == 3: # en unas baja demas y en otras sube demas, quiero pegarme un tiro
                if rotacion == 0:
                    if fliped == False or posicion_pieza[0][0] == lty-1 or posicion_pieza[1][0] == lty-1 or posicion_pieza[2][0] == lty-1 or posicion_pieza[3][0] == lty-1:
                        if (posicion_pieza[3][1]+2) < ltx and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8):
                            clean(tablero, posicion_pieza)
                            posicion_pieza[1] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]]
                            posicion_pieza[2] = [posicion_pieza[0][0], posicion_pieza[0][1]+1]
                            posicion_pieza[3] = [posicion_pieza[0][0], posicion_pieza[0][1]+2]
                            rotated = True
                    else:
                        if (posicion_pieza[3][1]+2) < ltx and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+2] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8):
                            clean(tablero, posicion_pieza)
                            posicion_pieza[0] = [posicion_pieza[0][0]+1, posicion_pieza[0][1]]
                            posicion_pieza[1] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]]
                            posicion_pieza[2] = [posicion_pieza[0][0], posicion_pieza[0][1]+1]
                            posicion_pieza[3] = [posicion_pieza[0][0], posicion_pieza[0][1]+2]
                            rotated = True                  
                elif rotacion == 1:
                    if (posicion_pieza[0][1]+1) < ltx and (tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]] == 0 or tablero[posicion_pieza[0][0]-1][posicion_pieza[0][1]] == 8) and (tablero[posicion_pieza[0][0]-2][posicion_pieza[0][1]] == 0 or tablero[posicion_pieza[0][0]-2][posicion_pieza[0][1]] == 8) and (tablero[posicion_pieza[0][0]-2][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]-2][posicion_pieza[0][1]+1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[1] = [posicion_pieza[0][0]-1, posicion_pieza[0][1]]
                        posicion_pieza[2] = [posicion_pieza[0][0]-2, posicion_pieza[0][1]]
                        posicion_pieza[3] = [posicion_pieza[0][0]-2, posicion_pieza[0][1]+1]
                        rotated = True
                
                elif rotacion == 2:
                    if (posicion_pieza[1][1]+2) < ltx and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+2] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+2] == 8) and (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+2] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+2] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[1][0], posicion_pieza[1][1]+1]
                        posicion_pieza[2] = [posicion_pieza[1][0], posicion_pieza[1][1]+2]
                        posicion_pieza[3] = [posicion_pieza[1][0]+1, posicion_pieza[1][1]+2]
                        rotated = True
                
                else:
                    if (posicion_pieza[3][1]-1) >= 0 and (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]-2][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]]
                        posicion_pieza[1] = [posicion_pieza[3][0]-2, posicion_pieza[3][1]]
                        posicion_pieza[2] = [posicion_pieza[3][0], posicion_pieza[3][1]-1]
                        rotated = True
            
            elif pieza == 5:
                if rotacion == 0 or rotacion == 2:
                    if (posicion_pieza[1][1]+2) < ltx and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+2] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]+2] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[1][0], posicion_pieza[1][1]+1]
                        posicion_pieza[2] = [posicion_pieza[1][0]+1, posicion_pieza[1][1]+1]
                        posicion_pieza[3] = [posicion_pieza[1][0]+1, posicion_pieza[1][1]+2]
                        rotated = True
                    
                else: # apaño pendiente XD  <-- no funca <-- creo que ya funca
                    if (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]+1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[1][0]+1, posicion_pieza[1][1]]
                        posicion_pieza[2] = [posicion_pieza[1][0], posicion_pieza[1][1]+1]
                        posicion_pieza[3] = [posicion_pieza[1][0]-1, posicion_pieza[1][1]+1]
                        rotated = True
            
            elif pieza == 6:
                if rotacion == 0 or rotacion == 2:
                    if (posicion_pieza[3][1]+1) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0], posicion_pieza[3][1]+1]
                        posicion_pieza[1] = [posicion_pieza[3][0]+1, posicion_pieza[3][1]]
                        posicion_pieza[2] = [posicion_pieza[3][0]+1, posicion_pieza[3][1]-1]
                        rotated = True
                
                else:
                    if (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8) and (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0]+1, posicion_pieza[3][1]]
                        posicion_pieza[1] = [posicion_pieza[3][0], posicion_pieza[3][1]-1]
                        posicion_pieza[2] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]-1]
                        rotated = True
            
            elif pieza == 7:
                if rotacion == 0:
                    if (posicion_pieza[3][1]+1) < ltx and (posicion_pieza[3][1]-2) > 0 and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-2] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-2] == 8) and (tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]-1][posicion_pieza[3][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[3][0], posicion_pieza[3][1]-1]
                        posicion_pieza[1] = [posicion_pieza[3][0], posicion_pieza[3][1]-2]
                        posicion_pieza[2] = [posicion_pieza[3][0]-1, posicion_pieza[3][1]-1]
                        rotated = True
                
                elif rotacion == 1:
                    if (tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]] == 0 or tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]] == 8) and (tablero[posicion_pieza[1][0]-2][posicion_pieza[1][1]] == 0 or tablero[posicion_pieza[1][0]-2][posicion_pieza[1][1]] == 8) and (tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]-1][posicion_pieza[1][1]+1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[1][0]-1, posicion_pieza[1][1]]
                        posicion_pieza[2] = [posicion_pieza[1][0]-2, posicion_pieza[1][1]]
                        posicion_pieza[3] = [posicion_pieza[1][0]-1, posicion_pieza[1][1]-1]
                        rotated = True
                
                elif rotacion == 2:
                    if (posicion_pieza[0][1]+2) < ltx and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 8) and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+2] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+2] == 8) and (tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]+1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[1] = [posicion_pieza[0][0], posicion_pieza[0][1]+1]
                        posicion_pieza[2] = [posicion_pieza[0][0], posicion_pieza[0][1]+2]
                        posicion_pieza[3] = [posicion_pieza[0][0]+1, posicion_pieza[0][1]+1]
                        rotated = True
                
                else:
                    if (tablero[posicion_pieza[2][0]-1][posicion_pieza[2][1]] == 0 or tablero[posicion_pieza[2][0]-1][posicion_pieza[2][1]] == 8) and (tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 0 or tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 8) and (tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 0 or tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 8):
                        clean(tablero, posicion_pieza)
                        posicion_pieza[0] = [posicion_pieza[2][0]-1, posicion_pieza[2][1]]
                        posicion_pieza[1] = [posicion_pieza[2][0]+1, posicion_pieza[2][1]]
                        posicion_pieza[3] = [posicion_pieza[2][0], posicion_pieza[2][1]-1]
                        rotated = True
            
            if rotated == True:
                rotacion += 1
                if rotacion > 3:
                    fliped = True # lo de fliped es para saber si ha dado una vuelta entera, porque la figura 3 da por saco y hace cosas raras y bueno, aunque no funciona del todo soluciona bstantes problemas que da
                    rotacion = 0
            time.sleep(speed)
        except:
            pass
                  
    return posicion_pieza, pieza, count, rotacion, reward, fliped

def destruirLinea(tablero, reward):
    for i in range(lty):
        if 0 not in tablero[i] and 8 not in tablero[i]:
            tablero[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if i != 0: #baja todas las lineas para rellenar la linea borrada
                for a in range(i, 1, -1):
                    tablero[a] = tablero[a-1]
                tablero[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            reward += 10
            break
    return reward

def nueva_pieza(posicion_pieza, tablero, rotacion, reward, fliped):
    reward = destruirLinea(tablero, reward) #para checkear si la vez anterior que se ha puesto una pieza, se ha rellenado alguna linea, y si eso la borra
    pieza = random.randint(1,7) # crea una nueva pieza
    #pieza = 1 # para pruebas 
    if pieza == 1:
        posicion_pieza = [[0,0], [1,0], [2,0], [3,0]]
    elif pieza == 2:
        posicion_pieza = [[0,0], [0,1], [1,1], [2,1]]
    elif pieza == 3:
        posicion_pieza = [[2,0], [0,1], [1,1], [2,1]]
    elif pieza == 4:
        posicion_pieza = [[0,0], [1,0], [0,1], [1,1]]
    elif pieza == 5:
        posicion_pieza = [[1,0], [2,0], [0,1], [1,1]]
    elif pieza == 6:
        posicion_pieza = [[0,0], [1,0], [1,1], [2,1]]
    elif pieza == 7:
        posicion_pieza = [[1,0], [0,1], [1,1], [2,1]]
        
    rotacion = 0
    fliped = False
    
    reward += 1
    
    for i in range(4):
        tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
    return posicion_pieza, pieza, rotacion, reward, fliped

screen.fill((0, 0, 0))
posicion_pieza, pieza, rotacion, reward, fliped = nueva_pieza(posicion_pieza, tablero, rotacion, reward, fliped)
draw_board(tablero, game, count)
pygame.display.flip()
reward = 0
action = train(tablero, reward, model)
while True:
    #inpt = input()
    #inpt = random.choice(acciones) # esto hay que cambiarlo al output de la IA
    inpt = action
    
    if inpt == "Abajo":
        posicion_pieza, pieza, count, rotacion, reward, fliped = mover("abajo", posicion_pieza, tablero, pieza, count, rotacion, reward, fliped)
    elif inpt == "Derecha":
        posicion_pieza, pieza, count, rotacion, reward, fliped = mover("derecha", posicion_pieza, tablero, pieza, count, rotacion, reward, fliped)
    elif inpt == "Izquierda":
        posicion_pieza, pieza, count, rotacion, reward, fliped = mover("izquierda", posicion_pieza, tablero, pieza, count, rotacion, reward, fliped)
    elif inpt == "Rotar":
        posicion_pieza, pieza, count, rotacion, reward, fliped = mover("rotar", posicion_pieza, tablero, pieza, count, rotacion, reward, fliped)
    
    draw_board(tablero, game, count)
    pygame.display.flip()
    delet_last_text(game, count)
    rewarded = False
    for i in range(2):
        for a in tablero[i]:
            if a != 0 and a != 8:
                reward -= 50
                action = train(tablero, reward, model)
                print("Game Over!")
                print("Game:", game, "Score:", count, "Rewards:", reward)
                game += 1
                count, reward = 0, 0
                tablero = copy.deepcopy(tablero_base)
                nueva_pieza(posicion_pieza, tablero, rotacion, reward, fliped)
                draw_board(tablero, game, count)
                pygame.display.flip()
                delet_last_text(game, count)
                rewarded = True
                break
    if rewarded == False:
        action = train(tablero, reward, model)
