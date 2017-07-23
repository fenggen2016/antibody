import random


def flip_bit(bit):
    """
    Negates bit.
    """
    return not bit


def mutate(a, rate, mutator=flip_bit):
    """
    Mutates chromosome using selected mutator as specified rate.
    """
    return [
        mutator(bit) if random.random() < rate else bit
        for bit in a
    ]
