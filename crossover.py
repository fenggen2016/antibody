import random
import itertools


def one_point_crossover_mask(length):
    point = random.randint(1, length-1)
    yield from itertools.repeat(True, point)
    yield from itertools.repeat(False, length - point)


def two_point_crossover_mask(length):
    p1, p2 = sorted(random.sample(range(1, length-1), k=2))
    yield from itertools.repeat(True, p1)
    yield from itertools.repeat(False, p2-p1)
    yield from itertools.repeat(True, length - p2)


def uniform_crossover_mask(length):
    return (random.choice([True, False]) for _ in range(length))


def crossover(a, b, mask):
    if callable(mask):
        mask = list(mask(len(a)))

    yield [
        a[i] if m else b[i]
        for i, m in enumerate(mask)
    ]

    yield [
        b[i] if m else a[i]
        for i, m in enumerate(mask)
    ]
