import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def save_network(network, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    save_path = os.path.join(script_dir, 'networks')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    network.save(os.path.join(save_path, filename))
    print("[+] Saved network")

