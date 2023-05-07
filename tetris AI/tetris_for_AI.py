import pygame # para la representacion visual del juego para humanos, para ver lo que hace la IA y en que vuelta va
import random
import time
import copy

reward = 0
alfa = 0.25 # valor de aprendizaje/modificacion en machine learning
ganma = 0.8 # si es proximo a 0 busca recompensas a corto plazo, y si es cercano a 1 las busca a largo plazo

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
screen = pygame.display.set_mode((200, 540))

speed = 0.00001

def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))

def draw_board(board):
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

# Piezas:
#     1       2      3     4      5      6      7
#            
#    ####     #       #    ##     ##    ##      #
#             ###   ###    ##    ##      ##    ###

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

posicion_pieza = [[0,0], [0,0], [0,0], [0,0]] #[y,x]
rotacion = 0 #0, 1, 2, 3
pieza = 0
count = 0

def mover(lado, posicion_pieza, tablero, pieza, count, rotacion, reward):
    if lado == "izquierda": 
        if posicion_pieza[0][1] != 0 and posicion_pieza[1][1] != 0 and posicion_pieza[2][1] != 0 and posicion_pieza[3][1] != 0 and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]-1] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]-1] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]-1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]-1] == 8) and (tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 0 or tablero[posicion_pieza[2][0]][posicion_pieza[2][1]-1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]-1] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][1] -= 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
    
    elif lado == "derecha": 
        if posicion_pieza[0][1] != len(tablero[0])-1 and posicion_pieza[1][1] != len(tablero[0])-1 and posicion_pieza[2][1] != len(tablero[0])-1 and posicion_pieza[3][1] != len(tablero[0])-1 and (tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 0 or tablero[posicion_pieza[0][0]][posicion_pieza[0][1]+1] == 8) and (tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 0 or tablero[posicion_pieza[1][0]][posicion_pieza[1][1]+1] == 8) and (tablero[posicion_pieza[2][0]][posicion_pieza[2][1]+1] == 0 or tablero[posicion_pieza[2][0]][posicion_pieza[2][1]+1] == 8) and (tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 0 or tablero[posicion_pieza[3][0]][posicion_pieza[3][1]+1] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][1] += 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
    
    elif lado == "abajo":
        if posicion_pieza[0][0] != len(tablero)-1 and posicion_pieza[1][0] != len(tablero)-1 and posicion_pieza[2][0] != len(tablero)-1 and posicion_pieza[3][0] != len(tablero)-1 and (tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]] == 0 or tablero[posicion_pieza[0][0]+1][posicion_pieza[0][1]] == 8) and (tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 0 or tablero[posicion_pieza[1][0]+1][posicion_pieza[1][1]] == 8) and (tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 0 or tablero[posicion_pieza[2][0]+1][posicion_pieza[2][1]] == 8) and (tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 0 or tablero[posicion_pieza[3][0]+1][posicion_pieza[3][1]] == 8):
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 0
            for i in range(4):
                posicion_pieza[i][0] += 1
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
            time.sleep(speed)
        else:
            for i in range(4):
                tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = pieza
            posicion_pieza, pieza, rotacion, reward = nueva_pieza(posicion_pieza, tablero, rotacion, reward)
            count += 1
                    
    elif lado == "rotar":
        rotacion += 1
        if rotacion > 4:
            rotacion = 0
            
        pass
        time.sleep(speed)
    
    return posicion_pieza, pieza, count

def destruirLinea(tablero):
    for i in range(len(tablero)):
        if 0 not in tablero[i]:
            tablero[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if i != 0: #baja todas las lineas para rellenar la linea borrada
                for a in range(i, 1, -1):
                    tablero[a] = tablero[a-1]
                tablero[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            break

def nueva_pieza(posicion_pieza, tablero, rotacion, reward):
    destruirLinea(tablero) #para checkear si la vez anterior que se ha puesto una pieza, se ha rellenado alguna linea, y si eso la borra
    pieza = random.randint(1,7) # crea una nueva pieza
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
    
    reward += 1
    
    for i in range(4):
        tablero[posicion_pieza[i][0]][posicion_pieza[i][1]] = 8
    return posicion_pieza, pieza, rotacion, reward

screen.fill((0, 0, 0))
posicion_pieza, pieza, rotacion, reward = nueva_pieza(posicion_pieza, tablero, rotacion, reward)
while True:
    print(posicion_pieza)

    for i in range(len(tablero)):
        print(tablero[i])
    
    draw_board(tablero)
    pygame.display.flip()
    
    #inpt = input()
    inpt = random.choice(["Abajo", "Izquierda", "Derecha", "Rotar"])
    
    if inpt == "Abajo":
        posicion_pieza, pieza, count = mover("abajo", posicion_pieza, tablero, pieza, count, rotacion, reward)
    elif inpt == "Derecha":
        posicion_pieza, pieza, count = mover("derecha", posicion_pieza, tablero, pieza, count, rotacion, reward)
    elif inpt == "Izquierda":
        posicion_pieza, pieza, count = mover("izquierda", posicion_pieza, tablero, pieza, count, rotacion, reward)
    elif inpt == "Rotar":
        posicion_pieza, pieza, count = mover("rotar", posicion_pieza, tablero, pieza, count, rotacion, reward)
    
    for i in range(2):
        for a in tablero[i]:
            if a != 0 and a != 8:
                reward -= 50
                print("Game Over!")
                print("Game:", game, "Score:", count, "Rewards:", reward)
                game += 1
                count, reward = 0, 0
                tablero = copy.deepcopy(tablero_base)
                nueva_pieza(posicion_pieza, tablero, rotacion, reward)
                break
