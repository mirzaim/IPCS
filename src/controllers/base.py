# project imports
from world import World


class Controller:

    def __init__(self, **config):
        self.config = config

    def decide(self, world: World):
        raise NotImplementedError
