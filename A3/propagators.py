#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    # ========BASED ON PROP_BT========

    # Check unary constraints
    if newVar is None:
        our_constraints = csp.get_all_cons()
    # If there arent any, check constraints involving new var
    else:
        our_constraints = csp.get_cons_with_var(newVar)

    # Track pruned and domain wipeouts
    domain_wipeout = False
    pruned = []

    # Use the forward checking rule: consider constraints with only one uninstantiated variable
    for constraint in our_constraints:
        if constraint.get_n_unasgn() == 1:
            u_variable = constraint.get_unasgn_vars()[0]

            # Forward check
            checked_fc = check_fc(constraint, u_variable)

            # Check our domain statues and pruned variables status
            domain_wipeout_occured = checked_fc[0]
            pruned_variables = checked_fc[1]

            # Check for domain wipeout
            pruned.extend(pruned_variables)
            if domain_wipeout_occured == True:
                domain_wipeout = True
                break
    return (not domain_wipeout, pruned)

def check_fc(constraint, variable):
    """ ========BASED ON PSUEDOCODE GIVEN IN LECTURE SLIDES========
    """
    values = []

    # Get the current scope
    variables = constraint.get_scope()

    # Track the unassigned value and create a list of values for the constraint we're checking
    for var in variables:
        values.append(var.get_assigned_value())
    # None is the index of the uninitialized value
    variable_index = values.index(None)

    # Pruned values
    pruned_variables = []

    # Check each domain, prune those that do not satisfy it
    for domain in variable.cur_domain():
        values[variable_index] = domain
        if not constraint.check(values):
            variable.prune_value(domain)
            pruned_variables.append((variable, domain))

    # Check for domain wipeout
    if variable.cur_domain_size() != 0:
        return (False, pruned_variables)
    elif variable.cur_domain_size() == 0:
        return (True, pruned_variables)



def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    """PSUEDO CODE
    while GACQueue not empty
    C = GACQueue.extract()
    for V := each member of scope(C)
        for d := CurDom[V]
            Find an assignment A for all other
            variables in scope(C) such that
            C(A ∪ V=d) = True
            if A not found
                CurDom[V] = CurDom[V] – d
                if CurDom[V] = ∅
                    empty GACQueue
                    return DWO //return immediately
                else
                    push all constraints C’ such that
                    V ∈ scope(C’) and C’ ∉ GACQueue
                    on to GACQueue
    return TRUE //while loop exited without DWO
    """
    # Check unary constraints
    if newVar is None:
        our_constraints = csp.get_all_cons()
    # If there arent any, check constraints involving new variable
    else:
        our_constraints = csp.get_cons_with_var(newVar)

    # Track the current GAC queue and pruned vars
    gacqueue = our_constraints[:]
    pruned = []

    # while GACQUEUE is not empty
    while gacqueue != []:
        # Get the first constraint
        constraint = gacqueue.pop(0)

        # Every variable that is in our scope and unassigned
        for variable in constraint.get_unasgn_vars():
            for domain in variable.cur_domain():
                # Find an assignment satisfying the constraint
                if not constraint.has_support(variable, domain):
                    # Prune
                    variable.prune_value(domain)
                    pruned.append((variable, domain))

                    # Check for domain wipeout
                    if variable.cur_domain_size() == 0:
                        return (False, pruned)
                    # Queue all the constraints with variable in scrop
                    else:
                        for con in our_constraints:
                            if variable in con.get_scope() and con not in gacqueue:
                                gacqueue.append(con)
    # Return true if there was no domain wipe out
    return (True, pruned)
