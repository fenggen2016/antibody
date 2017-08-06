import genome
import chromosome


class WormBinChromosome(chromosome.BinaryChromosome):
    LENGTH = 4


class WormGenome(genome.Genome):
    CHROMOSOMES = [
        (WormBinChromosome, dict())
    ]


worm = WormGenome()
print(worm.chromosomes[0].data)
print(worm.mutate([False, False, False, True]).chromosomes[0].data)
