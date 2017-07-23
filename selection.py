import random


def pairs(population):
    iterator = iter(population)
    for a, b in zip(iterator, iterator):
        yield (a, b)


def ranking(population, scores, greater_better):
    scored_population = [
        (score, member) for score, member in zip(scores, population)
    ]

    population = sorted(
        scored_population,
        reverse=greater_better,
        key=lambda member: member[0]
    )

    return [x[1] for x in population]


def tournament(tournament_size):
    def tournament_selector(population, scores, greater_better):
        win_function = max if greater_better else min

        num_parents = len(population)
        scored_population = [
            (score, member) for score, member in zip(scores, population)
        ]

        for _ in range(num_parents):
            sample = random.sample(scored_population, tournament_size)
            best = win_function(
                sample,
                key=lambda x: x[0]
            )

            yield best[1]

    return tournament_selector


def select(population, fitness_function, select_function, greater_better=True):
    scores = [fitness_function(x) for x in population]
    return select_function(population, scores, greater_better)
