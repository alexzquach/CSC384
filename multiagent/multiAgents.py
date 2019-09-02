# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #====Get the closest food to pacman using manhattan distance====
        our_food_list = newFood.asList()
        #Initialize the closest food manhattan distance
        first_food = True
        closest_food = 0
        #Find the closest food by iterating through the new food list
        for food in our_food_list:
            if first_food is True:
                closest_food = manhattanDistance(food, newPos)
                first_food = False
            else:
                distance_to_food = manhattanDistance(food, newPos)
                if distance_to_food < closest_food:
                    closest_food = distance_to_food
        #closest_food now contains the food closest to pacman

        #====Get the closest ghost to pacman using manhattan distance====
        first_ghost = True
        closest_ghost = 0
        #Find the closest ghost by iterating through the new ghost list
        for ghost in newGhostStates:
            if first_ghost is True:
                closest_ghost = manhattanDistance(ghost.getPosition(), newPos)
                first_ghost = False
            else:
                distance_to_ghost = manhattanDistance(ghost.getPosition(), newPos)
                if distance_to_ghost < closest_ghost:
                    closest_ghost = distance_to_ghost
        #closest_ghost now contains the food closest to pacman

        #====Determine the score====
        #If the new position of pacman is not in the current state's food list, then we must make the score the
        #"reciprocal" (negative) of the closest food so far (as recommended)
        if newPos not in currentGameState.getFood().asList():
            score = -closest_food
        #If it is, just zero it out because we just moved on top of the new food in newPos
        else:
            score = 0

        #Check if any of the ghosts are scared because pacman has eaten a power pellet
        not_scared = True
        for scaredTimes in newScaredTimes:
            #This means there is at 1 scared ghost
            if scaredTimes != 0:
                not_scared = False
        #If none of the ghosts are scared, they can potentially kill pacman because pacman has not eaten a power pellet
        if not_scared and closest_ghost <= 1:
            #If the closest ghost is within 1 of pacman, this state is potentially doomed so return the reciprocal of the
            #largest possible number on the machine (negative infinity)
            score =  -float("inf")
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        #Our tuple: (Utility value associated with best move so far, best move so far)
        mini_max_move = self.mini_max(gameState, 0)[1]
        return mini_max_move

    def mini_max(self, game_state, current_depth):
        """
        Our recursive minimax function
        :param game_state: The current state of the game
        :type game_state: gameState
        :param current_depth: The depth of the game tree so far
        :type current_depth: int
        :return: Returns the best move and best values made so far
        :rtype:
        """
        #Initialize a best move so far to start off our algorithm
        best_move_so_far = None

        #First, check if the game is over (terminal nodes)
        is_game_over = game_state.isWin() or game_state.isLose()

        #Checks if the max depth has been reached using a calculation with the number of agents and the total
        #depth specified before.  This is based on the example where if the depth was 1, and there were 4 players,
        #the current_depth of the bottom level would be 4 (see assignment sheet for more)
        is_max_depth = current_depth == game_state.getNumAgents() * self.depth

        #Base case: If the game is over or its the max depth, return the appropriate values
        if is_game_over or is_max_depth:
            return (self.evaluationFunction(game_state), best_move_so_far)

        #Determine our agent, if it is 0, our agent is the pacman, else its a ghost
        agent = current_depth % game_state.getNumAgents()

        #Get some default comparison values using a built in python function
        if agent != 0:
            #Our min player (ghosts)
            value_being_compared = float("inf")
        else:
            #Our max player (pacman), pacman is always agent 0
            value_being_compared = - float("inf")

        #Get the next set of legal actions
        legal_actions = game_state.getLegalActions(agent)

        #Exit early if there are no legal actions
        if len(legal_actions) == 0:
            return (self.evaluationFunction(game_state), best_move_so_far)

        #Loop through all actions to get the minimum / maximum utility value and the move that made that value
        for legal_action in legal_actions:
            #Get the next game state
            next_game_state = game_state.generateSuccessor(agent, legal_action)
            #Get the next best move using a recursive call
            next_best_move = self.mini_max(next_game_state, current_depth + 1)
            #Not Pacman, treat as a min player in the search tree
            if agent != 0:
                #Return the minimum of the two values and save the best move so far
                if value_being_compared > next_best_move[0]:
                    #Best move so far
                    best_move_so_far = legal_action
                    #Utility value gotten with that move
                    value_being_compared = next_best_move[0]
            #Pacman, treat as a max player in the search tree
            elif agent == 0:
                #Return the maximum of the two values and save the best move so far
                if value_being_compared < next_best_move[0]:
                    #Best move so far
                    best_move_so_far = legal_action
                    #Utility value gotten with that move
                    value_being_compared = next_best_move[0]
        #Return a tuple of the best move so far and the utility value achieved with that best move
        return (value_being_compared, best_move_so_far)

        # ======PSUEDO CODE======
        # if agent == 0:
        #     return max(mini_max(legal_action, current_depth + 1) for legal_action in legal_actions
        # else:
        #     return max(mini_max(legal_action, current_depth + 1) for legal_action in legal_actions

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        #Initialize alpha and beta to -infinity and infinity as in class, tuple is same as
        #minimax tuple
        mini_max_move = self.mini_max_alpha_beta(gameState, 0, -float("inf"), float("inf"))[1]
        return mini_max_move

    def mini_max_alpha_beta(self, game_state, current_depth, alpha, beta):
        """
        Our recursive minimax function with alpha-beta pruning
        :param beta: beta for alpha beta pruning
        :type beta:
        :param alpha: alpha for alpha beta pruning
        :type alpha:
        :param game_state: The current state of the game
        :type game_state: gameState
        :param current_depth: The depth of the game tree so far
        :type current_depth: int
        :return: Returns the best move and best values made so far
        :rtype:
        """
        # Initialize a best move so far to start off our algorithm
        best_move_so_far = None

        # First, check if the game is over (terminal nodes)
        is_game_over = game_state.isWin() or game_state.isLose()

        # Checks if the max depth has been reached using a calculation with the number of agents and the total
        # depth specified before.  This is based on the example where if the depth was 1, and there were 4 players,
        # the current_depth of the bottom level would be 4 (see assignment sheet for more)
        is_max_depth = current_depth == game_state.getNumAgents() * self.depth

        # Base case: If the game is over or its the max depth, return the appropriate values
        if is_game_over or is_max_depth:
            return (self.evaluationFunction(game_state), best_move_so_far)

        # Determine our agent, if it is 0, our agent is the pacman, else its a ghost
        agent = current_depth % game_state.getNumAgents()

        # Get some default comparison values using a built in python function
        if agent != 0:
            # Our min player (ghosts)
            value_being_compared = float("inf")
        else:
            # Our max player (pacman), pacman is always agent 0
            value_being_compared = - float("inf")

        # Get the next set of legal actions
        legal_actions = game_state.getLegalActions(agent)

        # Exit early if there are no legal actions
        if len(legal_actions) == 0:
            return (self.evaluationFunction(game_state), best_move_so_far)

        # Loop through all actions to get the minimum / maximum utility value and the move that made that value
        for legal_action in legal_actions:
            # Get the next game state
            next_game_state = game_state.generateSuccessor(agent, legal_action)
            # Get the next best move using a recursive call
            next_best_move = self.mini_max_alpha_beta(next_game_state, current_depth + 1, alpha, beta)
            # Not Pacman, treat as a min player in the search tree
            if agent != 0:
                # Return the minimum of the two values and save the best move so far
                if value_being_compared > next_best_move[0]:
                    # Best move so far
                    best_move_so_far = legal_action
                    # Utility value gotten with that move
                    value_being_compared = next_best_move[0]
                #========PRUNE========#
                beta = min(value_being_compared, beta)
                if beta <= alpha:
                    #Break early
                    return (value_being_compared, best_move_so_far)
            # Pacman, treat as a max player in the search tree
            elif agent == 0:
                # Return the maximum of the two values and save the best move so far
                if value_being_compared < next_best_move[0]:
                    # Best move so far
                    best_move_so_far = legal_action
                    # Utility value gotten with that move
                    value_being_compared = next_best_move[0]
                #========PRUNE========#
                alpha = max(value_being_compared, alpha)
                if beta <= alpha:
                    #Break early
                    return (value_being_compared, best_move_so_far)
        # Return a tuple of the best move so far and the utility value achieved with that best move
        return (value_being_compared, best_move_so_far)

        #======PSUEDO CODE======
        # if agent == 0:
        #     for legal_action in legal_actions:
        #         alpha = max(alpha, self.mini_max_alpha_beta(legal_action, current_depth + 1, alpha, beta))
        #         if beta <= alpha:
        #             break
        #     return alpha
        # else:
        #     for legal_action in legal_actions:
        #         beta = min(beta, self.mini_max_alpha_beta(legal_action, current_depth + 1, alpha, beta))
        #         if beta <= alpha:
        #             break
        #     return beta

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        expecti_max_move = self.expecti_max(gameState, 0)[1]
        return expecti_max_move


    def expecti_max(self, game_state, current_depth):
        """
        Our expecti_max function

        =========================================
        BASED ON PSUEDOCODE GIVEN IN CLASS SLIDES
        =========================================

        :param game_state: The current state of the game
        :type game_state: gameState
        :param current_depth: The depth of the game tree so far
        :type current_depth: int
        :return: Returns the best move and best values made so far with expectimax properties
        :rtype:
        """
        # Initialize a best move so far to start off our algorithm
        best_move_so_far = None

        # First, check if the game is over (terminal nodes)
        is_game_over = game_state.isWin() or game_state.isLose()

        # Checks if the max depth has been reached using a calculation with the number of agents and the total
        # depth specified before.  This is based on the example where if the depth was 1, and there were 4 players,
        # the current_depth of the bottom level would be 4 (see assignment sheet for more)
        is_max_depth = current_depth == game_state.getNumAgents() * self.depth

        # Base case: If the game is over or its the max depth, return the appropriate values
        if is_game_over or is_max_depth:
            return (self.evaluationFunction(game_state), best_move_so_far)

        # Determine our agent, if it is 0, our agent is the pacman, else its a ghost
        agent = current_depth % game_state.getNumAgents()

        # Get some default comparison values using a built in python function
        if agent != 0:
            # Our CHANCE player
            value_being_compared = 0
        else:
            # Our max player (pacman), pacman is always agent 0
            value_being_compared = - float("inf")

        # Get the next set of legal actions
        legal_actions = game_state.getLegalActions(agent)

        # Exit early if there are no legal actions
        if len(legal_actions) == 0:
            return (self.evaluationFunction(game_state), best_move_so_far)

        # Loop through all actions to get the minimum / maximum utility value and the move that made that value
        for legal_action in legal_actions:
            # Get the next game state
            next_game_state = game_state.generateSuccessor(agent, legal_action)
            # Get the next best move using a recursive call
            next_best_move = self.expecti_max(next_game_state, current_depth + 1)
            # Not Pacman, treat as a CHANCE player in our search tree
            if agent != 0:
                #the probability of making a move is based on the length of the legal actions available
                #for the agent that is not pacman
                value_being_compared += next_best_move[0] / len(legal_actions)
            # Pacman, treat as a max player in the search tree
            elif agent == 0:
                # Return the maximum of the two values and save the best move so far
                if value_being_compared < next_best_move[0]:
                    # Best move so far
                    best_move_so_far = legal_action
                    # Utility value gotten with that move
                    value_being_compared = next_best_move[0]
        # Return a tuple of the best move so far and the utility value achieved with that best move
        return (value_being_compared, best_move_so_far)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: As recommended, a linear combination of crucial pacman states was taken
      in order to determine our final score.  Based on what was learned in question 1, I found the
      closest food, and closest ghosts to pacman to determine score.  If the game is over, return
      a corresponding infinity depending on what ended the game.  Number of food was given a weighting of 70 by default.
      We also add the closest food to the score.  For the closest ghost, since it is very significant, we will multiply
      it by itself.  We do this to quickly amplify the danger of a close ghost.
      If a ghost is within two of pacman, we need to eat a power pellet ASAP to kill it so we give a
      weighting of 50 when a ghost is near, else just a weight of 10.  Finally, we return
      the negative reciprocal as we did in question 1.  Note: we subtract the current score because it is score
      that has already been counted in previous turns.
    """
    #First, check if the game is over by win or loss. If so, return the appropriate infinity
    #Negative infinity for an instant lose state
    # First, check if the game is over by win or loss. If so, return the appropriate infinity
    # Negative infinity for an instant lose state
    if currentGameState.isLose():
        return -float("inf")
    # Positive infinity for a instant win state
    elif currentGameState.isWin():
        return float("inf")

    # Based on question 1
    # Current pacman position
    pacman_pos = currentGameState.getPacmanPosition()
    # Current food list
    food_list = currentGameState.getFood()
    # Current ghost states
    ghost_states = currentGameState.getGhostStates()
    # Current scared times
    scared_times = [ghostState.scaredTimer for ghostState in ghost_states]

    #Our final score
    final_score = 0

    our_food_list = food_list.asList()
    # Initialize the closest food manhattan distance
    first_food = True
    closest_food = 0
    # Find the closest food by iterating through the new food list
    for food in our_food_list:
        if first_food is True:
            closest_food = manhattanDistance(food, pacman_pos)
            first_food = False
        else:
            distance_to_food = manhattanDistance(food, pacman_pos)
            if distance_to_food < closest_food:
                closest_food = distance_to_food
                # closest_food now contains the food closest to pacman

    # ====Get the closest ghost to pacman using manhattan distance====
    first_ghost = True
    closest_ghost = 0
    # Find the closest ghost by iterating through the new ghost list
    for ghost in ghost_states:
        if first_ghost is True:
            closest_ghost = manhattanDistance(ghost.getPosition(), pacman_pos)
            first_ghost = False
        else:
            distance_to_ghost = manhattanDistance(ghost.getPosition(), pacman_pos)
            if distance_to_ghost < closest_ghost:
                closest_ghost = distance_to_ghost
    # Check if any of the ghosts are scared because pacman has eaten a power pellet
    not_scared = True
    for scaredTimes in scared_times:
        # This means there is at 1 scared ghost
        if scaredTimes != 0:
            not_scared = False
            # If none of the ghosts are scared, they can potentially kill pacman because pacman has not eaten a power pellet
    # If there is a scared ghost within 2 of pacman, we need to eat a power pellet ASAP
    if not_scared and closest_ghost <= 2:
        # If the closest ghost is within 1 of pacman, this state is potentially doomed so return the reciprocal of the
        # largest possible number on the machine (negative infinity)
        # Add the number of power pellets according to a custom weight
        power_pellet_weight = 50
    # If not, not much weight should be put on power pellets
    else:
        # Add the number of power pellets according to a custom weight
        power_pellet_weight = 10

    #Linear combination of all our values
    final_score += closest_food + \
                   closest_ghost ** 2 + \
                   70 * currentGameState.getNumFood() + \
                   power_pellet_weight * len(currentGameState.getCapsules()) - \
                   currentGameState.getScore()
    # Return the negative reciprocol of the linear combination of all of our score determiners like in question 1
    return -final_score

# Abbreviation
better = betterEvaluationFunction
