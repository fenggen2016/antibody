import math
import struct
import random
import abc


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
    def __init__(self, population_size, fitness_function, generator):
        self.population_size = population_size
        self.fitness_function = fitness_function
        self.generator = generator

        self.population = [self.generator() for _ in range(self.population_size)]


sim = Simulation(
    generator=Binary8DNA,
    fitness_function=Binary8DNA.score,
    population_size=100
)

print(sim.population[0])
exit(0)


def mutate(a, probability=1.0):
    a = list(a)
    if random.random() <= probability:
        x = random.choice(range(len(a)))
        a[x] = (a[x] + 1) % 2

    return a


def split(a, points):
    result = []

    i = 0
    for p in points:
        result.append(a[i:p+1])
        i += p+1-i

    if i < len(a):
        result.append(a[i:])

    return result


def crossover(a, b, points=1):
    pts = sorted(random.sample(range(len(a)-1), points))
    portions = [
        split(a, pts),
        split(b, pts)
    ]

    parts = range(len(portions[0]))

    return [
        sum((portions[x % 2][x] for x in parts), []),
        sum((portions[(x+1) % 2][x] for x in parts), [])
    ]


def int2bits(i, pad=32):
    bits = [int(b) for b in bin(i)[2:]]
    return ((pad-len(bits)) * [0]) + bits


def bits2int(b):
    return int(
        "".join([str(x) for x in b]),
        2
    )


def float2bits(f):
    s = struct.pack('>f', f)
    i = struct.unpack('>l', s)[0]
    return [int(x) for x in bin(i)[2:]]


def bits2float(b):
    i = int("".join([str(x) for x in b]), 2)
    s = struct.pack('>l', i)
    return struct.unpack('>f', s)[0]


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def is_correct(x):
    return not math.isnan(bits2float(x))


n = 1000
wanted = 100
population = []
while (len(population) != n):
    a = [random.randint(0, 1) for x in range(31)]
    population.append(a)


def fitness(x, wanted):
    v = bits2int(x)
    return abs(wanted - v)


c = 0
while True:
    c += 1

    # best ones
    population = sorted(
        population,
        key=lambda x: fitness(x, wanted)
    )
    # remove bad ones
    population = population[:n]
    print(bits2int(population[0]))

#    fits = [fitness(x, wanted) for x in population]
#    worst = max(fits)
#    sss = sum(fits)
#    weights = [(worst-x+1.0)/(sss+1.0) for x in fits]

#    i = weights.index(max(weights))
#    b = bits2int(population[i])
#    print(b)

#    population = random.choices(population, weights=weights, k=n)

    # crossover
#    random.shuffle(population)
    elites = 100

    new_population = population[0:elites]

    for chunk in chunks(population[elites:], 2):
        #if random.random() < 0.2:
        new_population.extend(crossover(chunk[0], chunk[1], points=1))
#        else:
        new_population.extend(chunk)

    population = new_population
#    print(len(population))

    # mutate
    population = [mutate(x) for x in population]
