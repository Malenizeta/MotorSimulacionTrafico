import threading
import time

class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

class TrafficLightController:
    def __init__(self, defaultGreen, defaultYellow, defaultRed, noOfSignals):
        self.signals = []
        self.currentGreen = 0
        self.nextGreen = (self.currentGreen + 1) % noOfSignals
        self.currentYellow = 0
        self.defaultGreen = defaultGreen
        self.defaultYellow = defaultYellow
        self.defaultRed = defaultRed
        self.noOfSignals = noOfSignals

    def initialize(self):
        ts1 = TrafficLight(0, self.defaultYellow, self.defaultGreen[0])
        self.signals.append(ts1)
        ts2 = TrafficLight(ts1.red + ts1.yellow + ts1.green, self.defaultYellow, self.defaultGreen[1])
        self.signals.append(ts2)
        ts3 = TrafficLight(self.defaultRed, self.defaultYellow, self.defaultGreen[2])
        self.signals.append(ts3)
        ts4 = TrafficLight(self.defaultRed, self.defaultYellow, self.defaultGreen[3])
        self.signals.append(ts4)

        # Iniciar el ciclo del semáforo en otro hilo
        thread_repeat = threading.Thread(target=self.repeat)
        thread_repeat.daemon = True
        thread_repeat.start()

    def repeat(self):
        while True:
            # GREEN phase
            while self.signals[self.currentGreen].green > 0:
                self.updateValues()
                time.sleep(1)

            self.currentYellow = 1
            # YELLOW phase
            while self.signals[self.currentGreen].yellow > 0:
                self.updateValues()
                time.sleep(1)

            self.currentYellow = 0

            # Reset current signal
            self.signals[self.currentGreen].green = self.defaultGreen[self.currentGreen]
            self.signals[self.currentGreen].yellow = self.defaultYellow
            self.signals[self.currentGreen].red = self.defaultRed

            # Update signal cycle
            self.currentGreen = self.nextGreen
            self.nextGreen = (self.currentGreen + 1) % self.noOfSignals
            self.signals[self.nextGreen].red = self.signals[self.currentGreen].green + self.signals[self.currentGreen].yellow

    def updateValues(self):
        for i in range(self.noOfSignals):
            if i == self.currentGreen:
                if self.currentYellow == 0:
                    self.signals[i].green -= 1
                else:
                    self.signals[i].yellow -= 1
            else:
                self.signals[i].red -= 1