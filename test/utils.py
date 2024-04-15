

EPSILON = 0.05


def relative_error(observed, expected):
    if expected == 0:
        return abs(observed)
    return abs((observed - expected) / expected)
