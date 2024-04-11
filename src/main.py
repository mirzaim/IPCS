# python imports
from copy import deepcopy

# project imports
from conf import ConfigReader
from world import World
from simulator import Simulator
from controllers import get_controller
from manager import get_manager


conf = ConfigReader()

if __name__ == '__main__':
    world = World(**conf.world_config())
    simulator = Simulator(deepcopy(world))
    controller = get_controller(**conf.controller_config())
    manager = get_manager(simulator=simulator, controller=controller,
                          **conf.simulation_config())
    manager.run()
