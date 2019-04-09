"""
blackjack.py

Holds the implementation of Programming Assignment 3 for AI.  This script implements a blackjack
like game that has a lower and upper target, along with a number of cards.  The script prints
to stdout the dynamic programming created arrays play (denotes whether player x draws or not at
state p1_score and p2_score) and prob (the probability that x wins given the corresponding play
in the play array).

Author: Mark Xavier
"""

import sys

class Blackjack:

    def __init__(self, n_cards, l_target, u_target):
        """
        The initialization function for the class.  This creates a blackjack object that computes
        the play and prob arrays.

        Args:
            n_cards <int>: the number of individual card values
            l_target <int>: the lower target to win the blackjack game
            u_target <int>: the upper target to win the blackjack game

        Returns:
            <blackjack.Blackjack>
        """

        self.n_cards = n_cards
        self.l_target = l_target
        self.u_target = u_target
        self.cards = range(1, n_cards + 1)
        self.play = [[0 for i in xrange(l_target)] for j in xrange(l_target)]
        self.prob = [[0.0 for i in xrange(l_target)] for j in xrange(l_target)]

        self.compute_play_and_prob_arrays()
        print self

    def compute_prob_win_if_p1_draws(self, p1_score, p2_score):
        """
        Computes the probability that player 1 wins if the player draws this turn given that player
        2 drew the last turn.

        Args:
            p1_score <int>: the current score for player 1
            p2_score <int>: the current score for player 2

        Returns:
            <float>: the probability player 1 wins if he draws this turn
        """

        prob_p1_wins = 0.0
        for card in self.cards:
            prob_p2_wins = 0.0
            if p1_score + card > self.u_target:
                prob_p2_wins = 1.0
            elif p1_score + card >= self.l_target:
                prob_p2_wins = 0.0
            else:
                prob_p2_wins = self.prob[p2_score][p1_score + card]
            prob_p1_wins = prob_p1_wins + (1 - prob_p2_wins) / self.n_cards

        return prob_p1_wins

    def compute_prob_win_if_p1_stays(self, p1_score, p2_score):
        """
        Computes the probability that player 1 wins if the player doesn't draw this turn.

        Args:
            p1_score <int>: the current score for player 1
            p2_score <int>: the current score for player 2

        Returns:
            <float>: the probability player 1 wins if he stays this turn
        """

        if p2_score > p1_score:
            return 0
        return 1 - self.prob[p2_score][p1_score]

    def compute_move(self, p1_score, p2_score):
        """
        Computes the ideal move to make for player one given the current state of the game.

        Args:
            p1_score <int>: the current score for player 1
            p2_score <int>: the current score for player 2

        Returns:
            None - updates the play and prob arrays with the best move to make and its corresponding
                   probability.
        """

        if p1_score < p2_score:
            self.play[p1_score][p2_score] = True
            self.prob[p1_score][p2_score] = self.compute_prob_win_if_p1_draws(p1_score, p2_score)
        else:
            p1_wins_drawing = self.compute_prob_win_if_p1_draws(p1_score, p2_score)
            p1_wins_staying = self.compute_prob_win_if_p1_stays(p1_score, p2_score)

            if p1_wins_drawing > p1_wins_staying:
                self.play[p1_score][p2_score] = True
                self.prob[p1_score][p2_score] = p1_wins_drawing
            else:
                self.play[p1_score][p2_score] = False
                self.prob[p1_score][p2_score] = p1_wins_staying

        return

    def compute_play_and_prob_arrays(self):
        """
        The starter method that walks through the play and prob arrays in the correct order and
        fills in the appropriate play and prob values for player 1.

        Args:
            None

        Returns:
            None
        """

        for i in xrange(self.l_target * 2, -1, -1):
            outstr = ''
            start_col = max(0, i - self.l_target)
            count = min(i, self.l_target - start_col, self.l_target)
            for j in xrange(0, count):
                p1_score = start_col + j
                p2_score = min(self.l_target, i) - j - 1
                self.compute_move(p1_score, p2_score)

    def __str__(self):
        """
        A utility function for easier printing.
        """

        translator = {True:'D', False:'P'}
        outstr = 'Play Array\n'
        for row in self.play:
            outstr += ' '.join([translator[bl] for bl in row])
            outstr += '\n'
        outstr += '\nProb Array\n'
        for row in self.prob:
            outstr += ' '.join('%.2f' % (p) for p in row)
            outstr += '\n'

        return outstr

def print_usage():
    """
    A utility function to print usage in the case of incorrect use of this scripts methods.
    """

    print 'Usage:'
    print '> python blackjack.py <int: number of cards> <int: lower target> <int: upper target>\n'

    return

def main():
    """
    The main entry-point for this script.
    """

    if len(sys.argv) < 4:
        print '\n[*]ERROR: Too few arguments, this script expected exactly 3 command line arguments.'
        print_usage()
        sys.exit(1)
    elif len(sys.argv) > 4:
        print '\n[*]ERROR: Too many arguments, this script expected exactly 3 command line arguments.'
        print_usage()
        sys.exit(1)
    else:
        blackjack = Blackjack(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))


if __name__ == '__main__':
    main()