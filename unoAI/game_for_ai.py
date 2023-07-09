import random
import pygame

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

while True:
    if players_list[0].cards != [] and players_list[0].playing == True:
        posible_cards = []
        for i in players_list[0].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 1:    PASS")
        
        if players_list[0].cards == []:
            print("Player 1:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[1].cards != [] and players_list[1].playing == True:
        posible_cards = []
        for i in players_list[1].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 2:    PASS")
        
        if players_list[1].cards == []:
            print("Player 2:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[2].cards != [] and players_list[2].playing == True:
        posible_cards = []
        for i in players_list[2].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 3:    PASS")
        
        if players_list[2].cards == []:
            print("Player 3:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[3].cards != [] and players_list[3].playing == True:
        posible_cards = []
        for i in players_list[3].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 4:    PASS")
        
        if players_list[3].cards == []:
            print("Player 4:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[4].cards != [] and players_list[4].playing == True:
        posible_cards = []
        for i in players_list[4].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 5:    PASS")
        
        if players_list[4].cards == []:
            print("Player 5:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO

    if players_list[5].cards != [] and players_list[5].playing == True:
        posible_cards = []
        for i in players_list[5].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 6:    PASS")
        
        if players_list[5].cards == []:
            print("Player 6:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[6].cards != [] and players_list[6].playing == True:
        posible_cards = []
        for i in players_list[6].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 7:    PASS")
        
        if players_list[6].cards == []:
            print("Player 7:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[7].cards != [] and players_list[7].playing == True:
        posible_cards = []
        for i in players_list[7].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 8:    PASS")
        
        if players_list[7].cards == []:
            print("Player 8:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[8].cards != [] and players_list[8].playing == True:
        posible_cards = []
        for i in players_list[8].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 9:    PASS")
        
        if players_list[8].cards == []:
            print("Player 9:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
    
    if players_list[9].cards != [] and players_list[9].playing == True:
        posible_cards = []
        for i in players_list[9].cards:
            if colour(i) == last_card_colour or colour(i) == 0:
                posible_cards.append(i)
                
        if posible_cards != []:
            pass     #################### Y AQUI ELIGE LA IA
        
        
        
        else:
            print("Player 10:    PASS")
        
        if players_list[9].cards == []:
            print("Player 10:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
