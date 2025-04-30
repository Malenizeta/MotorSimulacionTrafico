https://github.com/Malenizeta/MotorSimulacionTrafico.git

# Motor de Simulación de Tráfico

## Introducción
Este proyecto es un motor de simulación de tráfico urbano que he desarrollado para modelar el comportamiento de vehículos, semáforos y su interacción en un entorno urbano. La simulación incluye una interfaz gráfica para visualizar el tráfico en tiempo real y utiliza programación concurrente y distribuida para manejar eventos simultáneos y escalabilidad.

---

## Funcionalidades Principales

### 1. Semáforos
He implementado un sistema de semáforos que regula el flujo de tráfico en las intersecciones. Los semáforos cambian de estado (rojo, amarillo, verde) de manera cíclica y están controlados por un controlador (`TrafficLightController`). Este controlador utiliza hilos para actualizar los tiempos de los semáforos y garantizar que las señales funcionen correctamente.

### 2. Vehículos
Los vehículos están modelados como objetos individuales con atributos como:
- Tipo de vehículo (coche, autobús, camión, moto).
- Dirección (arriba, abajo, izquierda, derecha).
- Velocidad y posición.
- Comportamiento al girar o continuar recto.

Los vehículos respetan las señales de tráfico y se mueven por las calles simuladas. Además, he implementado lógica para manejar colisiones y detenerse en las líneas de parada.

### 3. Interfaz Gráfica
La interfaz gráfica, desarrollada con **Pygame**, permite visualizar el tráfico en tiempo real. Incluye:
- Representación visual de los semáforos.
- Movimiento de los vehículos en las calles.
- Un fondo que simula una intersección urbana.

### 4. Comunicación Distribuida
He integrado **RabbitMQ** para manejar la comunicación entre diferentes nodos de la simulación. Esto permite que los vehículos que salen del mapa puedan ser enviados a otras zonas simuladas. La comunicación se realiza de manera asíncrona utilizando la biblioteca `aio-pika`.

---

## Estructura del Código

### 1. `TrafficLight.py`
Este archivo contiene la lógica de los semáforos:
- La clase `TrafficLight` define los tiempos de cada estado (rojo, amarillo, verde).
- La clase `TrafficLightController` gestiona el ciclo de los semáforos y utiliza un hilo para actualizar los estados de manera periódica.

### 2. `Vehicle.py`
Aquí he implementado la clase `Vehicle`, que representa a los vehículos en la simulación. Cada vehículo:
- Se mueve según su velocidad y dirección.
- Respeta las señales de tráfico.
- Puede girar o continuar recto dependiendo de su configuración.
- Envía datos a través de RabbitMQ si sale del mapa.

### 3. `simulator.py`
El archivo `simulator.py` contiene la lógica principal de la simulación:
- Generación de vehículos de manera periódica.
- Recepción de vehículos desde otros nodos utilizando RabbitMQ.
- Gestión de la interacción entre vehículos y semáforos.

### 4. `gui.py`
La interfaz gráfica se encuentra en este archivo:
- Renderiza los semáforos y vehículos en la pantalla.
- Actualiza el estado de la simulación en tiempo real.
- Permite observar el flujo de tráfico de manera visual.

### 5. `rabbit_client.py`
Este archivo maneja la comunicación con RabbitMQ:
- Envío de datos de vehículos que salen del mapa.
- Recepción de vehículos desde otros nodos.
- Uso de colas y mensajes para garantizar la comunicación asíncrona.

### 6. `main.py`
El archivo principal inicializa todos los componentes:
- Configura los semáforos y el controlador.
- Inicia la simulación y la generación de vehículos.
- Lanza la interfaz gráfica para visualizar el tráfico.

---

## Cómo Ejecutar el Proyecto

1. Instala las dependencias necesarias:
   ```bash
   pip install pygame aio-pika
