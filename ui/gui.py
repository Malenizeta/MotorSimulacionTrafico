import pygame
from simulation.simulator import Simulator
from environment.TrafficLight import TrafficLightController

class GUI:
    def __init__(self, simulator: Simulator, traffic_controller: TrafficLightController):
        self.simulation = simulator.simulation
        self.signals = traffic_controller.signals
        self.currentGreen = traffic_controller.currentGreen
        self.currentYellow = traffic_controller.currentYellow

        self.signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]

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
        for i in range(len(self.signals)):
            if i == self.currentGreen:
                if self.currentYellow == 1:
                    self.screen.blit(self.yellow_signal, self.signalCoods[i])
                else:
                    self.screen.blit(self.green_signal, self.signalCoods[i])
            else:
                self.screen.blit(self.red_signal, self.signalCoods[i])

    def render_vehicles(self):
        for vehicle in self.simulation:
            vehicle.move()
            vehicle.render(self.screen)
