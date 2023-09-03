import random
import pygame
import tensorflow as tf
from tensorflow import keras
import numpy as np
import time

cards = [
    1,   # 0 RED
    2,   # 0 RED
    3,   # 1 RED
    4,   # 1 RED
    5,   # 2 RED
    6,   # 2 RED
    7,   # 3 RED
    8,   # 3 RED
    9,   # 4 RED
    10,  # 4 RED
    11,  # 5 RED
    12,  # 5 RED
    13,  # 6 RED
    14,  # 6 RED
    15,  # 7 RED
    16,  # 7 RED
    17,  # 8 RED
    18,  # 8 RED
    19,  # 9 RED
    20,  # 9 RED
    21,  # 0 YELLOW
    22,  # 0 YELLOW
    23,  # 1 YELLOW
    24,  # 1 YELLOW
    25,  # 2 YELLOW
    26,  # 2 YELLOW
    27,  # 3 YELLOW
    28,  # 3 YELLOW
    29,  # 4 YELLOW
    30,  # 4 YELLOW
    31,  # 5 YELLOW
    32,  # 5 YELLOW
    33,  # 6 YELLOW
    34,  # 6 YELLOW
    35,  # 7 YELLOW
    36,  # 7 YELLOW
    37,  # 8 YELLOW
    38,  # 8 YELLOW
    39,  # 9 YELLOW
    40,  # 9 YELLOW
    41,  # 0 BLUE
    42,  # 0 BLUE
    43,  # 1 BLUE
    44,  # 1 BLUE
    45,  # 2 BLUE
    46,  # 2 BLUE
    47,  # 3 BLUE
    48,  # 3 BLUE
    49,  # 4 BLUE
    50,  # 4 BLUE
    51,  # 5 BLUE
    52,  # 5 BLUE
    53,  # 6 BLUE
    54,  # 6 BLUE
    55,  # 7 BLUE
    56,  # 7 BLUE
    57,  # 8 BLUE
    58,  # 8 BLUE
    59,  # 9 BLUE
    60,  # 9 BLUE
    61,  # 0 GREEN
    62,  # 0 GREEN
    63,  # 1 GREEN
    64,  # 1 GREEN
    65,  # 2 GREEN
    66,  # 2 GREEN
    67,  # 3 GREEN
    68,  # 3 GREEN
    69,  # 4 GREEN
    70,  # 4 GREEN
    71,  # 5 GREEN
    72,  # 5 GREEN
    73,  # 6 GREEN
    74,  # 6 GREEN
    75,  # 7 GREEN
    76,  # 7 GREEN
    77,  # 8 GREEN
    78,  # 8 GREEN
    79,  # 9 GREEN
    80,  # 9 GREEN
    81,  # RED PASS
    82,  # RED PASS
    83,  # GREEN PASS
    84,  # GREEN PASS
    85,  # YELLOW PASS
    86,  # YELLOW PASS
    87,  # BLUE PASS
    88,  # BLUE PASS
    89,  # RED REVERSE
    90,  # RED REVERSE
    91,  # GREEN REVERSE
    92,  # GREEN REVERSE
    93,  # BLUE REVERSE
    94,  # BLUE REVERSE
    95,  # YELLOW REVERSE
    96,  # YELLOW REVERSE
    97,  # RED +2
    98,  # RED +2
    99,  # GREEN +2
    100, # GREEN +2
    101, # YELLOW +2
    102, # YELLOW +2
    103, # BLUE +2
    104, # BLUE +2
    105, # COLOR CHANGE
    106, # COLOR CHANGE
    107, # COLOR CHANGE
    108, # COLOR CHANGE
    109, # COLOR CHANGE +4
    110, # COLOR CHANGE +4
    111, # COLOR CHANGE +4
    112  # COLOR CHANGE +4
]

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

            played = True
        
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
        print("pid:", self.player_id, "pred:", prediction, "cards:", self.cards)
        return posible_cards[prediction.index(max(prediction))]
    
players_list = [Player(i+1) for i in range(10)]

while True:
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

    for i in range(players):
        print("\nPlayer:", players_list[i].player_id)
        print(players_list[i].cards)

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
                        if unsafled_cards != [] :
                            card = int(random.choice(unsafled_cards))
                            players_list[next_player].cards.append(card)
                            unsafled_cards.remove(card)
                            used_cards.append(card)
                
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

            print("[!] pos cards:", posible_cards)
            print("[!] player_cards:", players_list[next_player].cards)

            if posible_cards != []:
                chosed = False
                while True:
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
                            
                            last_card = int(-1) # esto lo deberia utilizar para indicar que se puede utiliar cualquier carta 
                            
                        elif last_card >= 109 and last_card <= 112: # +4 & color change
                            plus4round += 1
                            
                            colors = []
                            for i in players_list[next_player].cards:
                                colors.append(colour(i))
                            last_card_colour = max(colors)
                            
                            last_card = int(-1) # esto lo deberia utilizar para indicar que se puede utiliar cualquier carta    
                        
                        if plus2round > 0:
                            if last_card >= 97 and last_card <= 104:
                                plus2round += 1
                                
                        if plus4round > 0:
                            if last_card >= 109 and last_card <= 112:
                                plus4round += 1
                        
                        break
            
            else:
                print(f"Player {next_player}:    PASS")
                card = int(random.choice(unsafled_cards))
                players_list[next_player].cards.append(card)
                unsafled_cards.remove(card)
                used_cards.append(card)
            
            if players_list[next_player].cards == []:
                print(f"Player {next_player}:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
                finished = True
                winner_network = players_list[next_player].network
                for i in players_list:
                    i.played = False
                partida += 1
                time.sleep(3)

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
                
        print("Last card:", last_card, "Player:", next_player)
        print("[-] cards:", players_list[next_player].cards)
