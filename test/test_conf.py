# third-party imports
import pytest

# project imports
from conf import ConfigReader


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        ConfigReader('/complex.fcl')


def test_no_input_exception():
    with pytest.raises(ValueError):
        ConfigReader()
