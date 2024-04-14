# python imports
from math import pi

# third-party imports
import pytest
import pandas as pd

# project imports
from main import main
from conf import ConfigReader


EPSILON = 0.05


def relative_error(observed, expected):
    if expected == 0:
        return abs(observed)
    return abs((observed - expected) / expected)


@pytest.fixture(scope="session")
def csv_file_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / 'output.csv'
    return str(path)


def make_config(force, x, theta, m, M, l, sim_time=40.0):
    return f"""
[simulator]
name = file
dt = 0.1
simulation_time = {sim_time}
output_file = %%csv_file%%

[controller]
name = fuzzy
fcl_path = src/configs/controllers/fuzzy_logic/complex.fcl


[world]
force = {force}
x = {x}
theta = {theta}

m = {m}
M = {M}
l = {l}
"""


@pytest.mark.parametrize('configs, exception', [
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 1.0, 1.0), False),
    (make_config('abc', 0.0, -90.0, 16.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 'abc', -90.0, 16.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, 'abc', 16.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 'abc', 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, 'abc', 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 'abc', 1.0), True),
    (make_config(0.0, 0.0, -90.0, -16.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, -80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, -1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 100.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, 100.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 50.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 5.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 0.0, -90.0, 90.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, -20.0, -90.0, 16.0, 80.0, 1.0, 1.0), True),
    (make_config(0.0, 20.0, -90.0, 16.0, 80.0, 1.0, 1.0), True),
])
def test_input_1(configs, exception, csv_file_path):
    configs = configs.replace('%%csv_file%%', csv_file_path)
    conf = ConfigReader(conf_str=configs)
    if exception:
        with pytest.raises(ValueError):
            main(conf)
    else:
        main(conf)


@pytest.mark.parametrize('configs, theta, x', [
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, 0.25,),
    (make_config(0.0, -5.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, -4.75,),
    (make_config(0.0, +5.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, 5.25,),
    (make_config(0.0, 0.0, 0.0, 16.0, 80.0, 1.0, 5.0), 6.0, 0.08,),
    (make_config(0.0, 0.0, -45.0, 16.0, 80.0, 1.0, 5.0), 2.5, -0.3,),
    (make_config(0.0, 0.0, -90.0, 30.0, 80.0, 1.0, 5.0), 1.5, 0.8,),
    (make_config(0.0, 0.0, -90.0, 16.0, 50.0, 1.0, 5.0), 1.45, 1.3,),
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 20.0, 5.0), 5.0, 0.25,),
    (make_config(+5.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 2.7, 0.65,),
    (make_config(-5.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.5, 0.0,),
])
def test_sim_1(configs, theta, x, csv_file_path):
    configs = configs.replace('%%csv_file%%', csv_file_path)
    conf = ConfigReader(conf_str=configs)

    main(conf)

    sim = pd.read_csv(csv_file_path)
    observed_theta, observed_x = sim['theta'].iloc[-1], sim['x'].iloc[-1]

    assert relative_error(observed_theta, theta) < EPSILON
    assert relative_error(observed_x,  x) < EPSILON


@pytest.mark.parametrize('configs', [
    make_config(0.0, 0.0, -90.0, 16.0, 80.0, 1.0),
    make_config(0.0, -5.0, -90.0, 16.0, 80.0, 1.0),
    make_config(0.0, +5.0, -90.0, 16.0, 80.0, 1.0),
    make_config(0.0, 0.0, 0.0, 16.0, 80.0, 1.0),
    make_config(0.0, 0.0, -45.0, 16.0, 80.0, 1.0),
    make_config(0.0, 0.0, -90.0, 30.0, 80.0, 1.0),
    make_config(0.0, 0.0, -90.0, 16.0, 50.0, 1.0),
    make_config(0.0, 0.0, -90.0, 16.0, 80.0, 20.0),
    make_config(+5.0, 0.0, -90.0, 16.0, 80.0, 1.0),
    make_config(-5.0, 0.0, -90.0, 16.0, 80.0, 1.0),
])
def test_control_1(configs, csv_file_path):
    configs = configs.replace('%%csv_file%%', csv_file_path)
    conf = ConfigReader(conf_str=configs)

    main(conf)

    dt = conf.simulation_config()['dt']
    sim = pd.read_csv(csv_file_path)['theta']

    assert sim.tail(int(10 / dt)).between(pi/3, 2*pi/3).all()


@pytest.mark.parametrize('configs, theta, x', [
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, 0.25,),
    (make_config(0.0, -5.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, -4.75,),
    (make_config(0.0, +5.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.0, 5.25,),
    (make_config(0.0, 0.0, 0.0, 16.0, 80.0, 1.0, 5.0), 6.0, 0.08,),
    (make_config(0.0, 0.0, -45.0, 16.0, 80.0, 1.0, 5.0), 2.5, -0.3,),
    (make_config(0.0, 0.0, -90.0, 30.0, 80.0, 1.0, 5.0), 1.5, 0.8,),
    (make_config(0.0, 0.0, -90.0, 16.0, 50.0, 1.0, 5.0), 1.45, 1.3,),
    (make_config(0.0, 0.0, -90.0, 16.0, 80.0, 20.0, 5.0), 5.0, 0.25,),
    (make_config(+5.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 2.7, 0.65,),
    (make_config(-5.0, 0.0, -90.0, 16.0, 80.0, 1.0, 5.0), 5.5, 0.0,),
])
def test_acc_1(configs, theta, x, csv_file_path):
    configs = configs.replace('%%csv_file%%', csv_file_path)
    conf = ConfigReader(conf_str=configs)

    main(conf)

    sim = pd.read_csv(csv_file_path)
    observed_theta, observed_x = sim['theta'].iloc[-1], sim['x'].iloc[-1]

    assert relative_error(observed_theta, theta) < EPSILON
    assert relative_error(observed_x,  x) < EPSILON
