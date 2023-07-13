import random
import pygame
import tensorflow as tf
from tensorflow import keras
import numpy as np

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
            layer.kernel.initializer.run(session=tf.compat.v1.keras.backend.get_session())
        if hasattr(layer, 'bias_initializer'):
            layer.bias.initializer.run(session=tf.compat.v1.keras.backend.get_session())

def first_network():
    model = keras.Sequential()
    model.add(keras.layers.Dense(random.randint(1, 2000), activation='relu', input_shape=(228))) # esta capa es la primera y la segunda y van por cojones, el numero de las otras capas ocultas puede salirme del coño si quiero
                    
    for i in range(1, 500):
        model.add(keras.layers.Dense(random.randint(1, 2000), activation='relu'))

    randomize_weights(model)

    return model

partida = 1

while True:
    players_list = []

    for i in range(10):
        class player():
            player_id = i+1 # esto realmente no es necesario porque es la posicion del array + 1, pero bueno, si no lo utilizo lo quitare
            cards = []
            used_cards = []
            playing = False
            
            network = None
            
            def choose(posible_cards, last_card, colour, used_cards, plus2, plus4): # y aqui la red que elija la carta
                if partida == 1: # genera la red de forma aleatoria
                    network = first_network()
                    network.add(keras.layers.Dense(len(posible_cards), activation='softmax')) # y esta es la capa de salida que tambien la tengo que poner por cojones
                    
                else: # copia la red ganadora pero le hace un 20% de modificaciones
                    pass
                
                return network.predict()
            
        players_list.append(player)
        
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
            unsafled_cards.remove(card)

    for i in range(players):
        print("\nPlayer:", players_list[i].player_id)
        print(players_list[i].cards)

    init_card = random.choice(unsafled_cards)
    used_cards.append(card)
    unsafled_cards.remove(card)

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
        if next_player > 9:
            next_player = 0    
            
        if players_list[next_player].cards != [] and players_list[next_player].playing == True:
            posible_cards = []
            if last_card < 97 or last_card > 104 or last_card < 109 or last_card > 112: # esto es para que no sea +2 o +4
                for i in players_list[next_player].cards:
                    if colour(i) == last_card_colour or colour(i) == 0 or ((i + 20) == last_card and (i + 20) <= 80) or ((i + 40) == last_card and (i + 40) <= 80) or ((i + 60) == last_card and (i + 60) <= 80) or ((i + 80) == last_card and (i + 80) <= 80) or ((i - 20) == last_card and (i - 20) >= 1) or ((i - 40) == last_card and (i - 40) >= 1) or ((i - 60) == last_card and (i - 60) >= 1) or ((i - 80) == last_card and (i - 80) >= 1):
                        posible_cards.append(i)
            elif last_card >= 97 and last_card <= 104: # +2
                for i in players_list[next_player].cards:
                    if last_card >= 97 and last_card <= 104:
                        posible_cards.append(i)
                if posible_cards == []:
                    for i in range(2):
                        if unsafled_cards != []:
                            card = int(random.choice(unsafled_cards))
                            players_list[next_player].cards.append(card)
                            unsafled_cards.remove(card)
                            used_cards.append(card)
                            unsafled_cards.remove(card)
                
            elif last_card >= 109 and last_card <= 112: # +4
                for i in players_list[next_player].cards:
                    if last_card >= 109 and last_card <= 112:
                        posible_cards.append(i)
                if posible_cards == []:
                    for i in range(4):
                        if unsafled_cards != []:
                            card = int(random.choice(unsafled_cards))
                            players_list[next_player].cards.append(card)
                            unsafled_cards.remove(card)
                            used_cards.append(card)
                            unsafled_cards.remove(card)
                        
            if posible_cards != []:
                chosed = False
                while True:
                    chosed_card, color2change = players_list[next_player].choose(posible_cards, last_card, last_card_colour, used_cards, plus2round, plus4round)
                    unsafled_cards -= 1
                    used_cards.append(chosed_card)
                    last_card = chosed_card
                    last_card_colour = colour(last_card)

                    posible_cards.remove(chosed_card)
                    used_cards.append(chosed_card)
                    
                    if chosed_card != 1000:
                        chosed = True
    
                    if chosed_card == 1000 and chosed == True:
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
                            last_card_colour = color2change
                            last_card = int(-1) # esto lo deberia utilizar para indicar que se puede utiliar cualquier carta 
                            
                        elif last_card >= 109 and last_card <= 112: # +4 & color change
                            plus4round += 1
                            last_card_colour = color2change
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
            
            if players_list[next_player].cards == []:
                print(f"Player {next_player}:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
                finished = True
                
        if player_move_foward:
            next_player += 1
            if next_player > players - 1:
                next_player = 0
                
        else:
            next_player -= 1
            if next_player < 0:
                next_player = players - 1
