import random


def random_element(elements):
    """
    Returns random element from list.
    """
    def function(_current=None):
        return random.choice(elements)

    return function


def random_bit(_current=None):
    """
    Returns True/False randomly.
    """
    return random_element([True, False])


def random_int(minimum, maximum):
    """
    Returns random int in specified range.
    """
    def func(_current=None):
        return random.randint(minimum, maximum)

    return func


def random_float(minimum=0.00, maximum=1.00):
    """
    Returns random float in specified range (default=0.00-1.00).
    """
    def func(_current=None):
        return random.uniform(minimum, maximum)

    return func
