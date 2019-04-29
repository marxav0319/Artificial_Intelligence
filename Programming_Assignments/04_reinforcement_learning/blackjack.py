"""
"""

import argparse

class Blackjack:

    def __init__(self, n, l_target, u_target, k, m, n_games):
        """
        The initializer for the blackjack game.

        Args:
            n <int>: the highest valued card
            l_target <int>: the lowest winning score
            u_target <int>: the highest winning score
            k <int>: the number of cards that can be drawn on a given turn
            m <float>: the learning rate
            n_games <int>: the number of games to play

        Returns:
            <blackjack.Blackjack>: an instance of the blackjack game, ready for simulation.
        """

        # Parameters from the command line or game description
        self.n = n
        self.l_target = l_target
        self.u_target = u_target
        self.k = k
        self.m = m
        self.n_games = n_games
        self.win_count = self._construct_array()
        self.lose_count = self._construct_array()

        # Variables defined for the script
        self.game_over = False
        self.p1_score = 0
        self.p2_score = 0

    def _construct_array(self):
        """
        Constructs the L x L x 2 x K+1 arrays required by the prompt.

        Args:
            None

        Returns:
            <list>: a 4-D array with the dimensions specified above 
        """

        empty_list = []
        for i in xrange(self.l_target):
            temp_1 = []
            for j in xrange(self.l_target):
                temp_2 = []
                for d in xrange(2):
                    temp_2.append([0 for i in xrange(self.k + 1)])
                temp_1.append(temp_2)
            empty_list.append(temp_1)
        return empty_list

    def play_game(self):
        """
        """

        while(not self.game_over):
            draw()
            continue

    def run_simulation(self):
        """
        """

        for game in xrange(self.n_games):
            continue

        return

def driver():
    """
    The driver program for this script.
    """

    print
    parser = argparse.ArgumentParser(description=('Blackjack game as described in programming'
                                                  'assignment 4 for Artificial Intelligence with'
                                                  'Prof. Davis at NYU, Spring 2019'))
    parser.add_argument('N', help='The highest value card', type=int)
    parser.add_argument('LTarget', help='The lowest winning score', type=int)
    parser.add_argument('UTarget', help='The highest winning score', type=int)
    parser.add_argument('K', help='The maximum number of cards that can be drawn per turn', type=int)
    parser.add_argument('M', help='A floating-point value', type=float)
    parser.add_argument('N_Games', help='The number of games to play', type=int)
    args = parser.parse_args()

    blackjack = Blackjack(args.N, args.LTarget, args.UTarget, args.K, args.M, args.N_Games)

if __name__ == '__main__':
    driver()