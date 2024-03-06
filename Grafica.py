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

# Listas para almacenar resultados por intervalo
tiempos_promedio_por_intervalo = [[] for _ in INTERVALOS]
desviaciones_estandar_por_intervalo = [[] for _ in INTERVALOS]

class Proceso:
    def __init__(self, env, memoria, cpu):
        self.env = env
        self.memoria = memoria
        self.cpu = cpu
        self.instrucciones_restantes = random.randint(1, 10)
        self.estado = None
        self.action = env.process(self.proceso())

    def proceso(self):
        yield self.env.timeout(random.expovariate(1.0 / INTERVALOS))
        self.estado = "new"
        yield self.memoria.get(random.randint(1, 10))
        self.estado = "ready"
        while self.instrucciones_restantes > 0:
            with self.cpu.request() as req:
                yield req
                self.estado = "running"
                yield self.env.timeout(VELOCIDAD_CPU)
                self.instrucciones_restantes -= 3
                if self.instrucciones_restantes <= 0:
                    self.estado = "terminated"
                    yield self.memoria.put(random.randint(1, 10))
                else:
                    opcion = random.randint(1, 21)
                    if opcion == 1:
                        self.estado = "waiting"
                        yield self.env.timeout(1)
                        self.estado = "ready"
                    elif opcion == 2:
                        self.estado = "ready"

def simular_procesos(env, num_procesos, memoria_ram):
    memoria = simpy.Container(env, init=memoria_ram, capacity=memoria_ram)
    cpu = simpy.Resource(env, capacity=1)
    for _ in range(num_procesos):
        Proceso(env, memoria, cpu)
    while True:
        yield env.timeout(1)
        if env.now >= TIEMPO_TOTAL_SIMULACION:
            break