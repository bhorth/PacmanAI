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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        #find the closest food
        foodDistance = float("inf") #set food distance as maximum value
        for food in newFood.asList():
            
            #get distance from current pacman position to food using manhattan distance
            distance = util.manhattanDistance(newPos, food)
            
            #find the closest food distance
            if distance <= foodDistance:
                foodDistance = distance
                    
        ghostDistance = 1
        nearbyDistance = 0
        
        #find the distance from current pacman position to ghosts using manhattan distance
        for ghost in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost)
            
            #if the ghost is close to pacman increase the nearby distance
            if distance <= 1:
                nearbyDistance += distance
            
            #add the distance to the ghost distance
            ghostDistance += distance
        
        #subtract the nearby distance from the total ghost distance
        ghostDistance = ghostDistance - nearbyDistance
        
        #use the reciprocal values of the food and ghost distances
        updatedScore = (1/foodDistance - 1/ghostDistance)
        
        #add updated score to the successor game state score
        return successorGameState.getScore() + updatedScore


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
        
        def miniMaxAgent(state, depth, agentIndex):
            
            #return evaluation function if game is won or lost or the depth is reached
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            #if agent index is 0 that is pacman so get the maximum value
            if agentIndex == 0:
                maximum = float("-inf")
                actions = state.getLegalActions(agentIndex) #pacmans legal actions
                
                #get successor from all actions and set maximum as the largest value found
                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    maximum = max(maximum, miniMaxAgent(successor, depth, 1)) #pass agent index as 1 to move onto the ghosts (min)
                
                return maximum
            
            #if agent index is greater than 0 it is a ghost so get the minimum value
            else:
                minimum = float("inf")
                actions = state.getLegalActions(agentIndex)
                
                #get successor from all actions and set the minimum to the smallest value found
                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action) #ghosts legal actions
                    
                    #if all ghosts have found a min, increase depth and set agent back to pacman (max)
                    if state.getNumAgents() -1 == agentIndex:
                        minimum = min(minimum, miniMaxAgent(successor, depth + 1, 0))
                    
                    #increase agent index to get the next ghost
                    else:
                        minimum = min(minimum, miniMaxAgent(successor, depth, agentIndex + 1))
                return minimum
        
        score = float("-inf")
        direction = None
        
        #get all the legal actions in the game state
        legalActions = gameState.getLegalActions()
        
        #get successor from each action in the game
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            
            #start at depth 0 and agent index 1
            value = miniMaxAgent(successor, 0, 1)
            
            #find the largest value and set direction to the action that returned that value
            if score < value:
                score = value
                direction = action
        
        return direction
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
