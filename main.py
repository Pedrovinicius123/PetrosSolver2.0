from collections import defaultdict
from src.clause import read_cnf_file, generate_random_3SAT
from src.solver import parse_formula, solve
from pysat.solvers import Minisat22
from rich.pretty import pprint
from time import time

import pycosat # for tests
import random, timeit
import matplotlib.pyplot as plt

def test(formula, assignment):
    for clause in formula:
        found = False

        for literal in assignment:
            if literal in clause:
                found = True
                break

        if not found:
            return False

    return True

def test_complexity():
    times, sizes = [], []
    for i in range(20, 200):
        for j in range(20, 200):
            setup = f"""
from src.clause import generate_random_3SAT
from src.solver import parse_formula, solve
from collections import defaultdict

CNF = generate_random_3SAT({i}, {j})
implications = parse_formula(CNF, defaultdict(list))
"""
            times.append(timeit.timeit('solve(implications)', setup=setup, number=1))
            sizes.append(i * j)

    plt.scatter(sizes, times)
    plt.show()


if __name__ == '__main__':
    CNF = generate_random_3SAT(200, 1000)
    implications = parse_formula(CNF, defaultdict(list))

    result = solve(implications)
    
    print(result)
    pprint(test(result))
