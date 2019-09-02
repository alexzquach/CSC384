# Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. kenken_csp_model (worth 20/100 marks)
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools


# ======== MY HELPERS FOR CREATING CONSTRAINT NAMES (neccessary for binary) ========
def create_cell_name(row, column):
    """ Creates a name for a cell, ex. r1c2 """
    return "r" + str(row + 1) + "c" + str(column + 1)


def create_binary_constraint(row1, column1, row2, column2):
    """ Creates a name for a binary constraint """
    return create_cell_name(row1, column1) + "," + create_cell_name(row2, column2)


def binary_ne_grid(kenken_grid):
    """ Returns a CSP for ken-ken with only binary constraints on each row and column """

    # Get the size of the board
    size_of_board = kenken_grid[0][0]
    # Get the cell values
    cell_values = list(range(1, size_of_board + 1))
    # Get the cell numbers
    # cells = list(range(size_of_board))
    # Constraint holders
    our_constraints = []
    our_constraint_names = []

    # Create the variables which is each cell of the board
    variables = []
    for r in range(size_of_board):
        row = []
        for c in range(size_of_board):
            variable = Variable(create_cell_name(r, c), list(range(1, size_of_board + 1))[:])
            row.append(variable)
        variables.append(row)

    # Add column & row constraints
    for cell in itertools.product(list(range(size_of_board)), list(range(size_of_board)), list(range(size_of_board))):
        # CHECK COLUMN CONSTRAINTS
        constraint1 = create_binary_constraint(cell[1], cell[0], cell[2], cell[0])
        constraint2 = create_binary_constraint(cell[2], cell[0], cell[1], cell[0])
        # checks to see if the rows are different and if the constraints are not created yet
        if constraint2 not in our_constraint_names and constraint1 not in our_constraint_names and cell[2] != cell[1]:
            # Create our constraint if we succesfully found a missing constraint
            # Add tuples that satisfy our constraint
            tuples = []
            for value1 in cell_values:
                for value2 in cell_values:
                    if value2 != value1:
                        tuples.append((value1, value2))
            # BUILT IN FUNCTION
            our_constraint = Constraint(create_binary_constraint(cell[1], cell[0], cell[2], cell[0]),
                                        [variables[cell[1]][cell[0]], variables[cell[2]][cell[0]]])
            our_constraint.add_satisfying_tuples(tuples)
            # Finally, add our constraint
            our_constraints.append(our_constraint)
            our_constraint_names.append(our_constraint.name)

            # CHECK ROW CONSTRAINTS
            constraint3 = create_binary_constraint(cell[0], cell[1], cell[0], cell[2])
            constraint4 = create_binary_constraint(cell[0], cell[2], cell[0], cell[1])
            # checks to see if the columns are different and if the constraints are not created yet
            if constraint3 not in our_constraint_names and constraint4 not in our_constraint_names and cell[2] != cell[
                1]:
                # Create our constraint if we succesfully found a missing constraint
                # Add tuples that satisfy our constraint
                tuples2 = []
                for value1 in cell_values:
                    for value2 in cell_values:
                        if value2 != value1:
                            tuples2.append((value1, value2))

                # BUILT IN FUNCTION
                our_constraint2 = Constraint(create_binary_constraint(cell[0], cell[1], cell[0], cell[2]),
                                             [variables[cell[0]][cell[1]], variables[cell[0]][cell[2]]])
                our_constraint2.add_satisfying_tuples(tuples2)
                # Finally, add our constraint
                our_constraints.append(our_constraint2)
                our_constraint_names.append(our_constraint2.name)
    # Create the CSP
    # BUILT IN FUNCTION
    our_csp = CSP('binary_ne', [our_variable for our_rows in variables for our_variable in our_rows])
    for our_constraint in our_constraints:
        our_csp.add_constraint(our_constraint)
    return (our_csp, variables)


def nary_ad_grid(kenken_grid):
    """ Returns a for kenken with n-ary all different constraints """
    # Get the size of the board
    size_of_board = kenken_grid[0][0]
    # Get the cell values
    cell_values = list(range(1, size_of_board + 1))
    # Get the cell numbers
    cells = list(range(size_of_board))

    # Create the variables which is each cell of the board
    variables = []
    for r in range(size_of_board):
        row = []
        for c in range(size_of_board):
            variable = Variable(create_cell_name(r, c), list(range(1, size_of_board + 1))[:])
            row.append(variable)
        variables.append(row)

    # Constraint holders
    our_constraints = []

    # Add column constraints based on permutations
    for column in cells:
        # Our column scope
        our_scope = []
        for row in cells:
            our_scope.append(variables[row][column])
        # Our tuples
        tuples = []
        for our_tuple in itertools.permutations(cell_values):
            tuples.append(our_tuple)

        tuples2 = []
        for our_tuple in itertools.permutations(cell_values):
            tuples2.append(our_tuple)
        # COMBINE OUR ROW AND COLUMN CONSTRAINT INTO ONE FUNCTION

        # Our constraint
        # Just hash our name in
        constraint = Constraint(hash(column), our_scope)
        constraint.add_satisfying_tuples(tuples)
        our_constraints.append(constraint)

        constraint2 = Constraint(hash(column), variables[column])
        constraint2.add_satisfying_tuples(tuples2)
        our_constraints.append(constraint2)

    # Create the CSP
    # BUILT IN FUNCTION
    our_csp = CSP('nary_ad', [our_variable for our_rows in variables for our_variable in our_rows])
    for our_constraint in our_constraints:
        our_csp.add_constraint(our_constraint)
    return (our_csp, variables)


def kenken_csp_model(kenken_grid):
    """ Returns a csp of kenken game with kenken cage constraints and nary all diff"""

    # Get the size of the board
    size_of_board = kenken_grid[0][0]
    # Get the cell values
    cell_values = list(range(1, size_of_board + 1))
    # Build our grid
    our_csp, variables = binary_ne_grid(kenken_grid)
    # Get our constraints
    our_constraints = []

    # Need cage variables
    length_of_kenken = len(kenken_grid)
    cage_constraint_total = range(1, length_of_kenken)

    # Create our cage constraints
    for cage in cage_constraint_total:
        row = list(kenken_grid[cage])

        # Get our operation and target AS DEFINED IN THE WORKSHEET
        our_operation = row[-1]
        our_target = row[-2]
        # Get the scope
        our_scope = []
        our_scope_values = row[:-2]
        for scope_value in our_scope_values:
            value = variables[(scope_value // 10) - 1][(scope_value % 10) - 1]
            our_scope.append(value)
        # Create constraints
        scope_size = len(our_scope)
        constraint_name = "op" + str(our_operation) + "=" + str(our_target)
        constraints = Constraint(constraint_name, our_scope)

        tuples = []

        # CHECK WHAT OUR OPERATION IS
        multiplication = False
        division = False
        subtraction = False
        addition = False

        if our_operation == 3:
            multiplication = True
        elif our_operation == 2:
            division = True
        elif our_operation == 1:
            subtraction = True
        elif our_operation == 0:
            addition = True

        # OUR DEFINED OPERATIONS
        if multiplication:
            # CHECK OUR MULTIPLICATION AGAINST OUR TARGET
            for our_tuple in itertools.product(tuple(cell_values), repeat=scope_size):
                for i in range(scope_size):
                    product = float(our_tuple[i])
                    for value1 in our_tuple[:i] + our_tuple[i + 1:]:
                        product *= value1
                    if product == our_target:
                        tuples.append(our_tuple)
        elif division:
            # CHECK OUR DIVISION AGAINST OUR TARGET
            for our_tuple in itertools.product(tuple(cell_values), repeat=scope_size):
                for i in range(scope_size):
                    quotient = float(our_tuple[i])
                    for value1 in our_tuple[:i] + our_tuple[i + 1:]:
                        quotient = quotient / value1
                    if quotient == our_target:
                        tuples.append(our_tuple)
        elif subtraction:
            # CHECK OUR SUBTRACTION AGAINST OUR TARGET
            for our_tuple in itertools.product(tuple(cell_values), repeat=scope_size):
                for i in range(scope_size):
                    if our_tuple[i] - sum(our_tuple[:i] + our_tuple[i + 1:]) == our_target:
                        tuples.append(our_tuple)
        elif addition:
            # CHECK OUR SUM AGAINST OUR TARGET
            for our_tuple in itertools.product(tuple(cell_values), repeat=scope_size):
                if sum(our_tuple) == our_target:
                    tuples.append(our_tuple)
        constraints.add_satisfying_tuples(tuples)
        our_constraints.append(constraints)

    # ADD OUR CONSTRAINTS TO THE CSP
    for temp_constraint in our_constraints:
        our_csp.add_constraint(temp_constraint)

    return (our_csp, variables)
