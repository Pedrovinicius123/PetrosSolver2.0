from collections import defaultdict
from src.clause import read_cnf_file, generate_random_3SAT
from src.solver import parse_formula, solve
from rich.pretty import pprint
from time import time # for tests

import numpy as np
import pycosat, timeit # for tests
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

    with open('log.txt', 'w') as file:
        file.write(f'Mediana: {np.median(times)}')
        file.write(f'Média: {np.mean(times)}')
        file.write(f'Desvio Padrão: {np.std(times)}')


def test_with_formula(filename):
    CNF = read_cnf_file(filename)

    print(pycosat.solve(CNF))

    a = time()
    implications = parse_formula(CNF, defaultdict(list))
    result = solve(implications)
    print(result)
    b = time()

    pprint(test(CNF, result))
    print(f'TIME PETROS SOLVER: {b-a}')

if __name__ == "__main__":
    CNF = generate_random_3SAT(200, 200)
    a = time()
    print(pycosat.solve(CNF))
    b = time()
    implications = parse_formula(CNF, defaultdict(list))
    result = solve(implications)
    pprint(result)
    c = time()

    pprint(test(CNF, list(map(lambda x:-x if not result[x] else x, result))))
    print(f'TIME PETROS SOLVER: {b-a}', f'TIME PYCOSAT {c-b}')
