import pygame # para la representacion visual del juego para humanos, para ver lo que hace la IA y en que vuelta va
import random
import time

# Piezas:
#     1       2      3     4      5      6      7
#            
#    ####     #       #    ##     ##    ##      #
#             ###   ###    ##    ##      ##    ###

tablero = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # coordenadas: tablero[y[x]]
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

piezaLibre = True # para saber si la pieza que esta bajando se ha colocado o no
posicion_pieza = [[0,0], [0,0], [0,0], [0,0]] #[x,y] pero la y es al reves, osea 0 es arriba y 24 es abajo
pieza = 0

def mover(lado, posicion_pieza, tablero):
    #chequear si debajo tiene algo
    #si no tiene nada bajar
    #sino piezaLibre = True
    #return(posicion pieza) [[x, y], [x, y], [x, y], [x, y]]
    pass
    
def rotar(posicion_pieza, lado, tablero):
    #chequear si se puede rotar
    #si se puede, rotar al lado indicado
    #return(posicion pieza) [[x, y], [x, y], [x, y], [x, y]]
    pass

def destruirLinea(tablero):
    #ver si hay alguna linea que destruir
    #return(linea que destruir) osea, eje y
    pass 

while True:
    if piezaLibre == True:
        piezaLibre = False
        pieza = random.randint(1,7)
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
        
    inpt = ""   # INPUT DE LA IA
    if inpt == "Abajo":
        #mover("abajo", posicion_pieza, tablero) #mover la pieza a la posicion que nos devuelva esa funcion
        pass
    elif inpt == "Derecha":
        #mover("derecha", posicion_pieza, tablero) #mover la pieza a la posicion que nos devuelva esa funcion
        pass
    elif inpt == "Izquierda":
        #mover("izquierda", posicion_pieza, tablero) #mover la pieza a la posicion que nos devuelva esa funcion
        pass
    elif inpt == "RotarDerecha":
        #rotar(posicion_pieza, "derecha", tablero) #mover la pieza a la posicion que nos devuelva esa funcion
        pass
    elif inpt == "RotarIzquierda":
        #rotar(posicion_pieza, "izquierda", tablero) #mover la pieza a la posicion que nos devuelva esa funcion
        pass