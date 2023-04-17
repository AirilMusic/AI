import RPi.GPIO as GPIO
from subprocess import call
import json
from pathlib import Path

def take_photo(): # saca una foto y return del nombre y el directorio
    images_dir = Path("Desktop/images") # si no existe el directorio lo crea
    images_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = "image-small.jpg" # crea el nombre de la foto en vase a si ya existe una con el mismo nombre
    i = 1
    while (images_dir / base_name).exists():
        base_name = f"image-small-{i}.jpg"
        i += 1
        
    file_path = images_dir / base_name
    call(["raspistill", "-o", str(file_path), "-w", "170", "-h", "170"]) # saca la foto
    return str(file_path)

def chose_bird(imagen): # return la especie de pajaro
    pass 

bird_count_file = Path("bird_count.json") # si no existe crea un archivo.json donde habra un diccionario {ave:veces_cotadas}
if bird_count_file.exists():
    with bird_count_file.open() as f:
        bird_count = json.load(f)

while True:
    if GPIO.input(18) == GPIO.HIGH:# si el ultrasonidos lo detecta
        img = take_photo()
        bird = chose_bird(img)
        
        #Actualiza la BBDD (el diccionario del archivo.json)
        if bird in bird_count: 
            bird_count[bird] += 1
        else:
            bird_count[bird] = 1
        
        with bird_count_file.open("w") as f:
            json.dump(bird_count, f)
