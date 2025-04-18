import pygame
from simulation.simulator import Simulator
from environment.TrafficLight import TrafficLightController

class GUI:
    def __init__(self, simulator: Simulator, traffic_controller: TrafficLightController):
        self.simulation = simulator.simulation
        self.signals = traffic_controller.signals
        self.traffic_controller = traffic_controller
        self.currentGreen = traffic_controller.currentGreen
        self.currentYellow = traffic_controller.currentYellow

        self.signalCoods = [(480, 490), (590, 170), (850, 295), (780, 550)]
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Traffic Simulation")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('images/Interseccion.jpg')
        self.red_signal = pygame.image.load('images/signals/red.png')
        self.yellow_signal = pygame.image.load('images/signals/yellow.png')
        self.green_signal = pygame.image.load('images/signals/green.png')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.blit(self.background, (0, 0))
            self.render_traffic_lights()
            self.render_vehicles()

            pygame.display.update()
            self.clock.tick(60)

    def render_traffic_lights(self):
        currentGreen = self.traffic_controller.currentGreen
        currentYellow = self.traffic_controller.currentYellow

        for i in range(len(self.signals)):
            if i == currentGreen:
                if currentYellow == 1:
                    signal_image = self.yellow_signal.copy()
                else:
                    signal_image = self.green_signal.copy()
            else:
                signal_image = self.red_signal.copy()

            if i == 0: #abajo izquierda
                signal_image = pygame.transform.rotate(signal_image, -90)
            if i == 1: #arriba izquierda
                signal_image = pygame.transform.rotate(signal_image, 180)
            elif i == 2:
                signal_image = pygame.transform.rotate(signal_image, -270)
            elif i == 3:#abajo derecha
                signal_image = pygame.transform.rotate(signal_image, 0)

            self.screen.blit(signal_image, self.signalCoods[i])



    def render_vehicles(self):
        for vehicle in self.simulation:
            vehicle.move()
            vehicle.render(self.screen)
