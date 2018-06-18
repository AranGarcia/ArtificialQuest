"""
Genetic algorithm module for artificial intelligence.
"""

import random
from constants import Heroes, Missions


class PathGenerator:
    def __init__(self, costs, starts):
        self.costs = costs
        self.starts = starts

    def generate_individual(self):
        """
        """

        # Helps keep track of which elements have already been used
        unchosen_heroes = [1, 2, 3, 4, 5, 6]
        unchosen_missions = [1, 2, 3, 4]
        chosen = []

        # Iterates while missions are still available
        # (A single hero may be assigned to all missions)
        while unchosen_missions:
            allele = []

            # Choosing a hero randomly
            hero_index = random.randint(0, len(unchosen_heroes) - 1)
            hero_id = unchosen_heroes.pop(hero_index)
            allele.append(Heroes(hero_id))

            # Choosing missions randomly
            amount = random.randint(0, len(unchosen_missions))
            for i in range(amount):
                miss_index = random.randint(0, len(unchosen_missions) - 1)
                miss_id = unchosen_missions.pop(miss_index)
                allele.append(Missions(miss_id))

            chosen.append(allele)


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
        self.chromosome = []
        for allele in assignments:
            # Index 0 is for the hero
            h = allele[0]
            self.chromosome.append(h.value)


def genetic_search(costs, starts, portal, gen_amount, pop_size):
    """
    Starts the search of possible solutions of the assignment of missions to heroes.

    costs:      A dictionary of matrices that represents the costs from a coordinate to another.
    starts:     List of all three starting points.
    pop_size:   Amount of individuals populating a generating.
    gen_amount: Total amount of iterations (generations) that the genetic search will 
                be doing.
    """
    pass


# Test
if __name__ == '__main__':
    pass
