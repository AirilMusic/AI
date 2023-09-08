##################### TO DO LIST ####################
#
#   Al ejecutar el script que de dos opciones, cargar modelo o correr desde 0
#
#####################################################

import random
import pygame
import sys
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import time

script_dir = os.path.dirname(os.path.abspath(__file__))

pygame.init()
size = (900, 530)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont(None, 36)

def que_no_pete_al_clicar_fuera():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

cards = {
    1 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\0.jpg')), (40, 80)),   # 0 RED
    2 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\0.jpg')), (40, 80)),   # 0 RED
    3 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\1.jpg')), (40, 80)),   # 1 RED
    4 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\1.jpg')), (40, 80)),   # 1 RED
    5 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\2.jpg')), (40, 80)),   # 2 RED
    6 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\2.jpg')), (40, 80)),   # 2 RED
    7 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\3.jpg')), (40, 80)),   # 3 RED
    8 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\3.jpg')), (40, 80)),   # 3 RED
    9 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\4.jpg')), (40, 80)),   # 4 RED
    10 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\4.jpg')), (40, 80)),  # 4 RED
    11 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\5.jpg')), (40, 80)),  # 5 RED
    12 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\5.jpg')), (40, 80)),  # 5 RED
    13 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\6.jpg')), (40, 80)),  # 6 RED
    14 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\6.jpg')), (40, 80)),  # 6 RED
    15 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\7.jpg')), (40, 80)),  # 7 RED
    16 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\7.jpg')), (40, 80)),  # 7 RED
    17 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\8.jpg')), (40, 80)),  # 8 RED
    18 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\8.jpg')), (40, 80)),  # 8 RED
    19 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\9.jpg')), (40, 80)),  # 9 RED
    20 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\9.jpg')), (40, 80)),  # 9 RED
    21 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\0.jpg')), (40, 80)),  # 0 YELLOW
    22 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\0.jpg')), (40, 80)),  # 0 YELLOW
    23 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\1.jpg')), (40, 80)),  # 1 YELLOW
    24 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\1.jpg')), (40, 80)),  # 1 YELLOW
    25 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\2.jpg')), (40, 80)),  # 2 YELLOW
    26 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\2.jpg')), (40, 80)),  # 2 YELLOW
    27 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\3.jpg')), (40, 80)),  # 3 YELLOW
    28 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\3.jpg')), (40, 80)),  # 3 YELLOW
    29 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\4.jpg')), (40, 80)),  # 4 YELLOW
    30 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\4.jpg')), (40, 80)),  # 4 YELLOW
    31 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\5.jpg')), (40, 80)),  # 5 YELLOW
    32 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\5.jpg')), (40, 80)),  # 5 YELLOW
    33 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\6.jpg')), (40, 80)),  # 6 YELLOW
    34 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\6.jpg')), (40, 80)),  # 6 YELLOW
    35 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\7.jpg')), (40, 80)),  # 7 YELLOW
    36 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\7.jpg')), (40, 80)),  # 7 YELLOW
    37 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\8.jpg')), (40, 80)),  # 8 YELLOW
    38 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\8.jpg')), (40, 80)),  # 8 YELLOW
    39 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\9.jpg')), (40, 80)),  # 9 YELLOW
    40 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\9.jpg')), (40, 80)),  # 9 YELLOW
    41 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\0.jpg')), (40, 80)),  # 0 BLUE
    42 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\0.jpg')), (40, 80)),  # 0 BLUE
    43 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\1.jpg')), (40, 80)),  # 1 BLUE
    44 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\1.jpg')), (40, 80)),  # 1 BLUE
    45 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\2.jpg')), (40, 80)),  # 2 BLUE
    46 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\2.jpg')), (40, 80)),  # 2 BLUE
    47 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\3.jpg')), (40, 80)),  # 3 BLUE
    48 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\3.jpg')), (40, 80)),  # 3 BLUE
    49 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\4.jpg')), (40, 80)),  # 4 BLUE
    50 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\4.jpg')), (40, 80)),  # 4 BLUE
    51 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\5.jpg')), (40, 80)),  # 5 BLUE
    52 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\5.jpg')), (40, 80)),  # 5 BLUE
    53 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\6.jpg')), (40, 80)),  # 6 BLUE
    54 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\6.jpg')), (40, 80)),  # 6 BLUE
    55 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\7.jpg')), (40, 80)),  # 7 BLUE
    56 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\7.jpg')), (40, 80)),  # 7 BLUE
    57 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\8.jpg')), (40, 80)),  # 8 BLUE
    58 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\8.jpg')), (40, 80)),  # 8 BLUE
    59 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\9.jpg')), (40, 80)),  # 9 BLUE
    60 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\9.jpg')), (40, 80)),  # 9 BLUE
    61 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\0.jpg')), (40, 80)),  # 0 GREEN
    62 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\0.jpg')), (40, 80)),  # 0 GREEN
    63 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\1.jpg')), (40, 80)),  # 1 GREEN
    64 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\1.jpg')), (40, 80)),  # 1 GREEN
    65 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\2.jpg')), (40, 80)),  # 2 GREEN
    66 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\2.jpg')), (40, 80)),  # 2 GREEN
    67 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\3.jpg')), (40, 80)),  # 3 GREEN
    68 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\3.jpg')), (40, 80)),  # 3 GREEN
    69 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\4.jpg')), (40, 80)),  # 4 GREEN
    70 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\4.jpg')), (40, 80)),  # 4 GREEN
    71 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\5.jpg')), (40, 80)),  # 5 GREEN
    72 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\5.jpg')), (40, 80)),  # 5 GREEN
    73 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\6.jpg')), (40, 80)),  # 6 GREEN
    74 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\6.jpg')), (40, 80)),  # 6 GREEN
    75 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\7.jpg')), (40, 80)),  # 7 GREEN
    76 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\7.jpg')), (40, 80)),  # 7 GREEN
    77 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\8.jpg')), (40, 80)),  # 8 GREEN
    78 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\8.jpg')), (40, 80)),  # 8 GREEN
    79 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\9.jpg')), (40, 80)),  # 9 GREEN
    80 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\9.jpg')), (40, 80)),  # 9 GREEN
    81 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\pass.jpg')), (40, 80)),  # RED PASS
    82 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\pass.jpg')), (40, 80)),  # RED PASS
    83 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\pass.jpg')), (40, 80)),  # GREEN PASS
    84 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\pass.jpg')), (40, 80)),  # GREEN PASS
    85 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\pass.jpg')), (40, 80)),  # YELLOW PASS
    86 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\pass.jpg')), (40, 80)),  # YELLOW PASS
    87 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\pass.jpg')), (40, 80)),  # BLUE PASS
    88 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\pass.jpg')), (40, 80)),  # BLUE PASS
    89 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\reverse.jpg')), (40, 80)),  # RED REVERSE
    90 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\reverse.jpg')), (40, 80)),  # RED REVERSE
    91 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\reverse.jpg')), (40, 80)),  # GREEN REVERSE
    92 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\reverse.jpg')), (40, 80)),  # GREEN REVERSE
    93 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\reverse.jpg')), (40, 80)),  # BLUE REVERSE
    94 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\reverse.jpg')), (40, 80)),  # BLUE REVERSE
    95 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\reverse.jpg')), (40, 80)),  # YELLOW REVERSE
    96 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\reverse.jpg')), (40, 80)),  # YELLOW REVERSE
    97 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\+2.jpg')), (40, 80)),  # RED +2
    98 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\red\\+2.jpg')), (40, 80)),  # RED +2
    99 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\+2.jpg')), (40, 80)),  # GREEN +2
    100 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\green\\+2.jpg')), (40, 80)), # GREEN +2
    101 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\+2.jpg')), (40, 80)), # YELLOW +2
    102 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\yellow\\+2.jpg')), (40, 80)), # YELLOW +2
    103 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\+2.jpg')), (40, 80)), # BLUE +2
    104 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\blue\\+2.jpg')), (40, 80)), # BLUE +2
    105 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\color_change.jpg')), (40, 80)), # COLOR CHANGE
    106 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\color_change.jpg')), (40, 80)), # COLOR CHANGE
    107 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\color_change.jpg')), (40, 80)), # COLOR CHANGE
    108 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\color_change.jpg')), (40, 80)), # COLOR CHANGE
    109 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\+4.jpg')), (40, 80)), # COLOR CHANGE +4
    110 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\+4.jpg')), (40, 80)), # COLOR CHANGE +4
    111 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\+4.jpg')), (40, 80)), # COLOR CHANGE +4
    112 : pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\color_change\\+4.jpg')), (40, 80))  # COLOR CHANGE +4
}

tamaño_cartas_jugadores = (40, 80)

def colour(card):
        if (card >= 1 and card <= 20) or card == 81 or card == 82 or card == 89 or card == 90 or card == 97 or card == 98:
            return 1 # RED
        elif (card > 20 and card <= 40) or card == 85 or card == 86 or card == 95 or card == 96 or card == 101 or card == 102:
            return 2 # YELLOW
        elif (card > 40 and card <= 60) or card == 87 or card == 88 or card == 93 or card == 94 or card == 103 or card == 104:
            return 3 # BLUE
        elif (card > 60 and card <= 80) or card == 83 or card == 84 or card == 91 or card == 92 or card == 99 or card == 100:
            return 4 # GREEN
        else:
            return 0 # COLOR CHANGE

def randomize_weights(model):
    for layer in model.layers:
        if hasattr(layer, 'kernel_initializer'):
            weights = layer.get_weights()
            weights = [np.random.random_sample(w.shape) for w in weights]
            layer.set_weights(weights)
    return model

def first_network():
    model = keras.Sequential()
    model.add(keras.layers.Dense(random.randint(1, 1000), activation='relu', input_shape=(228,)))
    for i in range(1, random.randint(10, 500)):
        model.add(keras.layers.Dense(random.randint(1, 1000), activation='relu'))
    model = randomize_weights(model)
    return model

partida = 1
winner_network = None

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []
        self.used_cards = []
        self.playing = False
        self.played = False
        self.network = None
    
    def choose(self, posible_cards, last_card, colour, used_cards, plus2, plus4, played):
        if partida == 1 and self.played == False:
            self.network = first_network()
            self.played = True
        
        elif played == False: # copia la red ganadora pero les hace modificaciones
            self.network = winner_network
            
            if self.player_id != 1: # la primera red la deja como la ganadora, las demas tienen una probabilidad de mutar
                for layer in self.network.layers:
                    if hasattr(layer, 'kernel_initializer') and random.randint(1, 10) == 1: # 10% de probabilidades de que una capa cambie sus pesos
                        weights = layer.get_weights()
                        weights = [np.random.random_sample(w.shape) for w in weights]
                        layer.set_weights(weights)
                
                if random.randint(1, 10) == 1: # 10% de probabilidades de que se le quiten capas
                    n_layers = len(self.network.layers)
                    for i in range(random.randint(1, int(n_layers/2))):
                        self.network.pop()

                if random.randint(1, 10) == 1: # 10% de probabilidades de que se le añadadan capas nuevas
                    self.network.pop() # se le quita la capa de salida

                    for i in range(1, random.randint(1, 100)):
                        self.network.add(keras.layers.Dense(random.randint(1, 1000), activation='relu'))

                    self.network.add(keras.layers.Dense(2, activation='softmax')) # capa de salida placeholder

            self.played = True
        
        self.network.pop()
        self.network.add(keras.layers.Dense(len(posible_cards), activation='softmax')) # y esta es la capa de salida que se actualiza al numero de cartas que se pueden jugar
        output_layer = self.network.layers[-1]
        weights = output_layer.get_weights()
        for i in range(len(weights)):
            weights[i].fill(0.5)
        output_layer.set_weights(weights)

        # tengo que traducir los datos a las 228 neuronas
        input_neurons = []
        for i in range(228):
            input_neurons.append(0)
        
        # 112 neuronas de 0 o 1 dependiendo si esa carta la tiene el jugador o no
        for i in posible_cards:
            input_neurons[i-1] = 1
            
        # last card & colour
        input_neurons[112], input_neurons[113] = last_card, colour
        
        # 112 neuronas de las cartas usadas, si esta usada 1 y sino 0
        for i in used_cards:
            input_neurons[i + 112] = 1
        
        # +2 & +4
        input_neurons[226], input_neurons[227] = plus2, plus4
        prediction = list(self.network.predict(np.array([input_neurons], dtype=int)))
        return posible_cards[prediction.index(max(prediction))]
    
players_list = [Player(i+1) for i in range(10)]

back_side = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\back.PNG')), (60, 120))
screen.blit(back_side, (420, 100))

players_place_holders = {
    0 : (10, 50),
    1 : (850, 50),
    2 : (10, 140),
    3 : (850, 140),
    4 : (10, 230),
    5 : (850, 230),
    6 : (10, 320),
    7 : (850, 320),
    8 : (10, 410),
    9 : (850, 410)
}

def show_cards(player, last_card):
    if player%2 == 0:
        for i in range(25):
            x = players_place_holders[player][0] - 5 + (i * 20)
            y = players_place_holders[player][1] - 5
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 50, 90))

        for i in range(len(players_list[player].cards)):
            x = players_place_holders[player][0] + (i * 20)
            y = players_place_holders[player][1]
            back_side = pygame.transform.scale(cards[players_list[player].cards[i]], (40, 80))
            screen.blit(back_side, (x, y))
    else:
        for i in range(25):
            x = players_place_holders[player][0] - 5 - (i * 20)
            y = players_place_holders[player][1] - 5
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 50, 90))

        for i in range(len(players_list[player].cards)):
            x = players_place_holders[player][0] - (i * 20)
            y = players_place_holders[player][1]
            back_side = pygame.transform.scale(cards[players_list[player].cards[i]], (40, 80))
            screen.blit(back_side, (x, y))

    lc = pygame.transform.scale(cards[last_card], (60, 120))
    screen.blit(lc, (420, 300))
    back_side = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\back.PNG')), (60, 120))
    screen.blit(back_side, (420, 100))
    pygame.display.flip()

animation_speed = 7

def move_new_card(player, last_card):
    new_card_1 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\back.PNG')), (60, 120))
    
    x_diff = players_place_holders[player][0] - 420
    y_diff = players_place_holders[player][1] - 100

    total_steps = int(abs(x_diff) / animation_speed)

    for i in range(total_steps):
        x_step = (x_diff / total_steps) * i
        y_step = (y_diff / total_steps) * i

        x2 = 420 + x_step
        y2 = 100 + y_step

        screen.blit(new_card_1, (x2, y2))

        pygame.display.flip()
        pygame.time.Clock().tick(800)

        pygame.draw.rect(screen, (0, 0, 0), (x2, y2, 60, 120))
        back_side = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,'assets\\back.PNG')), (60, 120))
        screen.blit(back_side, (420, 100))

    for i in range(10):
        show_cards(i, last_card)

while True:
    for i in range(10):
        players_list[i].cards = []
    texto = font.render(f"Partida: {partida-1}", True, (0, 0, 0))
    screen.blit(texto, (10, 10))
    texto = font.render(f"Partida: {partida}", True, (255, 255, 255))
    screen.blit(texto, (10, 10))

    players = random.randint(2, 10)
    unsafled_cards = []
    for i in range(1, 112+1):
        unsafled_cards.append(i)
    used_cards = []
    tota_cards = 112 #esto no hay que cambiarlo, es por si necesito saber cuanto es el total y no tener que hacer len(), para reducir el numero de operaciones

    for i in range(players):
        players_list[i].playing = True
        for a in range(7):
            card = int(random.choice(unsafled_cards))
            players_list[i].cards.append(card)
            unsafled_cards.remove(card)
            used_cards.append(card)
        
    for i in range(10):
        show_cards(i, 1)

    init_card = random.choice(unsafled_cards)
    used_cards.append(init_card)
    unsafled_cards.remove(init_card)

    plus2round = 0
    plus4round = 0

    last_card = init_card
    last_card_colour = colour(last_card)

    next_player = 0
    player_move_foward = True # si es false es porque al haber cambio de sentido va para a tras

    finished = False

    while finished == False:
        lc = pygame.transform.scale(cards[last_card], (60, 120))
        screen.blit(lc, (420, 300))
        que_no_pete_al_clicar_fuera()

        if next_player < 0:
            next_player = players - 1
        if next_player > players-1:
            next_player = 0    

        if players_list[next_player].cards != [] and players_list[next_player].playing == True:
            posible_cards = []
            if last_card < 97 or last_card > 104 or last_card < 109 or last_card > 112: # esto es para que no sea +2 o +4
                for i in players_list[next_player].cards:
                    if colour(i) == last_card_colour or colour(i) == 0 or ((i + 20) == last_card and (i + 20) <= 80) or ((i + 40) == last_card and (i + 40) <= 80) or ((i + 60) == last_card and (i + 60) <= 80) or ((i + 80) == last_card and (i + 80) <= 80) or ((i - 20) == last_card and (i - 20) >= 1) or ((i - 40) == last_card and (i - 40) >= 1) or ((i - 60) == last_card and (i - 60) >= 1) or ((i - 80) == last_card and (i - 80) >= 1):
                        posible_cards.append(i)
                        
            elif last_card >= 97 and last_card <= 104: # +2
                for i in players_list[next_player].cards:
                    if i >= 97 and i <= 104:
                        posible_cards.append(i)
                        
                if posible_cards == []:
                    for i in range(2):
                        if unsafled_cards != []:
                            card = int(random.choice(unsafled_cards))
                            players_list[next_player].cards.append(card)
                            unsafled_cards.remove(card)
                            used_cards.append(card)
                            move_new_card(next_player, last_card)
                
            elif last_card >= 109 and last_card <= 112: # +4
                for i in players_list[next_player].cards:
                    if i >= 109 and i <= 112:
                        posible_cards.append(i)
                        
                if posible_cards == []:
                    for i in range(4):
                        if unsafled_cards != []:
                            card = int(random.choice(unsafled_cards))
                            players_list[next_player].cards.append(card)
                            unsafled_cards.remove(card)
                            used_cards.append(card)
                            move_new_card(next_player, last_card)

            print("[!] Player:", next_player)
            print("[!] player_cards:", players_list[next_player].cards)

            if posible_cards != []:
                while True:
                    lc = pygame.transform.scale(cards[last_card], (60, 120))
                    screen.blit(lc, (420, 300))
                    chosed_card = players_list[next_player].choose(posible_cards, last_card, last_card_colour, used_cards, plus2round, plus4round, players_list[next_player].played)
                    
                    print("\nCHOSED CARD:", chosed_card)
                    
                    for i in posible_cards:
                        if colour(i) != colour(chosed_card):
                            posible_cards.remove(i)

                    used_cards.append(chosed_card)
                    posible_cards.remove(chosed_card)
                    players_list[next_player].cards.remove(chosed_card)
                    
                    last_card = chosed_card
                    last_card_colour = colour(last_card)

                    if posible_cards == []:
                        if last_card >= 81 and last_card <= 88: # SALTO
                            if player_move_foward:
                                next_player += 1
                                if next_player > players - 1:
                                    next_player = 0
                            
                            else:
                                next_player -= 1
                                if next_player < 0:
                                    next_player = players - 1
                        
                        elif last_card >= 89 and last_card <= 96: # REVERSE
                            if player_move_foward:
                                player_move_foward = False

                            else:
                                player_move_foward = True
                        
                        elif last_card >= 97 and last_card <= 104: # +2
                            plus2round += 1
                            
                        elif last_card >= 105 and last_card <= 108: # COLOR CHANGE
                            colors = []
                            for i in players_list[next_player].cards:
                                colors.append(colour(i))
                            if colors != []:
                                last_card_colour = max(colors)
                            
                        elif last_card >= 109 and last_card <= 112: # +4 & color change
                            plus4round += 1
                            
                            colors = []
                            for i in players_list[next_player].cards:
                                try: # sin este try ni el siguiente peta si hay cambio de color, porque no es un color especifico
                                    colors.append(colour(i))
                                except:
                                    pass
                            try:
                                last_card_colour = max(colors)
                            except:
                                pass 
                        
                        if plus2round > 0:
                            if last_card >= 97 and last_card <= 104:
                                plus2round += 1
                                
                        if plus4round > 0:
                            if last_card >= 109 and last_card <= 112:
                                plus4round += 1

                        show_cards(next_player, last_card)
                        break
            
            else:
                print(f"Player {next_player}:    PASS")
                card = int(random.choice(unsafled_cards))
                players_list[next_player].cards.append(card)
                unsafled_cards.remove(card)
                used_cards.append(card)
                move_new_card(next_player, last_card)
            
        if players_list[next_player].cards == []:
            print(f"Player {next_player}:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
            show_cards(next_player, last_card)
            finished = True
            winner_network = players_list[next_player].network
            for i in players_list:
                i.played = False
            partida += 1
            time.sleep(5)

        if player_move_foward:
            next_player += 1
            if next_player > players - 1:
                next_player = 0
                
        else:
            next_player -= 1
            if next_player < 0:
                next_player = players - 1
            
        if unsafled_cards == []: # si la baraja se queda sin cartas
            for i in used_cards:
                unsafled_cards.append(i)
                used_cards.remove(i)
