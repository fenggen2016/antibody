def initialize(population_size, length, init_function):
    if population_size % 2 == 1:
        raise ValueError("Population size must be even number.")

    return [
        [init_function() for _ in range(length)]
        for _ in range(population_size)
    ]
