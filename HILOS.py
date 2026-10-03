import threading
import time

def tarea1():
    for i in range(5):
        print(f"Tarea 1 - Iteración {i+1}")
        time.sleep(1)  # Simula trabajo

def tarea2():
    for i in range(5):
        print(f"Tarea 2 - Iteración {i+1}")
        time.sleep(1)

# Crear los hilos
hilo1 = threading.Thread(target=tarea1)
hilo2 = threading.Thread(target=tarea2)

# Iniciar los hilos (se ejecutan en paralelo)
hilo1.start()
hilo2.start()

# Esperar a que ambos terminen
hilo1.join()
hilo2.join()

print("Ambas tareas han terminado.")
