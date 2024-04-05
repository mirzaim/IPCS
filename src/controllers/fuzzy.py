# python imports
import re
from math import degrees

# third-party imports
import scipy.integrate as integrate

# project imports
from world import World
from controllers import Controller


def triangular(start: float, center: float, end: float):
    def func(x):
        if x == center:
            return 1
        elif start < x < center:
            return (x - start)/(center - start)
        elif center < x < end:
            return 1 - (x - center)/(end - center)
        else:
            return 0
    return func


cp_set = {
    'left_far':   triangular(-10, -10, -5),
    'left_near':  triangular(-10, -2.5, 0),
    'stop':       triangular(-2.5, 0, 2.5),
    'right_near': triangular(0, 2.5, 10),
    'right_far':  triangular(5, 10, 10),
}

pv_set = {
    'cw_fast':  triangular(-20000, -200, -100),
    'cw_slow':  triangular(-200, -100, 0),
    'stop':  triangular(-100, 0, 100),
    'ccw_slow': triangular(0, 100, 200),
    'ccw_fast': triangular(100, 200, 20000),
}

cv_set = {
    'left_fast':  triangular(-500, -5, -2.5),
    'left_slow':  triangular(-5, -1, 0),
    'stop':       triangular(-1, 0, 1),
    'right_slow': triangular(0, 1, 5),
    'right_fast': triangular(2.5, 5, 500),
}

pa_set = {
    'up_more_right':   triangular(0, 30, 60),
    'up_right':        triangular(30, 60, 90),
    'up':              triangular(60, 90, 120),
    'up_left':         triangular(90, 120, 150),
    'up_more_left':    triangular(120, 150, 180),
    'down_more_left':  triangular(180, 210, 240),
    'down_left':       triangular(210, 240, 270),
    'down':            triangular(240, 270, 300),
    'down_right':      triangular(270, 300, 330),
    'down_more_right': triangular(300, 330, 360),
}

force_set = {
    'left_fast':  triangular(-100, -80, -60),
    'left_slow':  triangular(-80, -60, 0),
    'stop':       triangular(-60, 0, 60),
    'right_slow': triangular(0, 60, 80),
    'right_fast': triangular(60, 80, 100),
}


def read_fuzzy_rules(path: str):
    """convert text rules to python evaluable instructions"""
    with open(path) as f:
        data = f.read()

    data = re.search(r'RULEBLOCK.*?\n(.*?)\s*?END_RULEBLOCK',
                     data, re.DOTALL).group(1)
    data = re.sub(r'[\n\t]*', '', data)
    data = re.sub(r';', '\n', data)
    AND_OP = re.search(r'AND\s?:\s?(.*)', data).group(1).lower()
    OR_OP = re.search(r'OR\s?:\s?(.*)', data).group(1).lower()
    data = re.sub(r'RULE \d+:\s?IF\s?(.*?)\s?THEN\s?(.*)', r'\2 = \1', data)
    data = re.sub(r'([a-z_]+)\s?IS\s([a-z_]+)?',
                  r'fuzzification["\1"]["\2"]', data)
    fuzzy_rules = []
    for line in data.splitlines():
        if re.search(r' = ', line):
            line = re.sub(r'\(?([a-z_\[\]"]+)\)?\s?AND\s?\(?([a-z_\[\]"]+)\)?\s?AND\s?\(?([a-z_\[\]"]+)\)?',
                          r'_AND_OP(\1,\2,\3)', line)
            line = re.sub(r'_AND_OP', AND_OP, line)
            line = re.sub(
                r'\(?([a-z_\[\]"]+)\)?\s?AND\s?\(?([a-z_\[\]"]+)\)?', r'_AND_OP(\1,\2)', line)
            line = re.sub(r'_AND_OP', AND_OP, line)
            if 'OR' in line:
                line = re.sub(r'\s?OR\s?', r',', line)
                line = re.sub(r' = ', ' = ' + OR_OP + '(', line) + ')'
            fuzzy_rules.append(line)

    return fuzzy_rules


class FuzzyController(Controller):

    def __init__(self, fcl_path: str, **config):
        super().__init__(**config)
        self.fuzzy_rules = read_fuzzy_rules(fcl_path)

    def _make_input(self, world: World):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    def decide(self, world: World):
        world_inputs = self._make_input(world)

        # fuzzify inputs
        fuzzification = dict(
            cp=dict(
                map(lambda kv: (kv[0], kv[1](world_inputs['cp'])), cp_set.items())),
            pv=dict(
                map(lambda kv: (kv[0], kv[1](world_inputs['pv'])), pv_set.items())),
            cv=dict(
                map(lambda kv: (kv[0], kv[1](world_inputs['cv'])), cv_set.items())),
            pa=dict(
                map(lambda kv: (kv[0], kv[1](world_inputs['pa'] % 360)), pa_set.items())),
            force=dict(map(lambda kv: (kv[0], 0), force_set.items())),
        )

        # rule inference
        for rule in self.fuzzy_rules:
            res, exp = rule.split('=')
            exec(res + ' = max(' + res + ', ' + exp + ')', globals(), locals())

        # calculate center of mass for defuzzification
        s_mu = integrate.quad(lambda x: max(map(lambda k: min(force_set[k](x), fuzzification['force'][k]), force_set)),
                              -100, 100)[0]
        s_mu_x = integrate.quad(lambda x: x*max(map(lambda k: min(force_set[k](x), fuzzification['force'][k]), force_set)),
                                -100, 100)[0]

        s_mu = 1e-6 if s_mu == 0 else s_mu
        result = s_mu_x / s_mu

        return result

# class FuzzyController:

#     def __init__(self, fcl_path):
#         self.system = Reader().load_from_file(fcl_path)


#     def _make_input(self, world):
#         return dict(
#             cp = world.x,
#             cv = world.v,
#             pa = degrees(world.theta),
#             pv = degrees(world.omega)
#         )


#     def _make_output(self):
#         return dict(
#             force = 0.
#         )


#     def decide(self, world):
#         output = self._make_output()
#         self.system.calculate(self._make_input(world), output)
#         return output['force']
