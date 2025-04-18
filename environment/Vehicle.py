import pygame

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, x, y, speeds, vehicles, stoppingGap, defaultStop, simulation, stopLines, movingGap, currentGreen, currentYellow):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.vehicles = vehicles
        self.stoppingGap = stoppingGap
        self.defaultStop = defaultStop
        self.simulation = simulation
        self.stopLines = stopLines
        self.movingGap = movingGap
        self.currentGreen = currentGreen
        self.currentYellow = currentYellow

        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = f"images/{direction}/{vehicleClass}.png"
        self.image = pygame.image.load(path)

        # Configuración de la posición de parada
        if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
            if direction == 'right':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().width - stoppingGap
            elif direction == 'left':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().width + stoppingGap
            elif direction == 'down':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().height - stoppingGap
            elif direction == 'up':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Ajustar coordenadas iniciales
        if direction == 'right':
            x[direction][lane] -= self.image.get_rect().width + stoppingGap
        elif direction == 'left':
            x[direction][lane] += self.image.get_rect().width + stoppingGap
        elif direction == 'down':
            y[direction][lane] -= self.image.get_rect().height + stoppingGap
        elif direction == 'up':
            y[direction][lane] += self.image.get_rect().height + stoppingGap

        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.direction == 'right':
            if self.crossed == 0 and self.x + self.image.get_rect().width > self.stopLines[self.direction]:
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (self.currentGreen == 0 and self.currentYellow == 0)) and
                (self.index == 0 or self.x + self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index - 1].x - self.movingGap))):
                self.x += self.speed
        elif self.direction == 'down':
            if self.crossed == 0 and self.y + self.image.get_rect().height > self.stopLines[self.direction]:
                self.crossed = 1
            if ((self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (self.currentGreen == 1 and self.currentYellow == 0)) and
                (self.index == 0 or self.y + self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index - 1].y - self.movingGap))):
                self.y += self.speed
        elif self.direction == 'left':
            if self.crossed == 0 and self.x < self.stopLines[self.direction]:
                self.crossed = 1
            if ((self.x >= self.stop or self.crossed == 1 or (self.currentGreen == 2 and self.currentYellow == 0)) and
                (self.index == 0 or self.x > (self.vehicles[self.direction][self.lane][self.index - 1].x + self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + self.movingGap))):
                self.x -= self.speed
        elif self.direction == 'up':
            if self.crossed == 0 and self.y < self.stopLines[self.direction]:
                self.crossed = 1
            if ((self.y >= self.stop or self.crossed == 1 or (self.currentGreen == 3 and self.currentYellow == 0)) and
                (self.index == 0 or self.y > (self.vehicles[self.direction][self.lane][self.index - 1].y + self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + self.movingGap))):
                self.y -= self.speed