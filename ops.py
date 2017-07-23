from common import random_element
from mutation import mutate
from crossover import crossover, two_point_crossover_mask
from init import initialize
from selection import select, ranking, pairs, tournament
import string


random_letter = random_element(
    list(
        string.ascii_lowercase + string.ascii_uppercase + string.punctuation + " ĄąĆćĘęŃńŚśÓóŁłŹźŻż"
    )
)


solution = "Zażółć gęślą jaźń"


def my_fitness(x):
    return sum(
        int(a != b) for a, b in zip(solution, x)
    )


population_size=500
population = initialize(
    population_size=population_size,
    length=len(solution),
    init_function=random_letter
)

elite_number = 4
n = 0
while True:
    n += 1
    print(n)
    parents = list(
        select(
            population,
            fitness_function=my_fitness,
            greater_better=False,
            select_function=tournament(2)   # ranking
        )
    )
    print("".join(parents[0]))
    if parents[0] == list(solution):
        break
#    elite = parents[:elite_number]

    children = []
    for a, b in pairs(parents):
        children.extend(
            crossover(a, b, two_point_crossover_mask)
        )

    mutated_children = [
        mutate(x, mutator=random_letter, rate=0.02)
        for x in children
    ]

    population = mutated_children # + elite
