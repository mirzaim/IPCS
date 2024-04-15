# third-party imports
import pytest

# project imports
from world import World
from controllers import FuzzyController

from utils import relative_error, EPSILON


@pytest.mark.parametrize('world_conf, expected_force', [
    ({}, 0.0),
    ({'theta': -90.}, 80.),
    ({'x': 3., 'theta': 90.}, 0.),
    ({'theta': 45.}, 80.),
])
def test_fuzzy(world_conf, expected_force):
    world = World(**world_conf)
    contoller = FuzzyController('src/configs/controllers/fuzzy_logic/complex.fcl')
    force = contoller.decide(world)

    assert relative_error(force, expected_force) < EPSILON
