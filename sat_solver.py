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
    Each integer in the list is a literal, where positive integers represent positive literals 
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
        if parse[0:2] == ["p","cnf"]:
            try:
                var_count = int(parse[2])
                clause_count = int(parse[3])
            except TypeError:
                print("Error: Variable and clause amounts not properly defined")
                return
            continue

        try:
            clause = []
            for var in parse:
                if var == "0":
                    break
                var = int(var)
                if abs(var) > var_count:
                    print("Error: Variable amount used does not match defined variable amount")
                    return
                clause.append(var)
            if clause:
                clauses.append(clause)
        except TypeError:
            print("Clauses improperly defined")

    return var_count,clause_count,clauses


def main():
    var_count, clause_count, parsed_clauses = parse_cnf(sys.stdin)
    print(f"Variables: {var_count}, Clauses: {clause_count}")
    for line in parsed_clauses:
        print(line)

if __name__ == '__main__':
    main()
