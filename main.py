from src.clause import read_cnf_file, generate_random_3SAT
from src.solver import parse_formula, solve
from rich.pretty import pprint
from time import time # for tests

import pycosat # for tests
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
    CNF = read_cnf_file('sample4')

    a = time()
    implications = parse_formula(CNF, defaultdict(list))
    result = solve(implications)
    b = time()

    print(result)
    c = time()
    pycosat_result = pycosat.solve(CNF)
    d = time()
    
    print(pycosat_result)

    pprint(test(CNF, result))
    print(f'TIME PYCOSAT: {d-c}', f'TIME PETROS SOLVER: {b-a}')
