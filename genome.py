class Genome:
    def __init__(self, chromosomes=None):
        if chromosomes is None:
            self.chromosomes = []

            for description in self.CHROMOSOMES:
                self.chromosomes.append(
                    description[0](
                        **description[1]
                    )
                )
        else:
            self.chromosomes = chromosomes

    def mutate(self, mask):
        x = 0

        chromosomes = []
        for index, description in enumerate(self.CHROMOSOMES):
            chromosomes.append(
                description[0](
                    data=list(
                        self.chromosomes[index].mutate_data(
                            mask[x:description[0].LENGTH+x+1]
                        )
                    ),
                    **description[1]
                )
            )

            x += description[0].LENGTH

        return type(self)(chromosomes)
