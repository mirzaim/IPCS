# project imports
from world import World
from controllers import Controller


class PIDController(Controller):

    def __init__(self, **config):
        super().__init__(**config)
