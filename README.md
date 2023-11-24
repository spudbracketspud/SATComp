# SATComp
Created for the COMP21111 Logic and Modelling SAT solver competition; will be developed as and when I have time. Please note this is a personal project not intended to be used for professional purposes.
Accepts SAT problems in clausal normal form in the DIMACs format, as defined here http://logic.pdmi.ras.ru/~basolver/dimacs.html
Reads problems through standard input - this can be done on the command line as
cat problem.cnf | py sat_solver.py
Implements DPLL with tautology removal and pure literal deletion to solve problems.
