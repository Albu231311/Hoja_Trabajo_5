import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Parámetros de la simulación
NUM_PROCESOS = [25, 50, 100, 150, 200]
MEMORIA_RAM_INICIAL = 200
MEMORIA_RAM_FINAL = 100
VELOCIDAD_CPU = 1
TIEMPO_TOTAL_SIMULACION = 1000
INTERVALOS = [10, 5, 1]