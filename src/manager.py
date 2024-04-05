# python imports
from copy import deepcopy

# project imports
from simulator import Simulator
from controllers import Controller
from world import World
from gui import GUI


class Manager:

    def __init__(self, world: World, controller: Controller, 
                 dt=0.1, fps=60, monitor_width=1200, monitor_height=300):
        self.dt = dt
        self.fps = fps
        self.controller = controller

        self.simulator = Simulator(deepcopy(world))
        self.gui = GUI(monitor_width, monitor_height)

    def run(self):
        while not self.gui.check_close():
            force = self.controller.decide(self.simulator.world)

            self.simulator.apply_force(force)
            self.simulator.tick(self.dt)

            self.gui.draw(self.simulator.world)
            self.gui.clock.tick(self.fps)
