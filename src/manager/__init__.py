# project imports
from manager.base import Manager
from manager.gui import GUI
from manager.file import FileOutput

list_of_managers = {
    "base": Manager,
    "gui": GUI,
    "file": FileOutput,
}


def get_manager(name, **config):
    if name not in list_of_managers:
        raise ValueError(f"Manager {name} not found")

    return list_of_managers[name](**config)
