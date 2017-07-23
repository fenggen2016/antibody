import math
import struct
import random
import abc
import enum
import itertools


def crossover(a, b, mask):
    x = a, b
    yield a.__class__([x[int(m)].data[i] for i, m in enumerate(mask)])
    yield b.__class__([x[int(not m)].data[i] for i, m in enumerate(mask)])


def mutate(a, mask):
    return [a.random_value() if m else x for x, m in zip(a.data, mask)]


def two_point_crossover(length):
    point1, point2 = sorted(random.randint(0, length) for _ in range(2))
    yield from itertools.repeat(True, point1)
    yield from itertools.repeat(False, point2 - point1)
    yield from itertools.repeat(True, length - point2)


class FitnessType(enum.Enum):
    MINIMALIZE = 1
    MAXIMALIZE = 2


def mutation_rate(rate):
    def mutation_mask(length):
        return (random.random() < rate for _ in range(length))
    return mutation_mask


class BaseDNA:
    def __init__(self, data=None):
        if data is None:
            self.data = self.initial_data()
        else:
            self.data = self.preprocess_data(data)

        self.data_length = len(self.data)

    @abc.abstractmethod
    def initial_data(self):
        pass

    def preprocess_data(self, data):
        return data


def arrayed_dna(base_type, length):
    class ArrayedDNA(base_type):
        def initial_data(self):
            return [self.random_value() for _ in range(length)]

    return ArrayedDNA


class BinaryDNA(BaseDNA):
    @staticmethod
    def random_value():
        return random.choice([True, False])

    def preprocess_data(self, data):
        if isinstance(data, str):
            return [bool(int(x)) for x in data]
        else:
            return [bool(x) for x in data]

    def __str__(self):
        return "".join([str(int(x)) for x in self.data])


class Binary8DNA(arrayed_dna(BinaryDNA, 8)):
    def score(self):
        return sum(x == y for x, y in zip(self.data, [1, 1, 1, 1, 0, 0, 0, 0]))


class Simulation:
    def __init__(self, population_size, fitness_function, fitness_type, generator, crossover_mask, mutation_mask):
        self.population_size = population_size
        self.fitness_function = fitness_function
        self.fitness_type = fitness_type
        self.generator = generator
        self.crossover_mask = crossover_mask
        self.mutation_mask = mutation_mask

    def initial_population(self):
        return [self.generator() for _ in range(self.population_size)]

    def calculate_scores(self, population):
        for member in population:
            yield (
                self.fitness_function(member),
                member
            )

    def step(self, population):
        scored_population = sorted(
            self.calculate_scores(population),
            reverse=True if self.fitness_type==FitnessType.MAXIMALIZE else False,
            key=lambda x: x[0]
        )

        i = iter(population)
        parents = zip(i, i)

        for p1, p2 in parents:
            mask = self.crossover_mask(p1.data_length)
            for child in crossover(p1, p2, mask):
                yield mutate(child, self.mutation_mask(child.data_length))


sim = Simulation(
    generator=Binary8DNA,
    fitness_function=Binary8DNA.score,
    fitness_type=FitnessType.MAXIMALIZE,
    population_size=100,
    crossover_mask=two_point_crossover,
    mutation_mask=mutation_rate(0.05)
)

population = sim.initial_population()
while True:
    population = list(sim.step(population))
