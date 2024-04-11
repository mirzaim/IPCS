# python imports
from math import pi

# third-party imports
import pytest
import pandas as pd

# project imports
from main import main
from conf import ConfigReader


@pytest.fixture(scope="session")
def csv_file_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / 'output.csv'
    return str(path)


@pytest.mark.parametrize('configs', [
    """
[simulator]
name = file
dt = 0.1
simulation_time = 30.0
output_file = %%csv_file%%

[controller]
name = fuzzy
fcl_path = src/configs/controllers/fuzzy_logic/complex.fcl


[world]
theta = -90.0
""",
    """
[simulator]
name = file
dt = 0.1
simulation_time = 30.0
output_file = %%csv_file%%

[controller]
name = fuzzy
fcl_path = src/configs/controllers/fuzzy_logic/complex.fcl


[world]
theta = -90.0
x = -5.0
""",
    """
[simulator]
name = file
dt = 0.1
simulation_time = 30.0
output_file = %%csv_file%%

[controller]
name = fuzzy
fcl_path = src/configs/controllers/fuzzy_logic/complex.fcl


[world]
theta = -90.0
x = -5.0
v = 5.0
"""])
def test_main(configs, csv_file_path):
    configs = configs.replace('%%csv_file%%', csv_file_path)
    conf = ConfigReader(conf_str=configs)

    main(conf)

    dt = conf.simulation_config()['dt']
    sim = pd.read_csv(csv_file_path)['theta']

    assert sim.tail(int(10 / dt)).between(pi/3, 2*pi/3).all()
