'''
OS simulation
Autor: Nils Muralles Morales
Fecha: 24/02/24
Versión: 1.0.0 
'''

import simpy as sp
import random as ran

MEMORY_CAPACITY = 100
SIMULATED_PROGRAMS = 25
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
    print(f'NEW: {program_name} llega al sistema operativo en {env.now:.3} y solicita {requested_memory} espacios de memoria')

    if (ram.level > requested_memory): # Verificar que haya memoria
        # Verificar que todavía queden instrucciones por ser ejecutadas
        while instructions_left > 0:
            print(f"READY: {program_name} está listo para correr {instructions_left} instrucciones en {env.now:.3}") 
            with cpu.request() as req:
                yield req
                print(f"RUNNING: {program_name} accede al procesador en {env.now:.3}")
                
                # Espera a que el procesador haga las operaciones
                yield env.timeout(INSTRUCTION_FRECUENCY)

                if instructions_left <= INSTRUCTION_FRECUENCY: # Si el número de instrucciones es igual o menor al máximo de instrucciones por unidad de tiempo    

                    # Solicitud de memoria
                    yield ram.get(requested_memory)

                    # Fin de la ejecución
                    print(f"TERMINATED: {program_name} terminó su ejecución. Sale del sistema en {env.now:.3}")
                    ram.put(requested_memory) # Devuelve la memoria utilizada para el proceso
                    instructions_left = 0

                else: # Si el número de instrucciones es mayor (N)

                   # ¿WAITING? Cola en la que se hacen operaciones I/O
                   choice = ran.randint(1,2)

                   if (choice == 1): # Pasa a waiting
                       print(f"WAITING: {program_name} pasa a la cola de waiting")
                       yield env.timeout(2) # El programa espera lo que se tarda el CPU en ejecutar un programa

                   else: # Regresa a ready
                       pass

                instructions_left -= INSTRUCTION_FRECUENCY 

# Semilla para replicabilidad del los procesos
ran.seed(RANDOM_SEED)

# Setup de Simpy
env = sp.Environment()
RAM = sp.Container(env, init=100, capacity=MEMORY_CAPACITY)
CPU = sp.Resource(env, capacity=1)

for i in range(SIMULATED_PROGRAMS):
    env.process(program_simulation(env, f'Programa_{i+1}', RAM, CPU,))

env.run()