# simulacion_trafico/environment/vehicle.py

class Vehicle:
    """
    Clase que modela el comportamiento básico de un vehículo.
    """
    def __init__(self, id_, position=(0, 0), speed=0.0, direction="NORTE"):
        self.id_ = id_
        self.position = position
        self.speed = speed
        self.direction = direction
        self.route = []

    def move(self):
        """
        Actualiza la posición del vehículo en función de su dirección y velocidad.
        Aquí se usa un modelo muy simplificado; en un motor real se realizarían
        cálculos de física, detección de colisiones, etc.
        """
        if not self.route:
            return 

        target = self.route[0]
        x, y = self.position
        tx, ty = target

        # Calculo el vector de dirección
        dx, dy = tx - x, ty - y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            # Llegó al punto
            self.position = target
            self.route.pop(0)
        else:
            # Avanza hacia el punto
            self.position = (x + self.speed * dx / dist, y + self.speed * dy / dist)

    def __str__(self):
        return f"Vehicle {self.id_} at position {self.position}, speed {self.speed}, direction {self.direction}"
