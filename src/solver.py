from collections import defaultdict
import networkx as nx
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
            clause.remove(key)
            formula.remove(clause)
            implications[-key].append(clause)

        elif -key in clause:
            clause.remove(-key)
            implications[key].append(clause)
            formula.remove(clause)

    if not any(formula):
        return implications

    return parse_formula(formula, implications)

def generate_implications_graph(formula):
    G = nx.DiGraph()

    for clause in formula:
        a, b = clause
        G.add_edge(-a, b)
        G.add_edge(-b, a)

    sccs = list(nx.strongly_connected_components(G))
    scc_map = {node: i for i, scc in enumerate(sccs) for node in scc}

    unsat_core = set()
    conflicting_sccs = set()

    for key in scc_map:
        if scc_map[key] == scc_map.get(-key, -1):  # Detecta ciclos contraditórios
            conflicting_sccs.add(scc_map[key])

    for u, v in G.edges():
        if scc_map[u] in conflicting_sccs and scc_map[v] in conflicting_sccs:
            unsat_core.add(frozenset([u, v]))  # Apenas cláusulas do ciclo contraditório

    return unsat_core, sccs, conflicting_sccs


def minimal_correction_subset(unsat_core):
    """
    Encontra um subconjunto mínimo de cláusulas a remover para tornar o problema satisfatível.
    """
    mcs = set()
    removed_vars = set()

    for clause in unsat_core:
        a, b = clause
        if a not in removed_vars and b not in removed_vars:
            mcs.add(clause)  # Remove apenas uma cláusula do ciclo
            removed_vars.add(a)
            removed_vars.add(b)

    return mcs


def solve(implications):
    new_formula = []
    for formula in implications.values():
        new_formula.extend(formula)

    unsat_core, sccs, conflicting_sccs = generate_implications_graph(new_formula)
    assignment = {}

    if conflicting_sccs:
        mcs = minimal_correction_subset(unsat_core)


        filtered_formula = []
        # Remove apenas o necessário
        for clause in new_formula:
            if frozenset(clause) not in mcs:
                filtered_formula.append(clause)

            else:
                for key, value in implications.items():
                    if frozenset(clause) not in set(map(frozenset, value)):
                        if -key in assignment.keys():
                            return 'UNSAT'
                            
                        assignment[key] = key > 0

        unsat_core, sccs, conflicting_sccs = generate_implications_graph(filtered_formula)
        if conflicting_sccs:
            return 'UNSAT'  # Se ainda houver conflito, o problema é insatisfatível

    sccs.reverse()    

    for scc in sccs:
        for node in scc:
            var = abs(node)
            if var not in assignment:
                assignment[var] = node > 0

    return assignment  # Dicionário {var: valor booleano}

