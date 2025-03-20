from collections import defaultdict
from pysat.solvers import Minisat22
from rich.pretty import pprint

def extract_variables_count(formula):
    counts = defaultdict(int)
    
    for clause in formula:
        for literal in clause:
            counts[abs(literal)] += 1

    return counts

def parse_formula(formula, implications):
    counts = extract_variables_count(formula)
    key = max(counts, key=counts.get)

    for clause in formula:
        if key in clause:
            formula.remove(clause)

        elif -key in clause:
            clause.remove(-key)
            implications[key].append(clause)
            formula.remove(clause)

    if not any(formula):
        return implications

    return parse_formula(formula, implications)

def check_empty_clauses(formula):
    for i in formula:
        if not any(i):
            return True

    return False

def solve(implications):
    pprint(implications)

    new_formula = []
    for formula in implications.values():
        new_formula.extend(formula)

    with Minisat22(bootstrap_with=new_formula) as solver:
        if solver.solve():
            result = solver.get_model()            
            return result

        else:
            return "UNSAT"

                