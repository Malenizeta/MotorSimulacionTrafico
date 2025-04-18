import pygame
from simulation.simulator import Simulator

class GUI:
    def __init__(self, simulation: Simulator):
        self.simulation = simulation
        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Traffic Simulation")
        self.clock = pygame.time.Clock()

        # Cargar la imagen de fondo
        self.background = pygame.image.load('images/Interseccion.jpg')

        # Cargar imágenes de los semáforos
        self.red_signal = pygame.image.load('images/signals/red.png')
        self.yellow_signal = pygame.image.load('images/signals/yellow.png')
        self.green_signal = pygame.image.load('images/signals/green.png')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Dibujar el fondo
            self.screen.blit(self.background, (0, 0))

            # Renderizar semáforos y vehículos
            self.render_traffic_lights()
            self.render_vehicles()

            # Actualizar la pantalla
            pygame.display.update()
            self.clock.tick(60)

    def render_traffic_lights(self):
    # Renderizar semáforos basados en su estado actual
        for i, signal in enumerate(self.simulation.signals):  # Acceder a los semáforos desde Simulator
            if signal.green > 0:
                self.screen.blit(self.green_signal, (100 * i + 100, 100))
            elif signal.yellow > 0:
                self.screen.blit(self.yellow_signal, (100 * i + 100, 100))
            else:
                self.screen.blit(self.red_signal, (100 * i + 100, 100))

    def render_vehicles(self):
        # Renderizar vehículos basados en sus posiciones actuales
        for vehicle in self.simulation.simulation:  # `simulation` es el grupo de vehículos
            vehicle.render(self.screen)