# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
from math import*

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

def MinValue(state,depth,visited,grid):

    """
    Try to maximize the action of the ghost.
    Arguments:
    ----------
    - `state`: the current game state.
    - `visited`: The data structure that store and look-up values of positions.
    - `depth`: Depth when the function have to stop.
    - `grid`: the current state's boolean grid of the position of the dots.
    Return:
    -------
    - A floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """
    
    visited_ = visited.copy()

    if depth == 0 or state.isWin() or state.isLose() :
        return eval(state,grid)

    if not key(state) in visited_: 
        visited_.add(key(state))
    else : 
        return float("-inf")
    
    v = float("inf")
    
    for nextState in state.generateGhostSuccessors(1):
        v = min(v,MaxValue(nextState[0],depth-1,visited_,grid))
    
    return v

def MaxValue(state,depth,visited,grid):

    """
    Try to maximize the action of the pacman.
    Arguments:
    ----------
    - `state`: the current game state.
    - `visited`: The data structure that store and look-up values of positions.
    - `depth`: Depth when the function have to stop.
    - `grid`: the current state's boolean grid of the position of the dots.
    Return:
    -------
    - A floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """

    visited_ = visited.copy()
    
    if depth == 0 or state.isWin() or state.isLose() :
        return eval(state,grid)

    if not key(state) in visited_: 
        visited_.add(key(state))
    else : 
        return float("inf")

    v = float("-inf")

    for nextState in state.generatePacmanSuccessors():
        v = max(v,MinValue(nextState[0],depth-1,visited_,grid))
    
    return v

def eval(state, grid):
    
    """
    Returns a score that defines the final numeric value for a game that ends for Min or Max.
    Arguments:
    ----------
    - `state`: the current game state.
    - `grid`: the current state's boolean grid of the position of the dots.
    
    Return:
    -------
    - A floating-point object that defines the final numeric value for a game that ends for Min or Max.
    """

    if manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(1)) < 1:
        return float("-inf") 
    
    if manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(1)) < 3:
        return 0.75*-(closestDotDistance(state,grid)) + 0.25*manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(1))
    else : return  -(closestDotDistance(state,grid))

def closestDotDistance(state,grid):

    """
    Search the closest euclidean distance between the pacman and the dots.
    Arguments:
    ----------
    - `state`: the current game state.
    - `grid`: the current state's boolean grid of the position of the dots.
    
    Return:
    -------
    - A floatinf-point value that is the closest distance. 
    """

    distances = [ manhattanDistance(pos,state.getPacmanPosition())for pos in grid.asList() ]
    i = distances.index(min(distances)) # index of the closest dot

    return (grid.asList()[i][0] - state.getPacmanPosition()[0])**2  +  (grid.asList()[i][1] - state.getPacmanPosition()[1])**2 

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.visited = set()
        

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
        
        
        action = list()
        score = list()

        if not key(state) in self.visited: 
            self.visited.add(key(state))

        for nextState in state.generatePacmanSuccessors() :
            if key(nextState[0]) not in self.visited:
                score.append(MinValue(nextState[0],1,set(),state.getFood()))
                action.append(nextState[1])

        try:
             return action[score.index(max(score))]


        except IndexError:
            return Directions.STOP
