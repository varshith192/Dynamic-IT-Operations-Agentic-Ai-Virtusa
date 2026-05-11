import time
import multiprocessing
import os

def stress_cpu():
    print(f"CPU Stressor started on PID {os.getpid()}")
    print("Consuming CPU cycles... Waiting for the AI Agents to remediate me!")
    # Heavy computation to spike CPU
    while True:
        _ = [x**2 for x in range(10000)]

if __name__ == "__main__":
    # Start on multiple cores to ensure a visible spike
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)
    
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
