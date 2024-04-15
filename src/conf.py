# python imports
import configparser
from pathlib import Path


def to_float(value):
    try:
        return float(value)
    except ValueError:
        return value


class ConfigReader:

    def __init__(self, file_path=None, conf_str=None):
        if file_path is None and conf_str is None:
            raise ValueError("Either file_path or conf_str must be provided.")

        if file_path is not None and not Path(file_path).is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.cfg = configparser.ConfigParser()
        self.cfg.optionxform = str
        if file_path is not None:
            self.cfg.read(file_path)
        elif conf_str is not None:
            self.cfg.read_string(conf_str)

    def simulation_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('simulator')}

    def controller_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('controller')}

    def world_config(self):
        return {item: to_float(value) for item, value in self.cfg.items('world')}
