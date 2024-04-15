# third-party imports
import pytest

# project imports
from world import World
from simulator import Simulator

from utils import relative_error, EPSILON


@pytest.mark.parametrize("dt", [-1.0, -0.1, 0.0])
def test_exception(dt):
    with pytest.raises(ValueError):
        world = World()
        sim = Simulator(world)
        sim.tick(dt)


@pytest.mark.parametrize("x_0, theta_0, x_1, theta_1", [
    (0., 0., 0., 6.185),
    (5., 0., 5., 6.185),
    (0., -90., 0., 4.712),
])
def test_tick(x_0, theta_0, x_1, theta_1):

    world = World(x=x_0, theta=theta_0)
    sim = Simulator(world)
    sim.tick(0.1)

    assert relative_error(sim.world.x, x_1) < EPSILON
    assert relative_error(sim.world.theta, theta_1) < EPSILON
