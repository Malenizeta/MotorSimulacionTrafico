import pygame
import random

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, x, y, speeds, vehicles, stoppingGap, defaultStop, simulation, stopLines, movingGap, trafficLightController):
        super().__init__()
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
        self.trafficLightController = trafficLightController

        self.willTurn = random.random() < 0.5
        self.turned = 0
        self.rotateAngle = 0
        self.crossedIndex = 0

        self.vehiclesTurned = {'right': {0: [], 1: []}, 'down': {0: [], 1: []}, 'left': {0: [], 1: []}, 'up': {0: [], 1: []}}
        self.vehiclesNotTurned = {'right': {0: [], 1: []}, 'down': {0: [], 1: []}, 'left': {0: [], 1: []}, 'up': {0: [], 1: []}}
        self.mid = {'right': {'x': 675, 'y': 465}, 'down': {'x': 639, 'y': 348}, 'left': {'x': 763, 'y': 351}, 'up': {'x': 766, 'y': 472}}
        self.rotationAngle = 5

        path = f"images/{direction}/{vehicleClass}.png"
        self.originalImage = pygame.image.load(path)
        self.image = self.originalImage.copy()

        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1

        if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
            prev = vehicles[direction][lane][self.index - 1]
            if direction == 'right':
                self.stop = prev.stop - prev.image.get_rect().width - stoppingGap
            elif direction == 'left':
                self.stop = prev.stop + prev.image.get_rect().width + stoppingGap
            elif direction == 'down':
                self.stop = prev.stop - prev.image.get_rect().height - stoppingGap
            elif direction == 'up':
                self.stop = prev.stop + prev.image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

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
        currentGreen = self.trafficLightController.currentGreen
        currentYellow = self.trafficLightController.currentYellow

        if self.direction == 'right':
            # Si el vehículo cruza la línea de detención
            if self.crossed == 0 and self.x + self.image.get_rect().width > self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            # Cuando el vehículo cruza y no va a girar (willTurn == False)
            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                if self.lane in self.vehiclesNotTurned[self.direction]:
                    self.vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            if self.lane == 1:
                if self.willTurn:
                    # Vehículo que va a girar
                    if self.crossed == 0 or self.x + self.image.get_rect().width < self.stopLines[self.direction] + 85:
                        if ((self.x + self.image.get_rect().width <= self.stop or
                            (currentGreen == 0 and currentYellow == 0) or self.crossed == 1) and
                            (self.index == 0 or
                            self.x + self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index - 1].x - self.movingGap) or
                            self.vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x += self.speed
                    else:
                        # Proceso de girar
                        if self.turned == 0:
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 2.4
                            self.y += 2.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            # Movimiento después de girar
                            if self.crossedIndex == 0 or (
                                self.y > self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].y +
                                self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().height + self.movingGap):
                                self.y += self.speed
                else:
                    # Vehículo que sigue recto (lane 1)
                    if self.crossed == 0:
                        if ((self.x + self.image.get_rect().width <= self.stop or
                            (currentGreen == 0 and currentYellow == 0)) and
                            (self.index == 0 or
                            self.x + self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index - 1].x - self.movingGap))):
                            self.x += self.speed
                    else:
                        if self.crossedIndex == 0 or (
                            self.x + self.image.get_rect().width < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x - self.movingGap):
                            self.x += self.speed
            else:
                # Carril 2
                if self.crossed == 0:
                    if ((self.x + self.image.get_rect().width <= self.stop or
                        (currentGreen == 0 and currentYellow == 0)) and
                        (self.index == 0 or
                        self.x + self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index - 1].x - self.movingGap))):
                        self.x += self.speed
                else:
                    if self.crossedIndex == 0 or (
                        self.x + self.image.get_rect().width < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x - self.movingGap):
                        self.x += self.speed

        elif self.direction == 'down':
            if self.crossed == 0 and self.y + self.image.get_rect().height > self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                if self.lane in self.vehiclesNotTurned[self.direction]:
                    self.vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            if self.lane != 1:
                if self.willTurn:
                    if self.crossed == 0 or self.y + self.image.get_rect().height < self.stopLines[self.direction] + 75:
                        if ((self.y + self.image.get_rect().height <= self.stop or
                            (currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and
                            (self.index == 0 or
                            self.y + self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index - 1].y - self.movingGap) or
                            self.vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y += self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x -= 2.4
                            self.y += 2.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if self.crossedIndex == 0 or (
                                self.x < self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].x -
                                self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().width - self.movingGap):
                                self.x -= self.speed
                else:
                    if self.crossed == 0:
                        if ((self.y + self.image.get_rect().height <= self.stop or
                            (currentGreen == 1 and currentYellow == 0)) and
                            (self.index == 0 or
                            self.y + self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index - 1].y - self.movingGap))):
                            self.y += self.speed
                    else:
                        if self.crossedIndex == 0 or (
                            self.y + self.image.get_rect().height < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].y - self.movingGap):
                            self.y += self.speed
            else:
                if self.crossed == 0:
                    if ((self.y + self.image.get_rect().height <= self.stop or
                        (currentGreen == 1 and currentYellow == 0)) and
                        (self.index == 0 or
                        self.y + self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index - 1].y - self.movingGap))):
                        self.y += self.speed
                else:
                    if self.crossedIndex == 0 or (
                        self.y + self.image.get_rect().height < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].y - self.movingGap):
                        self.y += self.speed

        elif self.direction == 'left':
            if self.crossed == 0 and self.x < self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                if self.lane in self.vehiclesNotTurned[self.direction]:
                    self.vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            if self.lane != 1:
                if self.willTurn:
                    if self.crossed == 0 or self.x > self.stopLines[self.direction] - 50:
                        if ((self.x >= self.stop or
                            (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and
                            (self.index == 0 or
                            self.x > (self.vehicles[self.direction][self.lane][self.index - 1].x +
                                    self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + self.movingGap) or
                            self.vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x -= 2.4
                            self.y -= 2.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if self.crossedIndex == 0 or (
                                self.y < self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].y -
                                self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().height - self.movingGap):
                                self.y -= self.speed
                else:
                    if self.crossed == 0:
                        if ((self.x >= self.stop or
                            (currentGreen == 2 and currentYellow == 0)) and
                            (self.index == 0 or
                            self.x > (self.vehicles[self.direction][self.lane][self.index - 1].x +
                                    self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + self.movingGap))):
                            self.x -= self.speed
                    else:
                        if self.crossedIndex == 0 or (
                            self.x > self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x +
                            self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().width + self.movingGap):
                            self.x -= self.speed
            else:
                if self.crossed == 0:
                    if ((self.x >= self.stop or
                        (currentGreen == 2 and currentYellow == 0)) and
                        (self.index == 0 or
                        self.x > (self.vehicles[self.direction][self.lane][self.index - 1].x +
                                self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + self.movingGap))):
                        self.x -= self.speed
                else:
                    if self.crossedIndex == 0 or (
                        self.x > self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x +
                        self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().width + self.movingGap):
                        self.x -= self.speed

        elif self.direction == 'up':
            if self.crossed == 0 and self.y < self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                if self.lane in self.vehiclesNotTurned[self.direction]:
                    self.vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            if self.lane == 1:
                if self.willTurn:
                    if self.crossed == 0 or self.y > self.stopLines[self.direction] - 55:
                        if ((self.y >= self.stop or
                            (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and
                            (self.index == 0 or
                            self.y > (self.vehicles[self.direction][self.lane][self.index - 1].y +
                                    self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + self.movingGap) or
                            self.vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 2.4
                            self.y -= 2.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if self.crossedIndex == 0 or (
                                self.x > self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].x +
                                self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().width + self.movingGap):
                                self.x += self.speed
                else:
                    if self.crossed == 0:
                        if ((self.y >= self.stop or
                            (currentGreen == 3 and currentYellow == 0)) and
                            (self.index == 0 or
                            self.y > (self.vehicles[self.direction][self.lane][self.index - 1].y +
                                    self.vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + self.movingGap))):
                            self.y -= self.speed
                    else:
                        if self.crossedIndex == 0 or (
                            self.y > self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].y +
                            self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().height + self.movingGap):
                            self.y -= self.speed