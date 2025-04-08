import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.City import City
from environment.TrafficLight import TrafficLight
from environment.Vehicle import Vehicle
from simulation.simulator import Simulator

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tamaño ventana
WIDTH, HEIGHT = 800, 600

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Tráfico")
clock = pygame.time.Clock()

# Crear ciudad y elementos
city = City("MiCiudad")

# Añado dos semáforos en posiciones aleatorias por ahora
traffic_light_positions = [(200, 200), (600, 200)]
for i, pos in enumerate(traffic_light_positions):
    tl = TrafficLight(id_=i)
    tl.position = pos  
    city.add_traffic_light(tl)

# Añado dos vehículos en posiciones aleatorias por ahora
vehicles = [
    Vehicle(id_=1, position=(100, 100), speed=2, direction="ESTE"),
    Vehicle(id_=2, position=(300, 300), speed=1.5, direction="NORTE")
]
for v in vehicles:
    city.add_vehicle(v)

# Creo el simulador
simulator = Simulator(city)

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Manejo evento de cierre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizo lógica
    simulator.update()

    # Dibujo los semáforos
    for tl in city.traffic_lights:
        x, y = tl.position
        color = RED if tl.current_state == "RED" else YELLOW if tl.current_state == "YELLOW" else GREEN
        pygame.draw.rect(screen, color, (x, y, 20, 60))

    # Dibujo los vehículos
    for v in city.vehicles:
        x, y = v.position
        pygame.draw.circle(screen, BLUE, (int(x), int(y)), 10)

    # Refresco la pantalla
    pygame.display.flip()
    clock.tick(30)  # FPS


pygame.quit()
sys.exit()