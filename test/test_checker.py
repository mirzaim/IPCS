# third-party imports
import pytest

# project imports
from checker import WorldChecker


@pytest.mark.parametrize('conf', [
    {'m': 0},
    {'M': -1},
    {'force': 'abd'},
])
def test_conf(conf):
    checker = WorldChecker()
    with pytest.raises(ValueError):
        checker.check(conf)

