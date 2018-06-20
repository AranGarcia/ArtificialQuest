"""
Genetic algorithm module for artificial intelligence.
"""

import random
from constants import Heroes, Missions


class PathGenerator:
    def __init__(self, costs, starts):
        # Set costs a class variable so that PathIndividual may have acces
        # without an instance
        PathGenerator.set_costs(costs)
        # self.starts = starts
        # self.hero_ids = dict(
        #     (index, Heroes[name].value) for index, name in enumerate(costs.keys()))
        self.hero_ids = [Heroes[name].value for name in costs.keys()]

    def generate_individual(self):
        unchosen_missions = ["KEY", "STONES", "TEMPLE", "FRIEND"]

        config = [
            [self.hero_ids[i], random.randint(1, 3)] for i in range(3)
        ]

        for um in unchosen_missions:
            index = random.randint(0, 2)
            config[index].append(um)

        return PathIndividual(config)

    def populate(self, pop_size):
        return [self.generate_individual() for i in range(pop_size)]

    @staticmethod
    def crossover(inda, indb):
        """
        Make individual A reproduce with individual B and form a new individual using the 
        crossover method of their chromosomes.
        """
        # It might be possible that the left subportion of the chromosome might
        # be from individual B and not always A.
        if random.random() > 0.5:
            inda, indb = indb, inda

        index = random.randint(1, 16)
        new_chrom = []
        new_chrom.extend(inda[:index])
        new_chrom.extend(indb[index:])

    @classmethod
    def set_costs(cls, costs):
        cls.costs = costs

    @classmethod
    def get_cost(cls, hero_id, start, goal):
        return cls.costs[Heroes(hero_id).name][start][goal].acc_cost


def key_sort(i): return i.cost


class PathIndividual:
    """
    The individual that represents a possible solution to the assignment of
    paths to an objective in the genetic search. 

    The chromosome representation for the individual is
    [I_1, S, M_1_1, M_1_2, M_1_3, M_1_4,..., I_3, S, M_3_1, M_3_2, M_3_3, M_3_4]
     0    1  2      3      4      5

    where I_i is the individual i, M_i_j is the j-th mission assigned to indvidual i where 
    i is a value from 1 to 3 and j is a value from 1 to 5 as represented in the enumerations
    defined in constants.py.
    """

    def __init__(self, assignments):
        if len(assignments) != 3:
            raise ValueError('invalid format of assignments', assignments)

        self.chromosome = []
        for allele in assignments:
            allele.extend([None for i in range(6 - len(allele))])
            self.chromosome.extend(allele)

        self.cost = self.__calculate_cost(self.chromosome)
        self.fitness = 0

    def __calculate_cost(self, chrom):
        """
        Calculates the cost of the paths using the costs stored in the PathGenerator
        class. 
        """
        cost = 0

        # Hero 1 costs
        for i in range(2, 6):
            if chrom[i] is None:
                if i > 2:
                    cost += PathGenerator.get_cost(
                        chrom[0], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[0], chrom[i - 1], chrom[i])

        # Hero 2 costs
        for i in range(8, 12):
            if chrom[i] is None:
                if i > 8:
                    cost += PathGenerator.get_cost(
                        chrom[6], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[6], chrom[i - 1], chrom[i])

        # Hero 3 costs
        for i in range(14, 18):
            if chrom[i] is None:
                if i > 14:
                    cost += PathGenerator.get_cost(
                        chrom[12], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[12], chrom[i - 1], chrom[i])

        return cost

    def mutate(self):
        found = False
        selectable = [2, 3, 4, 5, 8, 9, 10, 11, 14, 15, 16, 17]

        # Find an empty space
        while not found:
            index = random.choice(selectable)

            if self.chromosome[index] is None:
                index_1 = index
                found = True

                # Remove the range from which the index_1 was chosen
                if 2 <= index_1 <= 5:
                    remove = set([2, 3, 4, 5])
                elif 8 <= index_1 <= 11:
                    remove = set([8, 9, 10, 11])
                else:
                    remove = set([14, 15, 16, 17])

                selectable = [s for s in selectable if s not in remove]

        found = False

        # Find a space with mission
        while not found:
            index = random.choice(selectable)

            if self.chromosome[index]:
                index_2 = index
                found = True

        print("Before:", self.chromosome)
        temp = self.chromosome[index_1]
        self.chromosome[index_1] = self.chromosome[index_2]
        self.chromosome[index_2] = temp
        print("After:", self.chromosome)

    def clone(self):
        return PathIndividual([
            self.chromosome[0:6], self.chromosome[6:12], self.chromosome[12:]
        ])

    def is_consistent(self):
        missions = set()

        for i in range(0, 3):
            for j in range(2, 6):
                m = self.chromosome[j + 6 * i]

                if m is None:
                    break

                if m in missions:
                    return False

                missions.add(m)

        if len(missions) != 4:
            return False

        return True


class Roulette:
    def __init__(self, distribution):
        pass


def genetic_search(costs, starts, gen_amount=30, pop_size=10):
    """
    Starts the search of possible solutions of the assignment of missions to heroes.

    costs:      A dictionary of matrices that represents the costs from a coordinate to another.
    starts:     List of all three starting points.
    pop_size:   Amount of individuals populating a generating.
    gen_amount: Total amount of iterations (generations) that the genetic search will 
                be doing.
    """

    pg = PathGenerator(costs, starts)

    population = []

    for i in range(gen_amount):
        print("Generation #", i + 1)

        # Populate
        population.extend(pg.populate(10 - len(population)))

        # Evaluate fitness and mark inconsistent individuals
        total = 0
        to_be_removed = []
        for index, p in enumerate(population):
            if not p.is_consistent():
                to_be_removed.insert(0, index)
            else:
                total += p.cost

        # Removing inconsistent
        for tbr in to_be_removed:
            population.pop(tbr)

        # Create a fitness roulette
        dist = [0]
        for ind, p in enumerate(population):
            p.fitness = p.cost / total
            dist.append(p.fitness + dist[ind])

        # Mutate, instead of reproducing
        new_gen = []
        for p in population:
            offspring = p.clone()
            offspring.mutate()
            new_gen.append(offspring)
    
        population.extend(new_gen)

        population.sort(key=key_sort)

        population = population[:10]

        for p in population:
            print('\tCost:', p.cost, 
            
            
            p.chromosome)

        population = population[:6]

    return population[0]
