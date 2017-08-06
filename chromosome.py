import random


class Chromosome:
    # LENGTH

    def __init__(self, data=None):
        if data is None:
            self.data = [self.random_element() for _n in range(self.LENGTH)]
        else:
            assert(len(data) == self.LENGTH)
            self.data = data

    def mutate(self, mask):
        return type(self)(
            data=list(self.mutate_data(mask))
        )

    def mutate_data(self, mask):
        for element, mask_point in zip(self.data, mask):
            yield self.random_element() if mask_point else element


class BinaryChromosome(Chromosome):
    def random_element(self):
        return random.choice([True, False])
