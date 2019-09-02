# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_mrv(csp):
    """ Find the minimum remaining value """
    # Our initial value, since we havent found one yet
    minimum_remaining_value = None

    # Check our variables
    for variable in csp.get_all_vars():
        # Do we have another minimum remaining value? if so check its conditions
        if minimum_remaining_value is not None:
            # We only want to look at the smallest current value of unassigned variables,
            # so check for unassigned variables
            if not variable.is_assigned():
                # Find the MRV that affects the most constraints if we have a tie in domain sizes
                if variable.cur_domain_size() == minimum_remaining_value.cur_domain_size() and len(
                        csp.get_cons_with_var(minimum_remaining_value)) < len(csp.get_cons_with_var(variable)):
                    minimum_remaining_value = variable
                # Otherwise, just find the smallest domain
                elif variable.cur_domain_size() < minimum_remaining_value.cur_domain_size():
                    minimum_remaining_value = variable
        else:
            minimum_remaining_value = variable

    return minimum_remaining_value


def val_lcv(csp, var):
    """ Find a list of values ordered from least to most constrained"""

    constraints = csp.get_cons_with_var(var)
    values = []

    for domain in var.cur_domain():

        # Find the score and number of support tuples
        score = 0
        for constraint in constraints:
            if (var, domain) in constraint.sup_tuples:
                for tuples in constraint.sup_tuples[(var, domain)]:
                    if constraint.tuple_is_valid(tuples):
                        score += 1
                    else:
                        score += 0
        values.append((domain, score))

    # Sort our values
    n = len(values)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if values[j][1] < values[j + 1][1]:
                values[j], values[j + 1] = values[j + 1], values[j]

    # Return just the values without score in a list
    return [value[0] for value in values]
