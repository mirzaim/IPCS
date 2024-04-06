# project imports
from conf import ConfigReader
from world import World
from controllers import get_controller
from manager import get_manager


conf = ConfigReader()

if __name__ == '__main__':
    world = World(**conf.world_config())
    controller = get_controller(**conf.controller_config())
    # use 'gui' or 'file' as argument
    manager = get_manager('gui', world=world, controller=controller, **conf.simulation_config())
    manager.run()
