import sys
import math


def parse_cnf(input_cnf):

    """
    Parses lines of a .cnf file in the DIMACS format.

    Parameters
    -------------------
    input_cnf : list[string]
    A list of strings, where each element is a line from the input cnf file.

    Returns
    -------------------
    var_count : int
    The number of variables in the problem

    clause_count : int
    The number of clauses in the problem

    clauses : list[list[int]]
    A list of lists of integers.
    Each list represents a clause in the problem.
    Each integer in the list is a literal
    where positive integers represent positive literals
    and negative integers represent negative literals.
    """

    var_count = None
    clause_count = None
    clauses = []

    for line in input_cnf:
        parse = line.strip().split(" ")
        if not parse:
            continue
        if parse[0] == "c":
            continue
        if parse[0:2] == ["p", "cnf"]:
            try:
                var_count = int(parse[2])
                clause_count = int(parse[3])
            except TypeError:
                print("Variable and clause amounts not properly defined")
                return
            continue

        try:
            tautology = False
            clause = []
            for var in parse:
                if var == "0":
                    break
                var = int(var)
                if abs(var) > var_count:
                    print("Variable amount used does not match defined variable amount")
                    return None, None, None
                if -var in clause:
                    # tautology removal implemented on file read
                    tautology = True
                    break
                clause.append(var)
            if clause and not tautology:
                clauses.append(clause)
        except TypeError:
            print("Clauses improperly defined")

    return var_count, clause_count, clauses


def unit_propagate(clauses):
    """
    Performs unit propagation exhaustively on a set of clauses.


    Parameters
    -------------------
    clauses : list[list[int]]
    A list of lists of integers representing a set of clauses.

    Returns
    -------------------
    clauses : list[list[int]]
    A list of lists of integers representing the set of clauses
    after exhaustive unit propagation.
    """

    while True:
        # identify any unit clauses
        unit_clause = False
        for clause in clauses:
            if len(clause) == 1:
                unit_clause = True
                propagation_var = clause[0]
                break
        if not unit_clause:
            break

        # propagate on unit clauses
        i = 0
        length = len(clauses)
        while i < length:
            if propagation_var in clauses[i]:
                del clauses[i]
                i -= 1
                length -= 1
            elif -propagation_var in clauses[i]:
                for j in range(clauses[i].count(-(propagation_var))):
                    clauses[i].remove(-(propagation_var))
            i += 1

    return clauses


def del_pure_literal(clauses):
    """
    Removes pure literals from a clause.
    Pure literals only occur positively or negatively,
    and clauses containing pure literals can be removed from the problem.

    Parameters
    -------------------
    clauses : list[list[int]]
    A list of lists of integers representing a set of clauses.


    Returns
    -------------------
    clauses : list[list[int]]
    The set of clauses with pure literal deletion applied
    """

    while True:
        # get all literals in the problem
        literals = set([])
        pure_literals = []
        for clause in clauses:
            literals = literals.union(set(clause))

        for lit in literals:
            if -lit not in literals:
                pure_literals.append(lit)

        if not pure_literals:
            break

        i = 0
        while i < len(clauses):
            for lit in pure_literals:
                if lit in clauses[i]:
                    del clause[i]
                    i -= 1
                    continue
            i += 1

    return clauses


def dpll(clauses, var):
    """
    Performs DPLL on a set of clauses, recursively:
    - Performs unit propagation then checks the satisfiability of the resulting set of clauses.
    - Introduces a unit clause of the form n or -n and performs DPLL on both
    - If either of these return True, the set of clauses is satisfiable.

    Parameters
    -------------------
    clauses : list[list[int]]
    A list of lists of integers representing a set of clauses.

    var : int
    The next variable to be introduced as a unit clause.

    Returns
    -------------------
    True if the set of clauses is satisfiable, False otherwise.
    """

    clauses = unit_propagate(clauses)
    if not clauses:  # empty set of clauses - always satisfiable
        return True
    if [] in clauses:  # empty clause - cannot be satisfied
        return False

    clauses = del_pure_literal(clauses)

    # splitting on var and -var
    # a deep copy needs to be created to avoid modifying clause sets further up the tree
    pos_clauses = [[i for i in clause] for clause in clauses] + [[var]]
    pos_split = dpll(pos_clauses, var + 1)
    neg_clauses = [[i for i in clause] for clause in clauses] + [[-var]]
    neg_split = dpll(neg_clauses, var + 1)
    return pos_split or neg_split


def main():
    var_count, clause_count, clauses = parse_cnf(sys.stdin)
    if not var_count or not clause_count or not clauses:
        print("File read failed. Terminating")
        return

    result = dpll(clauses, 1)
    if result:
        print("SATISFIABLE")
    else:
        print("UNSATISFIABLE")


if __name__ == '__main__':
    main()
