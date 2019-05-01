"""
"""

import argparse
import random

class Player:
    
    def __init__(self, u_target):
        """
        """

        self.u_target = u_target
        self.score = 0
        self.drew_last_turn = 1
        self.lost_game = False

    def draw(self, card):
        """
        """

        self.score += card
        if self.score > self.u_target:
            self.lost_game = True

    def stayed_last_turn(self):
        """
        """

        return False if self.drew_last_turn else True

    def clear(self):
        """
        """

        self.score = 0
        self.drew_last_turn = 1
        self.lost_game = False

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
        self.player_1 = Player(u_target)
        self.player_2 = Player(u_target)
        self.moves = []

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

    def _sample(self):
        """
        """

        prob = 1/float(self.k + 1)
        probs = [(prob * i) + prob for i in xrange(self.k + 1)]
        x = random.random()
        for i in xrange(self.k + 1):
            if x < probs[i]:
                return i

    def draw(self):
        """
        """

        return self._sample()

    def add_move(p1, p2, cards_drawn):
        """
        """

        self.moves.append([p1.score, p2.score, p1.drew_last_turn, cards_drawn])

    def player_plays(self, player, other):
        """
        """

        card = self.draw()
        self.add_move(player, other, card)
        player.draw(card)

        if player.lost_game:
            self.game_over = True

        if card == 0:
            player.drew_last_turn = 0

    def check_no_play_made(self):
        """
        """

        return self.player_1.stayed_last_turn() and self.player_2.stayed_last_turn()

    def play_game(self):
        """
        """

        while(not self.game_over):
            if self.check_no_play_made():
                self.game_over = True
            else:
                self.player_plays(self.player_1, self.player_2)
                if self.check_no_play_made():
                    self.game_over = True
                else:
                    self.player_plays(self.player_2, self.player_1)

    def determine_winner(self):
        """
        """

        if not self.player_1.lost_game and not self.player_2.lost_game:
            if self.player_1.score < self.player_2.score:
                self.player_1.lost_game = True
            else:
                self.player_2.lost_game = True

    def update(self):
        """
        """

        p1_array = self.win_count
        p2_array = self.lose_count
        self.determine_winner()
        if self.player_1.lost_game:
            p1_array = self.lose_count
            p2_array = self.win_count

        current_player = 1
        for element in self.moves:
            if current_player == 1:
                p1_array[element[0], element[1], element[2], element[3]] += 1
            else:
                p2_array[element[0], element[1], element[2], element[3]] += 1
            current_player = 2 if current_player == 1 else 1

    def clear(self):
        """
        """

        self.player_1.clear()
        self.player_2.clear()
        self.game_over = False
        self.moves = []

    def run_simulation(self):
        """
        """

        for game in xrange(self.n_games):
            self.play_game()
            self.update()
            self.clear()
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