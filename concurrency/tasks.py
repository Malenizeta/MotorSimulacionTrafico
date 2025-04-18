import threading
from simulation.simulator import Simulator

def run_simulation_in_thread():
    simulator = Simulator()
    threading.Thread(target=simulator.run, daemon=True).start()