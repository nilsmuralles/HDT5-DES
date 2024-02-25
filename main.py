'''
OS simulation
Autor: Nils Muralles Morales
Fecha: 24/02/24
Versión: 1.0.0 
'''

import simpy as sp
import random as ran

MEMORY_CAPACITY = 100
SIMULATED_PROGRAMS = 5
INSTRUCTION_FRECUENCY = 3
RANDOM_SEED = 10
ran.seed(RANDOM_SEED)
CPU_FRECUENCY = 1
INTERVAL = 1

def program_simulation(env, program_name, ram, cpu):
    # Espacios de memoria solicitada (1-10)
    requested_memory = ran.randint(1, 10)

    # Distribución exponencial para la creación de procesos
    yield env.timeout(ran.expovariate(1.0/INTERVAL))
    print(f'NEW: {program_name} llega al sistema operativo en {env.now} y solicita {requested_memory} espacios de memoria')

    # Retiro de memoria solicitada
    yield ram.get(requested_memory)

env = sp.Environment()
RAM = sp.Container(env, init=100, capacity=MEMORY_CAPACITY)
CPU = sp.Resource(env, capacity=1)

