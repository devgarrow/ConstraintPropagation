# =============================
# Student Names: Devynn Garrow, Jessica Guetre
# Group ID: 13
# Date: January 28, 2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: Functions to create Cagey puzzles using a CSP object. The three CSP models produced satisfied (1) binary not-equal constraints,
#       (2) n-ary all-different constraints, and (3) cage constraints and binary not-equal constraints. Each constraint type has a helper
#       function to add the constraints to the CSP object. Each CSP creation function returns the CSP object and a list of Variable objects
#       contained within the CSP object.
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
from itertools import permutations, product
from math import prod

def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    # Creates a binary not-equal constraint CSP model
    try:
        n = cagey_grid[0]
        var_array = []
        for i in range(1, n+1):
            for j in range(1, n+1): 
                var_array.append(Variable(f'V{i}{j}', list(range(1, n+1))))
    except Exception as e:
        print(f"Error in variable creation: {e}")
        raise

    try:
        binary_CSP = CSP("BinaryCSP", var_array)
    except Exception as e:
        print(f"Error creating binary not-equal CSP object: {e}")
        raise

    binary_CSP = binary_ne_constraints(n, var_array, binary_CSP)

    return binary_CSP, var_array
    
def nary_ad_grid(cagey_grid):
    ##IMPLEMENT
    # Creates an n-ary all-different constraint CSP model
    try:
        n = cagey_grid[0]
        var_array = []
        for i in range(1, n+1):
            for j in range(1, n+1): 
                var_array.append(Variable(f'V{i}{j}', list(range(1, n+1))))
    except Exception as e:
        print(f"Error in variable creation: {e}")
        raise

    try:
        nary_CSP = CSP("NaryCSP", var_array)
    except Exception as e:
        print(f"Error creating n-ary all-different CSP object: {e}")
        raise

    nary_CSP = nary_ad_constraints(n, var_array, nary_CSP)

    return nary_CSP, var_array

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    # Creates a CSP model with cage constraints and binary not-equal constraints
    try:
        n = cagey_grid[0]
        cages = cagey_grid[1]
        var_array = []

        for cage in cages:
            value, indices, operation = cage
            var_cells = [f"Var-Cell({i},{j})" for i, j in indices]
            var_cells_str = ', '.join(var_cells)
            var_array.append(Variable(f"Cage_op({value}:{operation}:[{var_cells_str}])", ['+', '-', '*', '/', 'f']))

        for i in range(1, n+1):
            for j in range(1, n+1):
                var_array.append(Variable(f'Cell{i}{j}', list(range(1, n+1))))
    except Exception as e:
        print(f"Error in variable creation: {e}")
        raise

    try:
        cagey_CSP = CSP("CageyCSP", var_array)
    except Exception as e:
        print(f"Error creating cagey CSP object: {e}")
        raise

    cagey_CSP = binary_ne_constraints(n, var_array, cagey_CSP)
    cages = cagey_grid[1]
    cagey_CSP = cagey_constraints(n, cages, var_array, cagey_CSP)

    return cagey_CSP, var_array

def binary_ne_constraints(n, var_array, binary_CSP):
    # Adds binary not-equal constraints to a CSP object
    try:
        binary_ne_tuples = [(i, j) for i in range(1, n+1) for j in range(1, n+1) if i != j]
        for i in range(n):
            for j in range(n):
                for k in range(j+1, n):
                    r_scope = [var_array[i*n+j], var_array[i*n+k]]
                    r_con = Constraint(f"NE({r_scope[0].name}{r_scope[1].name})", r_scope)
                    r_con.add_satisfying_tuples(binary_ne_tuples)
                    binary_CSP.add_constraint(r_con)

                for k in range(i+1, n):
                    c_scope = [var_array[i*n+j], var_array[k*n+j]]
                    c_con = Constraint(f"NE({c_scope[0].name}{c_scope[1].name})", c_scope)
                    c_con.add_satisfying_tuples(binary_ne_tuples)
                    binary_CSP.add_constraint(c_con)
    except Exception as e:
        raise Exception(f"Error generating binary not-equal constraints: {e}")

    return binary_CSP

def nary_ad_constraints(n, var_array, nary_CSP):
    # Adds n-ary all-different constraints to a CSP object
    try:
        nary_ad_tuples = [list(perm) for perm in permutations(range(1, n+1))]
        for i in range(n):
            r_scope = [var_array[i*n+j] for j in range(n)]
            r_con = Constraint(f"Row({i})", r_scope)
            r_con.add_satisfying_tuples(nary_ad_tuples)
            nary_CSP.add_constraint(r_con)

            c_scope = [var_array[j*n+i] for j in range(n)]
            c_con = Constraint(f"Col({i})", c_scope)
            c_con.add_satisfying_tuples(nary_ad_tuples)
            nary_CSP.add_constraint(c_con)
    except Exception as e:
        raise Exception(f"Error generating n-ary all-different constraints: {e}")

    return nary_CSP

def cagey_constraints(n, cages, var_array, cagey_CSP):
    # Adds cage constraints to a CSP object
    for k, cage in enumerate(cages):
        try:
            value, indices, operation = cage
            op_scope = [var_array[k]]
            cell_scope = [var_array[(i-1)*n + (j-1) + len(cages)] for i, j in indices]
            cagey_scope = op_scope + cell_scope
            cagey_con = Constraint(f"Cage({value}:{operation}:{[v.name for v in cagey_scope]})", cagey_scope)
        except Exception as e:
            print(f"Error creating constraint object or scope: {e}")
            raise

        tuples = []
        if operation == '?':
            for o in ['+', '-', '*', '/']:
                tuples.extend(cagey_tuples(o, value, cell_scope, n))
        else:
            tuples.extend(cagey_tuples(operation, value, cell_scope, n))

        try:
            cagey_con.add_satisfying_tuples(tuples)
            cagey_CSP.add_constraint(cagey_con)
        except Exception as e:
            print(f"Error adding constraints to CSP object: {e}")
            raise

    return cagey_CSP

def cagey_tuples(operation, value, cell_scope, n):
    # Creates tuples that satisfy the cage constraint
    tuples = []
    try:
        if operation == '+':
                for tup in product(range(1,n+1), repeat=len(cell_scope)):
                    if sum(tup) == value:
                        tuples.append((operation,) + tup)
        elif operation == '-':
            for tup in permutations(range(1,n), r=len(cell_scope)):
                if abs(tup[0] - sum(tup[1:])) == value:
                    tuples.append((operation,) + tup)
        elif operation == '*':
            for tup in product(range(1,n+1), repeat=len(cell_scope)):
                if prod(tup) == value:
                    tuples.append((operation,) + tup)
        elif operation == '/':
            for tup in permutations(range(1,n), r=len(cell_scope)):
                if tup[0] / prod(tup[1:]) == value:
                    tuples.append((operation,) + tup)
    except Exception as e:
        print(f"Error generating tuples for cage constraints: {e}")
        raise
 
    return tuples