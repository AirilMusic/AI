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

players_list = []

for i in range(10):
    class player():
        player_id = i+1 # esto realmente no es necesario porque es la posicion del array + 1, pero bueno, si no lo utilizo lo quitare
        cards = []
        used_cards = []
        playing = False
        
        def choose(posible_cards, last_card, colour, used_cards, plus2, plus4): # y aqui la red que elija la carta
            pass
        
        
    players_list.append(player)
    
players = random.randint(2, 10)
unsafled_cards = 112
used_cards = []
tota_cards = 112 #esto no hay que cambiarlo, es por si necesito saber cuanto es el total y no tener que hacer len(), para reducir el numero de operaciones

for i in range(players):
    players_list[i].playing = True
    for a in range(7):
        card = int(random.randint(1, unsafled_cards))
        players_list[i].cards.append(random.choice(cards))
        unsafled_cards -= 1
        used_cards.append(card)
        cards.remove(cards[card])

for i in range(players):
    print("\nPlayer:", players_list[i].player_id)
    print(players_list[i].cards)

init_card = random.randint(1, unsafled_cards)
unsafled_cards -= 1
used_cards.append(card)
cards.remove(cards[card])

plus2round = 0
plus4round = 0

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

last_card = init_card
last_card_colour = colour(last_card)

next_player = 0
player_move_foward = True # si es false es porque al haber cambio de sentido va para a tras

while True:
    if next_player < 0:
        next_player = players - 1
    if next_player > 9:
        next_player = 0    
        
    if players_list[next_player].cards != [] and players_list[next_player].playing == True:
        posible_cards = []
        for i in players_list[next_player].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            chosed_card, color2change = players_list[next_player].choose(posible_cards, last_card, last_card_colour, used_cards, plus2round, plus4round)
            unsafled_cards -= 1
            used_cards.append(chosed_card)
            last_card = chosed_card
            last_card_colour = colour(last_card)

            if last_card >= 81 and last_card <= 88: # SALTO
                pass
            
            elif last_card >= 89 and last_card <= 96: # REVERSE
                pass
            
            elif last_card >= 97 and last_card <= 104: # +2
                plus2round += 1
                
            
        
        
        else:
            print(f"Player {next_player}:    PASS")
        
        if players_list[next_player].cards == []:
            print(f"Player {next_player}:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
            
    if player_move_foward:
        next_player += 1
    else:
        next_player -= 1
