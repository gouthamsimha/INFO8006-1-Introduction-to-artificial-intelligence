# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

    def update_belief_state(self, evidences, pacman_position):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        beliefStates = self.beliefGhostStates

        # XXX: Your code here

        
        height = self.walls.height
        width  =  self.walls.width
        
        z=0
        while z<len(beliefStates):
            
            for m in range(0,width):

                for n in range(0,height):

                    if (not self.walls[m][n] ) and (not pacman_position == (m,n)) :
                        
                        currDistance = util.manhattanDistance( pacman_position , (m,n) )
                        sigma = np.sqrt(self.sensor_variance)
                        mu    = currDistance
                        sModel = ( 1/(np.sqrt(2*np.pi) * sigma) ) * np.exp(-np.power(evidences[z] - mu, 2.) / (2 * np.power(sigma, 2.)))
                        tModel = util.Counter()

                        if self.ghost_type == "scared":   k = 3
                        if self.ghost_type == "afraid":   k = 1
                        if self.ghost_type == "confused": k = 0

                        
                        
                        for i in range(0,width):
                            for j in range(0,height):

                                succDistance = util.manhattanDistance(pacman_position,(i,j))

                                if ( (m+1 == i and n == j) or (m-1 == i and n == j) or (m == i and n+1 == j)  or (m == i and n-1 == j) ) and (not self.walls[i][j]):

                                    if succDistance > currDistance:
                                        tModel[(i,j)] = np.power(2, k) 
                                    else: 
                                        tModel[(i,j)] = 1

                                else:
                                    tModel[(i,j)] = 0 
                            
                        tModel.normalize()

                        epsilon = 0 

                        for i in range(0,width):
                            for j in range(0,height):

                                epsilon = epsilon + tModel[(i,j)] * beliefStates[z][i][j]
                        
                        
                        beliefStates[z][m][n] = sModel*epsilon
                        
                    else : 
                        beliefStates[z][m][n] = 0
            #On peut mtn calculer alpha.

            alpha = np.sum(beliefStates[z])
            beliefStates[z] = np.divide(beliefStates[z], alpha)
            
            z = z + 1
        
        
        # XXX: End of your code
        

        self.beliefGhostStates = beliefStates

        return beliefStates

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for p in positions:
            true_distance = util.manhattanDistance(p, pacman_position)
            noisy_distances.append(
                np.random.normal(loc=true_distance,
                                 scale=np.sqrt(self.sensor_variance)))

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        num="16"
        mon_fichier = open("damso"+str(num)+".txt", "a")
        b = np.where( belief_states[0].max() == belief_states[0] )
        B = (b[0][0],b[1][0])
        g = state.getGhostPosition(1)

        d = util.manhattanDistance(B,g)
        

        mon_fichier.write(str(belief_states.var()*100)+"\t"+str(d)+"\n")
        mon_fichier.close()
        
        pass

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        newBeliefStates = self.update_belief_state(self._get_evidence(state),
                                                   state.getPacmanPosition())
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates
