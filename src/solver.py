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
    for key in implications.keys():
        for other, formula in implications.items():
            if key != other:
                for clause in formula:
                    if key in clause:
                        formula.remove(clause)

                    elif -key in clause:
                        clause.remove(-key)

    must_be_false = []

    for key, formula in implications.items():
        if check_empty_clauses(formula):
            must_be_false.append(key)

    for neg in must_be_false:
        implications.pop(neg)

    new_formula = []
    for formula in implications.values():
        new_formula.extend(formula)

    with Minisat22(bootstrap_with=new_formula) as solver:
        if solver.solve():
            result = solver.get_model()

            for literal in must_be_false:
                if literal in result:
                    result.remove(literal)
                    result.append(-literal)

            return solver.get_model()

        else:
            return "UNSAT"

                