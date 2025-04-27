import threading
import pygame
from environment.TrafficLight import TrafficLightController
from simulation.simulator import Simulator
from ui.gui import GUI
from distribution.rabbit_client import RabbitClient
import asyncio

async def main():
    pygame.init()

    # Semáforos
    defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
    defaultRed = 150
    defaultYellow = 3
    noOfSignals = 4
   

    # Inicializar controlador de semáforos
    trafficLightController = TrafficLightController(defaultGreen, defaultYellow, defaultRed, noOfSignals)
    trafficLightController.initialize()

    # Simulación
    simulation = pygame.sprite.Group()

    rabbit_client = RabbitClient()
    await rabbit_client.connect()
    

    simulator = Simulator(
        vehicleTypes={0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'},
        directionNumbers={0: 'right', 1: 'down', 2: 'left', 3: 'up'},
        vehicles={'right': {0: [], 1: [], 'crossed': 0}, 'down': {0: [], 1: [], 'crossed': 0}, 
                  'left': {0: [], 1: [], 'crossed': 0}, 'up': {0: [], 1: [], 'crossed': 0}},
        x={'right': [0, 0], 'down': [630, 675], 'left': [1400, 1400], 'up': [715, 750]},
        y={'right': [420, 460], 'down': [0, 0], 'left': [342, 380], 'up': [800, 800]},
        speeds={'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5},
        stoppingGap=15,
        defaultStop={'right': 540, 'down': 245, 'left': 860, 'up': 570},
        stopLines={'right': 560, 'down': 265, 'left': 840, 'up': 550},
        movingGap=15,
        currentGreen=0,
        currentYellow=0,
        signals=trafficLightController.signals,
        simulation=simulation,
        trafficLightController=trafficLightController,
        rabbit_client=rabbit_client
    )

    # Iniciar hilos
    threading.Thread(target=simulator.generateVehicles, daemon=True).start()
    asyncio.create_task(simulator.receive_vehicles())
    


    # Iniciar GUI
    gui = GUI(simulator, trafficLightController)
    gui.run()

if __name__ == "__main__":
    asyncio.run(main())
