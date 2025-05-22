import threading
import time
from environment.Vehicle import Vehicle
import random

class Simulator:
    def __init__(self, vehicleTypes, directionNumbers, vehicles, x, y, speeds, stoppingGap, defaultStop, simulation, stopLines, movingGap, currentGreen, currentYellow, signals, trafficLightController, rabbit_client):
        self.vehicleTypes = vehicleTypes
        self.directionNumbers = directionNumbers
        self.vehicles = vehicles
        self.x = x
        self.y = y
        self.speeds = speeds
        self.stoppingGap = stoppingGap
        self.defaultStop = defaultStop
        self.simulation = simulation
        self.stopLines = stopLines  
        self.movingGap = movingGap  
        self.currentGreen = currentGreen  
        self.currentYellow = currentYellow
        self.signals = signals
        self.trafficLightController = trafficLightController
        self.rabbit_client = rabbit_client

    def generateVehicles(self):
        while True:
            vehicle_type = random.randint(0, 3)
            is_emergency = random.random() < 0.07
            lane_number = random.randint(0, 1)
            temp = random.randint(0, 99)
            direction_number = 0
            dist = [25, 50, 75, 100]
            if temp < dist[0]:
                direction_number = 0  # From the left (right direction)
            elif temp < dist[1]:
                direction_number = 1  # From above (down direction)
            elif temp < dist[2]:
                direction_number = 3  # From below (up direction)
            else:
                direction_number = 2  # From the right (left direction)
            Vehicle(
                lane=lane_number,
                vehicleClass=self.vehicleTypes[vehicle_type],
                direction_number=direction_number,
                direction=self.directionNumbers[direction_number],
                x=self.x,
                y=self.y,
                speeds=self.speeds,
                vehicles=self.vehicles,
                stoppingGap=self.stoppingGap,
                defaultStop=self.defaultStop,
                simulation=self.simulation,
                stopLines=self.stopLines,  
                movingGap=self.movingGap, 
                trafficLightController = self.trafficLightController, 
                is_emergency=is_emergency
               
            )
            time.sleep(1)

    async def receive_vehicles(self):
            async def handle_vehicle(data):
                Vehicle(
                    lane=data["lane"],
                    vehicleClass=data["vehicleClass"],
                    direction_number=data["direction_number"],
                    direction=data["direction"],
                    x=self.x,
                    y=self.y,
                    speeds=self.speeds,
                    vehicles=self.vehicles,
                    stoppingGap=self.stoppingGap,
                    defaultStop=self.defaultStop,
                    simulation=self.simulation,
                    stopLines=self.stopLines,  
                    movingGap=self.movingGap, 
                    trafficLightController=self.trafficLightController
                )
            await self.rabbit_client.consume_vehicles(handle_vehicle)