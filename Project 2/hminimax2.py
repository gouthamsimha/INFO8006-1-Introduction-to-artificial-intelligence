# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.
    Arguments:
    ----------
    - `state`: the current game state. 
    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return (state.getPacmanPosition(), state.getFood(), state.getGhostPosition(1),state.getGhostDirection(1))

def MinValue(state,visited, depth):

    """
    Try to maximize the action of the ghost.
    Arguments:
    ----------
    - `state`: the current game state.
    - `visited`: the data structure that store and look-up values of positions.
    - `depth`: depth when the function have to stop.

    Return:
    -------
    - a floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """

    if cutOff(state,depth) :
        return eval(state)
    
    visited_ = visited.copy()
    score = []

    if not key(state) in visited_: 
        visited_.add(key(state))
    else : 
        return float("-inf")

    for nextState in state.generateGhostSuccessors(1):
        value = MaxValue(nextState[0],visited_,depth+1)
        score.append(value)
    
    return min(score)

def MaxValue(state,visited,depth):

    """
    Try to maximize the action of the pacman.
    Arguments:
    ----------
    - `state`: the current game state.
    - `visited`: The data structure that store and look-up values of positions.
    - `depth`: depth when the function have to stop.
    
    Return:
    -------
    - A floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """

    if cutOff(state,depth) :
        return eval(state)

    visited_ = visited.copy()
    
    score = []

    if not key(state) in visited_: 
        visited_.add(key(state))
    else : 
        return float("inf")

    for nextState in state.generatePacmanSuccessors():
        value = MinValue(nextState[0],visited_,depth+1)
        score.append(value)

    return max(score)

def eval(state):

    """
    Returns a score that defines the final numeric value for a game that ends for Min or Max.
    Arguments:
    ----------
    - `state`: the current game state.
    
    Return:
    -------
    - A floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """

    if manhattanDistance(state.getPacmanPosition(), state.getGhostPosition(1)) < 2:
        return float("-inf")
    return -0.5*state.getNumFood() + 0.5*manhattanDistance(state.getPacmanPosition(), state.getGhostPosition(1))

def cutOff(state,depth):
    """
    Decide when to stop expanding a state.
    Arguments:
    ----------
    - `state`: the current game state.
    - `depth`: depth when the function have to stop.
    
    Return:
    -------
    - A boolean value 
    """

    return depth >= 3 or state.isWin() or state.isLose()

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.visited = dict()

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        v = []
        if key(state) not in self.visited:
            self.visited[key(state)]= set()
        
        PSuccessors = state.generatePacmanSuccessors()
        for nextState,action in PSuccessors :

            if key(nextState) not in self.visited[key(state)]:
                
                value = MinValue(nextState,set(self.visited.keys()),0)

                v.append([value,action])

        if not len(v):
            return Directions.STOP
        best_value,best_action = max(v)
        self.visited[key(state)].add( key( PSuccessors[v.index([best_value,best_action])][0] ) )
        
        try:
            return best_action

        except IndexError:
            return Directions.STOP
