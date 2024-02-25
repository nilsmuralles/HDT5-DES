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
INSTRUCTION_FRECUENCY = 3 # Instrucciones por unidad de tiempo
RANDOM_SEED = 10
CPU_FRECUENCY = 1 # Procesos en el CPU por unidad de tiempo
INTERVAL = 1

def program_simulation(env, program_name, ram, cpu):
    # Espacios de memoria solicitada e instrucciones (1-10)
    requested_memory = ran.randint(1, 10)
    instructions_left = ran.randint(1, 10)

    # Distribución exponencial para la creación de procesos
    yield env.timeout(ran.expovariate(1.0/INTERVAL))
    print(f'NEW: {program_name} llega al sistema operativo en {env.now:.2} y solicita {requested_memory} espacios de memoria')

    # Verificar que todavía queden instrucciones por ser ejecutadas
    while instructions_left > 0:
        print(f"READY: {program_name} está listo para correr {instructions_left} instrucciones en {env.now:.2}")

        # Solicitud de memoria
        yield ram.get(requested_memory)

        if (ram.level > 0): # Verificar que haya memoria 
            with cpu.request() as req:
                yield req

                if instructions_left <= INSTRUCTION_FRECUENCY: # Si el número de instrucciones es igual o menor al máximo de instrucciones por unidad de tiempo
                    print(f"RUNNING: {program_name} accede al procesador en {env.now:.2}")

                    # Espera a que el procesador haga las operaciones
                    yield env.timeout(INSTRUCTION_FRECUENCY * instructions_left)

                    # Fin de la ejecución
                    print(f"TERMINATED: {program_name} terminó su ejecución. Sale del sistema en {env.now:.2}")
                    ram.put(requested_memory) # Devuelve la memoria utilizada para el proceso
                    instructions_left = 0

                else: # Si el número de instrucciones es mayor (N)
                   print(f"RUNNING: {program_name} accede al procesador en {env.now:.2}")
                   yield env.timeout(INSTRUCTION_FRECUENCY * instructions_left) # Tiempo en el que se realizan N instrucciones por unidad de tiempo

                   # ¿WAITING?
                   choice = ran.randint(1,2)
                   if (choice == 1):
                       print(f"WAITING: {program_name} pasa a la cola de waiting")
                       yield env.timeout(CPU_FRECUENCY) # El programa espera lo que se tarda el CPU en ejecutar un programa

                   else:
                       pass

                   instructions_left -= INSTRUCTION_FRECUENCY     

# Semilla para replicabilidad del los procesos
ran.seed(RANDOM_SEED)

# Setup de Simpy
env = sp.Environment()
RAM = sp.Container(env, init=100, capacity=MEMORY_CAPACITY)
CPU = sp.Resource(env, capacity=1)