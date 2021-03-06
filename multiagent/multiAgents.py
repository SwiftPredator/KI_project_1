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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        """ The idea is to look at the nearest food and the nearest ghost and evaluate a score out of the distances """
        foodList = newFood.asList()
        capsuleListSucc = successorGameState.getCapsules()
        capsuleListCurr = currentGameState.getCapsules()
        realFoodList = currentGameState.getFood().asList()

        #compute distance to next food
        distanceToNextFood = 99999
        for food in foodList:
            temp_dist = manhattanDistance(newPos, food)
            if temp_dist < distanceToNextFood:
                distanceToNextFood = temp_dist

        # compute nearest distance to active and passive ghost
        dist_pGhost, dist_aGhost = 0, 0
        for ghost in newGhostStates:
            temp_dist = manhattanDistance(newPos, ghost.getPosition())
            if(ghost.scaredTimer):
                if(dist_pGhost == 0):
                    dist_pGhost = temp_dist
                elif(dist_pGhost > temp_dist):
                    dist_pGhost = temp_dist
            else:
                if(dist_aGhost == 0):
                    dist_aGhost = temp_dist
                elif(dist_aGhost > temp_dist):
                    dist_aGhost = temp_dist
                
        if(dist_aGhost == 0):
            dist_aGhost = 5

         #compute distance to closest capsule
        dist_capsule = 999999
        for capsule in capsuleListSucc:
          temp_dist = manhattanDistance(newPos, capsule)
          if temp_dist < dist_capsule and temp_dist != 0:
            dist_capsule = temp_dist

        #evaluation
        score_nextFood = 0
        score_nextCapsule = 0
        score_nextAGhost = 0
        score_nextPGhost = 0
        if len(foodList)<len(realFoodList):
            score_nextFood = 10

        if len(capsuleListSucc)<len(capsuleListCurr):
            score_nextCapsule = 20

        if(dist_aGhost < 3):
            #print("GHOST NEAR")
            score_nextAGhost = -100
        else:
            score_nextAGhost = 5
        #with the information we can compute a score
        score = score_nextFood + score_nextAGhost + score_nextPGhost + score_nextCapsule + (1/distanceToNextFood) + (1/dist_capsule)
        
        #print("stats: ", score)
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def minimax_max(state, depth, player=0):
            if(state.isWin() or state.isLose() or depth == 0):
                return self.evaluationFunction(state), Directions.STOP
            actions = state.getLegalActions(player)
            pos_scores = []
            for action in actions:
                pos_scores.append(minimax_min(state.generateSuccessor(player, action), depth - 1, 1))
            maxScore = max(pos_scores)
            #print(maxScore, actions[pos_scores.index(max(pos_scores))])
            return maxScore, actions[pos_scores.index(max(pos_scores))]

        def minimax_min(state, depth, player=1):
            if(state.isWin() or state.isLose() or depth == 0):
                #print("depth:", depth)
                return self.evaluationFunction(state)
            actions = state.getLegalActions(player)
            pos_scores = []
            for action in actions:
                #check if last agent, so its pacmans turn.
                if(player == state.getNumAgents() - 1):
                    pos_scores.append(minimax_max(state.generateSuccessor(player, action), depth - 1, 0)[0])
                else:
                    pos_scores.append(minimax_min(state.generateSuccessor(player, action), depth, player + 1))
            
            minScore = min(pos_scores)
            
            return minScore


        print(self.depth)
        return minimax_max(gameState, self.depth*2, 0)[1]
        
      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def maxABT(state, depth, alpha, beta, player=0):
            if(state.isWin() or state.isLose() or depth == 0):
                return self.evaluationFunction(state), Directions.STOP
            actions = state.getLegalActions(player)
            pos_score = 0
            highest_score = float("-inf")
            best_action = Directions.STOP
            for action in actions:
                pos_score = minABT(state.generateSuccessor(player, action), depth - 1, alpha, beta, 1)
                if(pos_score > highest_score):
                    highest_score = pos_score
                    best_action = action
                alpha = max(alpha, highest_score)
                if(highest_score > beta):
                    return pos_score, action 
            return highest_score, best_action

        def minABT(state, depth, alpha, beta, player=1):
            if(state.isWin() or state.isLose() or depth == 0):
                return self.evaluationFunction(state)
            actions = state.getLegalActions(player)
            pos_score =  0
            lowest_score = float("inf")
            for action in actions:
                if(player == state.getNumAgents() -1):
                    pos_score = maxABT(state.generateSuccessor(player, action), depth - 1, alpha, beta, 0)[0]
                else:
                    pos_score = minABT(state.generateSuccessor(player, action), depth, alpha, beta, player + 1)
                if(pos_score < lowest_score):
                    lowest_score = pos_score
                beta = min(beta, lowest_score)
                if(lowest_score < alpha):
                    return lowest_score
            return lowest_score
                    

        return maxABT(gameState, self.depth*2, float("-inf"), float("inf"), 0)[1]
        

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
        def value(state, depth, player=0):
            if(state.isWin() or state.isLose() or depth == 0):
                return self.evaluationFunction(state), Directions.STOP
            elif player == 0:
                return maxABT(state, depth, player)
            else:
                return minABT(state, depth, player)

        def maxABT(state, depth, player=0):
            if(state.isWin() or state.isLose() or depth == 0):
                return self.evaluationFunction(state), Directions.STOP
            actions = state.getLegalActions(player)
            pos_score = 0
            highest_score = float("-inf")
            best_action = Directions.STOP
            for action in actions:
                pos_score = value(state.generateSuccessor(player, action), depth - 1, 1)[0]
                if(pos_score > highest_score):
                    highest_score = pos_score
                    best_action = action
            return highest_score, best_action

        def minABT(state, depth, player=1):
            if(state.isLose() or depth == 0):
                return self.evaluationFunction(state), Directions.STOP
            actions = state.getLegalActions(player)
            pos_score =  0
            score = 0
            for action in actions:
                if(player == state.getNumAgents() -1):
                    pos_score = value(state.generateSuccessor(player, action), depth - 1, 0)[0]
                else:
                    pos_score = value(state.generateSuccessor(player, action), depth, player + 1)[0]
                p = 1/len(actions)
                score += p*pos_score
            return score, Directions.STOP
                    

        return value(gameState, self.depth*2, 0)[1]

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
