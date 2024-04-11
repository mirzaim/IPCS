# python imports
import sys
import configparser


def to_float(value):
    try:
        return float(value)
    except ValueError:
        return value


class ConfigReader:

    def __init__(self):
        cfg_path = "configs/default.ini" if len(sys.argv) < 2 else sys.argv[1]
        self.cfg = configparser.ConfigParser()
        self.cfg.optionxform = str
        self.cfg.read(cfg_path)

    def simulation_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('simulator')}

    def controller_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('controller')}

    def world_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('world')}
