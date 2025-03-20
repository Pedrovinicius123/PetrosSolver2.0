import os
import random

def read_cnf_file(filename:str):    
    with open(os.path.join('src', 'samples', f'{filename}.cnf'), 'r') as file:
        CNF = []
        lines = file.readlines()

        for line in lines:
            if not (line.startswith('p') or line.startswith('c')):
                clause = list(map(int, line.split()))[:-1]
                CNF.append(clause)

        return CNF

def check_tautology(clause):
    for item in clause:
        if -item in clause:
            return True

    return False

def generate_random_3SAT(n_literals, n_clauses):
    literals = list(range(n_literals))[:-1]
    literals += list(map(lambda x: -x, literals))

    CNF = []
    for n in range(n_clauses):
        clause = random.sample(literals, 3)
        while check_tautology(clause):
            clause = random.sample(literals, 3)

        CNF.append(clause)

    return CNF
