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
from util import manhattanDistance # noqa


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

        "Add more of your code here if you want to"

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
        numFood = currentGameState.getFood().count()
        "*** YOUR CODE HERE ***"
        if successorGameState.getNumFood() == numFood:
            distance = min(manhattanDistance(f, newPos) for f in newFood.asList())
        else:
            distance = 0
        for ghost in successorGameState.getGhostPositions():
            distance += 10 ** (2 - manhattanDistance(ghost, newPos))
        return 1.0/distance


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
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        max = -float("inf")
        max_index = 0
        for index in range(len(actions)):
            score = self.MiniMax(gameState.generateSuccessor(0, actions[index]), 1, self.depth)
            if score > max:
                max = score
                max_index = index
        return actions[max_index]


    def MiniMax(self, n, index, depth):
        """the minimax implemented by recursion"""
        if n.isWin() or n.isLose() or depth == 0:
            return self.evaluationFunction(n)
        child_list = [n.generateSuccessor(index, a) for a in n.getLegalActions(index)]
        if index != 0:
            if index == n.getNumAgents() - 1:
                return min(self.MiniMax(c, 0, depth - 1) for c in child_list)
            else:
                return min(self.MiniMax(c, index + 1, depth) for c in child_list)
        else:
            return max(self.MiniMax(c, 1, depth) for c in child_list)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        max_score = -float("inf")
        max_action = None
        alpha = -float("inf")
        for action in gameState.getLegalActions(0):
            val = self.AlphaBeta(gameState.generateSuccessor(0, action), 1, self.depth, alpha, float("inf"))
            alpha = max(val, alpha)
            if alpha > max_score:
                max_score = alpha
                max_action = action
        return max_action

    def AlphaBeta(self, n, index, depth, alpha, beta):
        """aplha-beta pruning"""
        if n.isWin() or n.isLose() or depth == 0:
            return self.evaluationFunction(n)
        if index == 0:
            for action in n.getLegalActions(index):
                alpha = max(alpha, self.AlphaBeta(n.generateSuccessor(index, action), 1, depth, alpha, beta))
                if beta <= alpha:
                    break
            return alpha
        elif index == n.getNumAgents() - 1:
            for action in n.getLegalActions(index):
                beta = min(beta, self.AlphaBeta(n.generateSuccessor(index, action), 0, depth - 1, alpha, beta))
                if beta <= alpha:
                    break
            return beta
        else:
            for action in n.getLegalActions(index):
                beta = min(beta, self.AlphaBeta(n.generateSuccessor(index, action), index + 1, depth, alpha, beta))
                if beta <= alpha:
                    break
            return beta


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
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions()
        max = -float("inf")
        max_index = 0
        for index in range(len(actions)):
            [move, score] = self.Expectimax(gameState.generateSuccessor(0, actions[index]), 1, self.depth)
            if score > max:
                max = score
                max_index = index
        return actions[max_index]


    def Expectimax(self, state, index, depth):
        """
        the recursive expectimax
        """
        best_move = None
        if state.isLose() or state.isWin() or depth == 0:
            return [best_move, self.evaluationFunction(state)]
        value = 0
        if index == 0: value = -float("inf")
        for move in state.getLegalActions(index):
            new_state = state.generateSuccessor(index, move)
            if index == state.getNumAgents() - 1:
                [next_move, next_value] = self.Expectimax(new_state, 0, depth - 1)
            else:
                [next_move, next_value] = self.Expectimax(new_state, index + 1, depth)
            if index == 0 and value < next_value:
                value, best_move = next_value, move
            if index != 0:
                value = value + 1.0/len(state.getLegalActions(index)) * next_value
        return [best_move, value]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: if game already finished, return the corresponding score, else:
      1. the more food left, the worse the state is (score is higher but return the negative inverse of the score)
      2. the closer the closest food the better the state is
      3. capsules is good so the more left the worst the state is
      4. minus the score of current state as the higher the score the better
      5. the closer the ghost the worse, use exponential function here to amplify the effect
      6. return the negative inverse so the higher score represents the better state

    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return -float("inf")
    score = 100 * currentGameState.getNumFood()
    pacman_pos = currentGameState.getPacmanPosition()
    min_dis = float("inf")
    for food in currentGameState.getFood().asList():
        distance = manhattanDistance(pacman_pos, food)
        if distance < min_dis: min_dis = distance
    if min_dis < float("inf"): score += min_dis
    score += 2 ** min(manhattanDistance(g, pacman_pos) for g in currentGameState.getGhostPositions())
    score += 10 * len(currentGameState.getCapsules())
    score -= currentGameState.getScore()
    return -score

# Abbreviation
better = betterEvaluationFunction
