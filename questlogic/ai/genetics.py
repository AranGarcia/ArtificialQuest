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
            [self.hero_ids[i], random.randint(1, 3) ] for i in range(3)
        ]

        for um in unchosen_missions:
            index = random.randint(0, 2)
            config[index].append(um)
        
        return PathIndividual(config)

    def populate(self, pop_size):
        return [self.generate_individual() for i in range(pop_size)]

    @classmethod
    def set_costs(cls, costs):
        cls.costs = costs

    @classmethod
    def get_cost(cls, hero_id, start, goal):
        return cls.costs[Heroes(hero_id).name][start][goal].acc_cost


class PathIndividual:
    """
    The individual that represents a possible solution to the assignment of
    paths to an objective in the genetic search. 

    The chromosome representation for the individual is
    [I_1, S, M_1_1, M_1_2, M_1_3,..., I_3, S, M_3_1, M_3_2, M_3_3]

    where I_i is the individual i, M_i_j is the j-th mission assigned to indvidual i where 
    i is a value from 1 to 3 and j is a value from 1 to 5 as represented in the enumerations
    defined in constants.py.
    """

    def __init__(self, assignments):
        if len(assignments) != 3:
            raise ValueError('invalid format of assignments', assignments)

        self.chromosome = []
        for allele in assignments:
            # Index 0 is for the hero
            allele.extend([None for i in range(6 - len(allele))])
            self.chromosome.extend(allele)
        
        self.cost = self.__calculate_cost(self.chromosome)

    def __calculate_cost(self, chrom):
        cost = 0

        # Hero 1 costs
        for i in range(2, 6):
            if chrom[i] is None:
                if i > 2:
                    cost += PathGenerator.get_cost(chrom[0], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[0], chrom[i - 1], chrom[i])

        # Hero 2 costs
        for i in range(8, 12):
            if chrom[i] is None:
                if i > 8:
                    cost += PathGenerator.get_cost(chrom[6], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[6], chrom[i - 1], chrom[i])

        # Hero 3 costs
        for i in range(14, 18):
            if chrom[i] is None:
                if i > 14:
                    cost += PathGenerator.get_cost(chrom[12], chrom[i - 1], "PORTAL")
                break
            cost += PathGenerator.get_cost(chrom[12], chrom[i - 1], chrom[i])
        
        return cost


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

    pop = pg.populate(pop_size)

    for p in pop:
        print(p.chromosome, p.cost)

    for i in range(gen_amount):
        # Populate
        # Remove unfit
        # Reproduce
        # Mutate
        pass
