import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, env, num_processes, arrival_interval=10, memory=200, cpu_speed=3, num_cpus=1):
        self.env = env
        self.memory = simpy.Container(env, init=memory, capacity=memory)
        self.cpu = simpy.Resource(env, capacity=num_cpus)
        self.num_processes = num_processes
        self.arrival_interval = arrival_interval
        self.cpu_speed = cpu_speed
        self.process_times = []
        self.process_generator = env.process(self.generate_processes(env))
    
    def generate_processes(self, env):
        for i in range(self.num_processes):
            instructions = random.randint(50, 200)
            env.process(self.process(env, i, instructions))
            yield env.timeout(self.arrival_interval)
    
    def process(self, env, pid, instructions):
        start_time = env.now
        with self.cpu.request() as req:
            yield req
            while instructions > 0:
                yield env.timeout(1)
                instructions -= self.cpu_speed
                if random.randint(1, 2) == 1:
                    yield env.timeout(5)  # Simula espera por I/O
        end_time = env.now
        self.process_times.append(end_time - start_time)
    
    def get_results(self):
        return np.mean(self.process_times), np.std(self.process_times)

def run_experiment(num_processes_list, arrival_interval, title):
    results = []
    for num_processes in num_processes_list:
        env = simpy.Environment()
        sim = Simulation(env, num_processes, arrival_interval=arrival_interval, memory=200)
        env.run()
        avg_time, std_time = sim.get_results()
        results.append((num_processes, avg_time, std_time))
        print(f'Procesos: {num_processes}, Tiempo Promedio: {avg_time:.2f}, Desviación Estándar: {std_time:.2f}')
    
    # Graficar resultados
    plt.figure(figsize=(10, 5))
    x, y, _ = zip(*results)
    plt.plot(x, y, marker='o', label=f'Intervalo {arrival_interval}')
    plt.xlabel('Número de procesos')
    plt.ylabel('Tiempo promedio en sistema')
    plt.title(title)
    plt.legend()
    plt.show()

# Ejecutar experimentos con intervalo de llegada 10
title_10 = 'Simulación con intervalo de llegada 10'
run_experiment([25, 50, 100, 150, 200], arrival_interval=10, title=title_10)
