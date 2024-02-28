import simpy as sp
from simulator import program_simulation

SIMULATED_PROGRAMS = 25
MEMORY_CAPACITY = 100

# Setup de Simpy
env = sp.Environment()
RAM = sp.Container(env, init=100, capacity=MEMORY_CAPACITY)
CPU = sp.Resource(env, capacity=1)

for i in range(SIMULATED_PROGRAMS):
    env.process(program_simulation(env, f'Programa_{i+1}', RAM, CPU,))

env.run()