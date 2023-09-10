import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

filename = input("[-] Filename: ")

def save_network(network, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    save_path = os.path.join(script_dir, 'networks')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    network.save(os.path.join(save_path, filename))
    print("[+] Saved network")

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

while True:
    for i in range(10):
        players_list[i].cards = []
    players = random.randint(2, 10)
    unsafled_cards = []
    for i in range(1, 112+1):
        unsafled_cards.append(i)
    used_cards = []

    for i in range(players):
        players_list[i].playing = True
        for a in range(7):
            card = int(random.choice(unsafled_cards))
            players_list[i].cards.append(card)
            unsafled_cards.remove(card)
            used_cards.append(card)

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
                continue
                
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
                continue

            if posible_cards != []:
                while True:
                    chosed_card = players_list[next_player].choose(posible_cards, last_card, last_card_colour, used_cards, plus2round, plus4round, players_list[next_player].played)
                    
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
                        break
            
            else:
                card = int(random.choice(unsafled_cards))
                players_list[next_player].cards.append(card)
                unsafled_cards.remove(card)
                used_cards.append(card)
            
        if players_list[next_player].cards == []:
            print(f"Play {partida} :   Player {next_player}:    Winner!")   ################# Y ESTA RED SERA LA QUE SE UTILIZARA EN EL ALGORITMO EVOLUTIVO
            finished = True
            winner_network = players_list[next_player].network
            for i in players_list:
                i.played = False
            if partida%10 == 0:
                save_network(winner_network, filename)
            partida += 1

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
