# project imports
from world import World


class WorldChecker:
    def __init__(self):
        self.checks = [self.check_m, self.check_M, self.check_l,
                       self.check_m_M, self.check_x]

    def check_type(self, confs: dict):
        for key, value in confs.items():
            if not isinstance(value, float):
                raise ValueError(f"Input Value {key} Should be a float.")

    def check_m(self, world: World):
        if not (0.0 <= world.m <= 80.0):
            raise ValueError("m should be between 0.0 and 80.0.")

    def check_M(self, world: World):
        if not (0.0 <= world.M <= 80.0):
            raise ValueError("M should be between 0.0 and 80.0.")

    def check_l(self, world: World):
        if not (0.5 <= world.l <= 20.0):
            raise ValueError("l should be between 0.5 and 20.0.")

    def check_m_M(self, world: World):
        if not (world.M / 5 <= world.m <= world.M):
            raise ValueError("M / 5 <= m <= M.")

    def check_x(self, world: World):
        if not (world.min_x <= world.x <= world.max_x):
            raise ValueError("min_x <= x <= max_x.")

    def check(self, world_config: dict):
        self.check_type(world_config)
        world = World(**world_config)
        for check in self.checks:
            check(world)
        return world
