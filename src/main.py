# project imports
from conf import ConfigReader
from world import World
from controllers import get_controller
from manager import Manager


conf = ConfigReader()

if __name__ == '__main__':
    world = World(**conf.world_config())
    controller = get_controller(**conf.controller_config())
    manager = Manager(world, controller, **conf.simulation_config())
    manager.run()
