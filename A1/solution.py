#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
import math

from search import * #for search engines
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state #for LunarLockout specific classes and problems

#LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return 0

def heur_manhattan_distance(state):
    #OPTIONAL
    '''Manhattan distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
    # Our coordinates for the middle of the board
    middle_x = (state.width - 1) / 2
    middle_y = (state.height - 1) / 2
    # The sum
    manhattan_distance = 0

    # Go through all the xanadus in the state space
    for xanadu in state.xanadus:
        # Find the change in x and y
        x_distance = abs(xanadu[0] - middle_x)
        y_distance = abs(xanadu[1] - middle_y)
        manhattan_distance = manhattan_distance + x_distance + y_distance
    return manhattan_distance


def heur_L_distance(state):
    #IMPLEMENT
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the L distances between each xanadu and the escape hatch.
    middle_x = (state.width - 1) / 2
    middle_y = (state.height - 1) / 2
    # The sum
    l_distance = 0

    # Go through all the xanadus in the state space
    for xanadu in state.xanadus:
        # Find the change in x and y
        x_distance = abs(xanadu[0] - middle_x)
        #If there is a difference in x, then we have to make 1 x move to move along the x axis
        if x_distance > 0:
            x_distance = 1
        else:
            x_distance = 0
        #If there is a difference in y, then wew have to make 1 y move to move along the y axis
        y_distance = abs(xanadu[1] - middle_y)
        if y_distance > 0:
            y_distance = 1
        else:
            y_distance = 0
        #Total the distances
        l_distance += x_distance + y_distance
    return l_distance

def heur_alternate(state):
    #IMPLEMENT
    '''a better lunar lockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    """================Heuristic explanation================:
    This heuristic acts as a modified L distance, where we add 1 for specific cases.  To start off, we determine how many
    xanadus there are and add 1 per xanadu, since they all need to reach the goal.  Then, per xanadu, we will determine 
    1. If the xanadu is on the goal
        If so, we subtract 1 cost from the heuristic because that is one less xanadu to move
    2. If not on the goal we will check if the xanadu is on the middle column / row.
        If not, we add 1 cost because it will take at least 1 turn to move the xanadu into the correct rows/columns
    3. If there is a robot on the goal, we will add 1 cost because we need to move the robot off, adding 1 cost
    4. If there are any xanadus and robots that share the same x or y coordinates, then has_robot_in_line is true
    and dead_states is false since we can move a xanadu.  Else we add 1 cost since we need at least 1 turn to move it
    5. If there is a xanadu on the middle line and a robot on the middle line, we check if the robot is blocking the goal
    or not.  If it is blocking, we add 1 cost because we need to move the robot out of the way.
    ================End Heuristic explanation================
    """
    #Your function should return a numeric value for the estimate of the distance to the goal.
    middle_x = (state.width - 1) / 2
    middle_y = (state.height - 1) / 2
    #Since there are a len(state.xanadus) amount of xanadaus, our base value for the heuristic is the number of xanadus
    #since we need to get all of them to the goal to win
    heur_alt = len(state.xanadus)

    for xanadu in state.xanadus:
        #Keeps track of any robots between any xanadus and the goal.  Add 1 to the heuristic since
        #it will take at least 1 move to move the robot away from between the xanadu and the goal
        has_goal_between_xanrob = False
        #Checks if there are robots in the same line that will allow it to move
        has_robot_in_line = False
        #Check for dead states (mentioned in piazza), assume true to begin
        dead_states_exist = True

        #Check for xanadus in the goal state, if there are any, avoid the other checks since we have reached our goal state
        if xanadu[0] == middle_x and xanadu[1] == middle_y:
            heur_alt -= 1
        else:
            for robot in state.robots:
                # Check if the xanadu is in the middle column / row, if not add 1 since we need at least 1 move
                # to get into the centre areas
                if xanadu[0] != middle_x or xanadu[1] != middle_y:
                    heur_alt += 1
                #Add 1 to the heuristic if there is a robot on the centre, since we need at least
                #1 turn to move the robot away from the centre
                if robot[0] == middle_x and robot[1] == middle_y:
                    heur_alt += 1
                for coordinate in range(0, 1):
                    #Check if there are matching x or y coordinates between robot and xanadu, if so there are
                    #no dead states as we are able to make at least 1 move
                    if robot[coordinate] == xanadu[coordinate]:
                        dead_states_exist = False
                        has_robot_in_line = True
                    #wanted to put a break, but what if they matched x and y!
                    #Check to see if there are any xanadus and robots lined up with the middle
                    if xanadu[coordinate] == middle_x and robot[coordinate] == middle_x:
                        #Check if the centre is between the xanadu and the robot
                        if (xanadu[coordinate] < middle_x < robot[coordinate]) or (xanadu[coordinate] > middle_x > robot[coordinate]):
                            has_goal_between_xanrob = True
                        #The robot is blocking the xanadu and the centre
                        else:
                            heur_alt += 1
            #if the goal is not between a xanadu and a robot, add 1 since it will take more turns
            if has_goal_between_xanrob == False:
                heur_alt += 1
            #if there is no robot in line with a xanadu, add 1 to the heuristic since it will take at least 1 turn to move
            #a robot in to make sure the xanadu can move
            if has_robot_in_line == False:
                heur_alt += 1
            #If there are dead states, we want to return infinity as our heuristic (as specified by piazza)
            if dead_states_exist:
                return 2**30 #Infinity representation of the dead state
    return heur_alt

def fval_function(sN, weight):
    #IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a LunarLockoutState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    #Formula as given from assignment
    return sN.gval + (weight * sN.hval)

def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound = 2):
    #IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    our_search_engine = SearchEngine('custom', 'full')
    #Pulled from the search code
    end_time = os.times()[0] + timebound
    end_state = None
    while os.times()[0] < end_time and weight >= 1:
        #Defined on assignment sheet
        wrapped_fval_function = (lambda  sN: fval_function(sN, weight))
        #Initialize our search engine
        our_search_engine.init_search(initial_state, lockout_goal_state, heur_fn, wrapped_fval_function)
        #Get the final time
        end_state = our_search_engine.search(timebound)
        #Decrease weight
        weight -= 1
    #Returns the goal state if goal state is found else we return false
    if end_state:
        return end_state
    else:
        return False

def anytime_gbfs(initial_state, heur_fn, timebound = 2):
#OPTIONAL
  '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
  '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
  '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  return 0

PROBLEMS = (
  #5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2),(0,4),(2,0),(4,0)),((4, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 3),)),
  #7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6,3), (5,4)), ((6, 2),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2,6)), ((4, 6),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2,6), (4,6)), ((2, 0),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0 ,2), (2 ,3), (4, 4), (2, 5)), ((2, 4),(3, 1),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0 ,2), (1 ,2), (6, 4), (2, 5)), ((2, 0),(3, 0),(4, 0))),

  )

if __name__ == "__main__":

  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(len(PROBLEMS)): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    print("*******RUNNING A STAR*******")
    se = SearchEngine('astar', 'full')
    se.init_search(s0, lockout_goal_state, heur_alternate)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0;
  print("Running Anytime Weighted A-star")

  for i in range(len(PROBLEMS)):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]
    weight = 4
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0;
  print("Running Anytime GBFS")

  for i in range(len(PROBLEMS)):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]
    final = anytime_gbfs(s0, heur_alternate, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")





