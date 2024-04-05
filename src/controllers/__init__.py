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
    if name not in list_of_controllers:
        raise ValueError(f"Controller {name} not found")

    return list_of_controllers[name](**config)
