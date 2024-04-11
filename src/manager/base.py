# project imports
from simulator import Simulator
from controllers import Controller
from world import World


class Manager:

    def __init__(self, simulator: Simulator, controller: Controller, dt=0.1, **config):
        self.dt = dt
        self.controller = controller
        self.simulator = simulator

    def resume(self):
        raise NotImplementedError

    def draw(self, world: World):
        raise NotImplementedError

    def wait(self):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError

    def run(self):
        try:
            while self.resume():
                force = self.controller.decide(self.simulator.world)

                self.simulator.apply_force(force)
                self.simulator.tick(self.dt)

                self.draw(self.simulator.world)
                self.wait()
        finally:
            self.quit()
            print("Simulation ended")
