# project imports
from controllers.base import Controller
from controllers.fuzzy import FuzzyController
from controllers.pid import PIDController

list_of_controllers = {
    "base": Controller,
    "fuzzy": FuzzyController,
    "pid": PIDController,
}

def get_controller(name, **config):
    return list_of_controllers[name](**config)

