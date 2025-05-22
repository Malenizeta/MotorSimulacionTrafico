import pygame
import random
import asyncio

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, x, y, speeds, vehicles, stoppingGap, defaultStop, simulation, stopLines, movingGap, trafficLightController, rabbit_client=None, is_emergency=False):
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
        self.rabbit_client = rabbit_client
        self.is_emergency = is_emergency

        self.willTurn = random.random() < 0.5
        self.turned = 0
        self.rotateAngle = 0
        self.crossedIndex = 0

        self.vehiclesTurned = {'right': {0: [], 1: []}, 'down': {0: [], 1: []}, 'left': {0: [], 1: []}, 'up': {0: [], 1: []}}
        self.vehiclesNotTurned = {'right': {0: [], 1: []}, 'down': {0: [], 1: []}, 'left': {0: [], 1: []}, 'up': {0: [], 1: []}}
        self.mid = {'right': {'x': 675, 'y': 465}, 'down': {'x': 639, 'y': 348}, 'left': {'x': 763, 'y': 351}, 'up': {'x': 766, 'y': 472}}
        self.rotationAngle = 5

        if is_emergency:
            path = f"images/{direction}/emergency.png"
        else:
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
    
    def is_ambulance_behind(self):
        for i in range(self.index + 1, len(self.vehicles[self.direction][self.lane])):
            vehicle = self.vehicles[self.direction][self.lane][i]
            if vehicle.is_emergency:
                # Chequea si la ambulancia está suficientemente cerca
                if self.direction in ['right', 'left']:
                    distance = abs(vehicle.x - self.x)
                else:
                    distance = abs(vehicle.y - self.y)
                if distance < 200:  # puedes ajustar esta distancia
                    return True
        return False

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def can_move_emergency(self):
        # Un vehículo de emergencia puede moverse sin restricciones
        return self.is_emergency
    
    def is_ambulance_crossing(self):
            for direction in self.vehicles:
                for lane in self.vehicles[direction]:
                    for vehicle in self.vehicles[direction][lane]:
                        if vehicle.is_emergency and 592 <= vehicle.x <= 792 and 295 <= vehicle.y <= 495:
                            return True
            return False
        
    def move(self):
        currentGreen = self.trafficLightController.currentGreen
        currentYellow = self.trafficLightController.currentYellow
        rect = self.image.get_rect()
        width = rect.width
        height = rect.height
        movingGap = self.movingGap

        # Verificar si hay una ambulancia cruzando
        ambulance_crossing = False
        for direction in self.vehicles:
            for lane in [0, 1]:
                for vehicle in self.vehicles[direction][lane]:
                    if vehicle.is_emergency and 592 <= vehicle.x <= 792 and 295 <= vehicle.y <= 495:
                        ambulance_crossing = True
                        break

        def can_move_forward(pos, stop_pos, index_check, vehicles_list, axis='x', direction=1):
            if index_check == 0:
                return True
            prev_vehicle = vehicles_list[index_check - 1]
            if axis == 'x':
                if direction > 0:
                    return pos < (prev_vehicle.x - movingGap)
                else:
                    return pos > (prev_vehicle.x + prev_vehicle.image.get_rect().width + movingGap)
            else:
                if direction > 0:
                    return pos < (prev_vehicle.y - movingGap)
                else:
                    return pos > (prev_vehicle.y + prev_vehicle.image.get_rect().height + movingGap)


        in_intersection = (592 <= self.x <= 792) and (295 <= self.y <= 495)
        # Definir factor de aceleración solo si hay ambulancia y está en intersección
        acceleration_factor = 1.5 if (ambulance_crossing and in_intersection and not self.is_emergency) else 1

        ambulance_direction_crossing = None
        for direction in self.vehicles:
            for lane in [0, 1]:
                for vehicle in self.vehicles[direction][lane]:
                    if vehicle.is_emergency and 592 <= vehicle.x <= 792 and 295 <= vehicle.y <= 495:
                        ambulance_direction_crossing = direction
                        break
                if ambulance_direction_crossing:
                    break
            if ambulance_direction_crossing:
                break

        # Función para verificar si la dirección es perpendicular a la ambulancia cruzando
        def is_perpendicular(dir1, dir2):
            perpendicular_pairs = {
                'right': ['up', 'down'],
                'left': ['up', 'down'],
                'up': ['left', 'right'],
                'down': ['left', 'right']
            }
            return dir2 in perpendicular_pairs.get(dir1, [])

        # Frenar si ambulancia cruzando y vehículo va perpendicular a la ambulancia
        if ambulance_direction_crossing and is_perpendicular(ambulance_direction_crossing, self.direction) and not self.is_emergency:
            # Aquí el vehículo no se mueve, por ejemplo, saliendo directamente de move() o return
            return

        # Según dirección
        if self.direction == 'right':
            speed = self.speed * acceleration_factor

            if self.crossed == 0 and ambulance_crossing and not self.is_emergency:
                return

            if self.crossed == 0 and self.x + width > self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                if self.lane in self.vehiclesNotTurned[self.direction]:
                    self.vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            speed = self.speed * 1.5 if self.crossed == 1 and ambulance_crossing and not self.is_emergency else self.speed

            # Movimiento según carril y giro
            if self.lane != 1 and self.lane != 0:
                if self.willTurn:
                    if self.crossed == 0 or self.x + width < self.stopLines[self.direction] + 85:
                        if ((self.x + width <= self.stop or
                            self.can_move_emergency() or
                            self.is_ambulance_behind() or
                            (currentGreen == 0 and currentYellow == 0)) and
                            (self.index == 0 or
                            can_move_forward(self.x + width, self.stop, self.index, self.vehicles[self.direction][self.lane]))):
                            self.x += speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 2.4
                            self.y += 2.8
                            if self.rotateAngle >= 90:
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if self.crossedIndex == 0 or (
                                self.y > self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].y +
                                self.vehiclesTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().height + movingGap):
                                self.y += speed
                else:
                    if self.crossed == 0:
                        if ((self.x + width <= self.stop or
                            self.can_move_emergency() or
                            self.is_ambulance_behind() or
                            (currentGreen == 0 and currentYellow == 0)) and
                            (self.index == 0 or
                            can_move_forward(self.x + width, self.stop, self.index, self.vehicles[self.direction][self.lane]))):
                            self.x += speed
                    else:
                        if self.crossedIndex == 0 or (
                            self.x + width < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x - movingGap):
                            self.x += speed

            else:
                if self.crossed == 0:
                    if ((self.x + width <= self.stop or
                        self.can_move_emergency() or
                        self.is_ambulance_behind() or
                        (currentGreen == 0 and currentYellow == 0)) and
                        (self.index == 0 or
                        can_move_forward(self.x + width, self.stop, self.index, self.vehicles[self.direction][self.lane]))):
                        self.x += speed
                else:
                    if self.crossedIndex == 0 or (
                        self.x + width < self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x - movingGap):
                        self.x += speed

        elif self.direction == 'down':
            speed = self.speed * acceleration_factor
            if self.crossed == 0 and ambulance_crossing and not self.is_emergency:
                return

            if self.crossed == 0 and self.y + height > self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.lane not in self.vehiclesNotTurned[self.direction]:
                self.vehiclesNotTurned[self.direction][self.lane] = []

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                self.vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            speed = self.speed * 1.5 if self.crossed == 1 and ambulance_crossing and not self.is_emergency else self.speed

            if self.crossed == 0:
                can_advance = (
                    (self.index == 0 and self.is_ambulance_behind()) or
                    self.y + height <= self.stop or
                    self.can_move_emergency() or
                    (currentGreen == 1 and currentYellow == 0)
                )
                has_gap = (
                    self.index == 0 or
                    can_move_forward(self.y + height, self.stop, self.index,
                                    self.vehicles[self.direction][self.lane], axis='y', direction=1)
                )

                if can_advance and has_gap:
                    self.y += speed

            else:
                prev = (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1]
                        if self.crossedIndex > 0 else None)

                if self.crossedIndex == 0 or (
                    prev and self.y + height < prev.y - movingGap
                ):
                    self.y += speed

        elif self.direction == 'left':
            speed = self.speed * acceleration_factor
            if self.crossed == 0 and ambulance_crossing and not self.is_emergency:
                return

            if self.crossed == 0 and self.x < self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                self.vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            speed = self.speed * 1.5 if self.crossed == 1 and ambulance_crossing and not self.is_emergency else self.speed

            if self.crossed == 0:
                if ((self.x >= self.stop or
                    self.can_move_emergency() or
                    self.is_ambulance_behind() or
                    (currentGreen == 2 and currentYellow == 0)) and
                    (self.index == 0 or
                    can_move_forward(self.x, self.stop, self.index,
                                    self.vehicles[self.direction][self.lane], axis='x', direction=-1))):
                    self.x -= speed
            else:
                if self.crossedIndex == 0 or (
                    self.x > self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].x +
                    self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().width + movingGap):
                    self.x -= speed

        # Dirección UP
        elif self.direction == 'up':
            speed = self.speed * acceleration_factor
            if self.crossed == 0 and ambulance_crossing and not self.is_emergency:
                return

            if self.crossed == 0 and self.y < self.stopLines[self.direction]:
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1

            if self.crossed == 1 and self.willTurn == 0 and self.crossedIndex == -1:
                self.vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(self.vehiclesNotTurned[self.direction][self.lane]) - 1

            speed = self.speed * 1.5 if self.crossed == 1 and ambulance_crossing and not self.is_emergency else self.speed

            if self.crossed == 0:
                if ((self.y >= self.stop or
                    self.can_move_emergency() or
                    self.is_ambulance_behind() or
                    (currentGreen == 3 and currentYellow == 0)) and
                    (self.index == 0 or
                    can_move_forward(self.y, self.stop, self.index,
                                    self.vehicles[self.direction][self.lane], axis='y', direction=-1))):
                    self.y -= speed
            else:
                if self.crossedIndex == 0 or (
                    self.y > self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].y +
                    self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex - 1].image.get_rect().height + movingGap):
                    self.y -= speed

        if not asyncio.get_event_loop().is_running():
                asyncio.run(self.check_and_send_if_outside())
        else:
                asyncio.create_task(self.check_and_send_if_outside())

    async def check_and_send_if_outside(self):
        MAP_WIDTH = 1400
        MAP_HEIGHT = 800
        if (self.x > MAP_WIDTH or self.x < 0 or self.y > MAP_HEIGHT or self.y < 0):
            if self.rabbit_client:
                vehicle_data = {
                    "lane": self.lane,
                    "vehicleClass": self.vehicleClass,
                    "direction_number": self.direction_number,
                    "direction": self.direction,
                    "position": {"x": self.x, "y": self.y},
                    "speed": self.speed,
                    "willTurn": self.willTurn
                }
                await self.rabbit_client.send_vehicle(vehicle_data)
            self.simulation.remove(self)

