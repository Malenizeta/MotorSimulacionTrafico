import threading
from environment.TrafficLight import TrafficLightController
from simulation.simulator import Simulator
import pygame

def main():
    # Configuración inicial
    defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
    defaultRed = 150
    defaultYellow = 5
    noOfSignals = 4
    clock = pygame.time.Clock()  # Controlar FPS
    screen = pygame.display.set_mode((1400, 800))  # Configurar la ventana de pygame
    pygame.display.set_caption("Simulación de Tráfico")


    background = pygame.image.load('images/Interseccion.jpg')

    speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}
    x = {'right': [0, 0], 'down': [630, 675], 'left': [1400, 1400], 'up': [715, 750]}
    y = {'right': [420, 460], 'down': [0, 0], 'left': [342, 380], 'up': [800, 800]}
    vehicles = {'right': {0: [], 1: [], 'crossed': 0}, 'down': {0: [], 1: [], 'crossed': 0}, 'left': {0: [], 1: [], 'crossed': 0}, 'up': {0: [], 1: [], 'crossed': 0}}
    vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
    directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}
    stoppingGap = 15
    defaultStop = {'right': 540, 'down': 245, 'left': 860, 'up': 570}
    stopLines = {'right': 560, 'down': 265, 'left': 840, 'up': 550}  # Definición de stopLines
    movingGap = 15  # Espacio entre vehículos en movimiento
    currentGreen = 0  # Semáforo actual en verde
    currentYellow = 0
    simulation = pygame.sprite.Group()

    # Inicializar controladores
    trafficLightController = TrafficLightController(defaultGreen, defaultYellow, defaultRed, noOfSignals)
    trafficLightController.initialize()
    signals = trafficLightController.signals  

    simulator = Simulator(
        vehicleTypes=vehicleTypes,
        directionNumbers=directionNumbers,
        vehicles=vehicles,
        x=x,
        y=y,
        speeds=speeds,
        stoppingGap=stoppingGap,
        defaultStop=defaultStop,
        simulation=simulation,
        stopLines=stopLines, 
        movingGap=movingGap,  
        currentGreen=currentGreen,  
        currentYellow=currentYellow,
        signals=signals 
    )
    # Iniciar generación de vehículos
    thread_generate = threading.Thread(target=simulator.generateVehicles)
    thread_generate.daemon = True
    thread_generate.start()

    # Lógica principal
    while True:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar la ventana
                pygame.quit()
                return

        # Dibujar el fondo
        screen.blit(background, (0, 0))

        # Actualizar el estado de los vehículos
        for vehicle in simulation:
            vehicle.move()

        # Dibujar los vehículos
        for vehicle in simulation:
            vehicle.render(screen)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad de actualización (FPS)
        clock.tick(60)

if __name__ == "__main__":
    main()