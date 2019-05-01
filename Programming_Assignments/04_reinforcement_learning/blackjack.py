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
        self.cards = [i for i in xrange(k+1)]

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

    def get_f(self, player, other):
        """
        Calculates the "f" array described in the assignment, which holds for any given state of
        p1_score, p2_score, and last_player_drew, the ratio of times won drawing the number of cards
        indicated by the position in the array.  Therefore, f[1] = the ratio of times won in the
        current state after drawing 1 card.
        """

        win_state = self.win_count[player.score][other.score][other.drew_last_turn]
        lose_state = self.lose_count[player.score][other.score][other.drew_last_turn]
        f = []
        games_played_in_state = 0
        for i in xrange(len(win_state)):
            if win_state[i] + lose_state[i] == 0:
                f.append(0.5)
            else:
                f.append(win_state[i] / float(win_state[i] + lose_state[i]))
            games_played_in_state += win_state[i] + lose_state[i]
        return f, games_played_in_state

    def get_best_move(self, f):
        """
        Given the "f" array, determines the highest win ratio of all possible plays in the given
        state.
        """

        best = -1
        best_index = -1
        for index, value in enumerate(f):
            if value > best:
                best = value
                best_index = index
        return best, best_index

    def get_sum_of_other_moves(self, f, best_move_index):
        """
        Given the "f" array and the best_move of all enumerated in this state, sums the ratio of
        wins drawing cards that are not the best move.
        """

        sum_of_other_moves = 0
        for i in xrange(len(f)):
            if i != best_move_index:
                sum_of_other_moves += f[i]
        return sum_of_other_moves

    def calculate_probabilities(self, f, B, B_index, g, T):
        """
        Given the background arrays and values as outlined in the assignment, calculates the
        probability of drawing a given number of cards from 0...(k+1) given the win ratio. 
        """

        probs = [None for i in xrange(len(f))]
        p_best = (T * B + self.m) / (T * B + ((self.k + 1) * self.m))
        for index, value in enumerate(f):
            if index == B_index:
                probs[index] = p_best
            else:
                probs[index] = (1-p_best) * (T * f[i] + self.m) / (g * T + self.k * self.m)
        return probs

    def sample(self, probs):
        """
        Randomly (yet less randomly over time) determines the number of cards to draw
        """

        u = [None for i in xrange(len(probs))]
        u[0] = probs[0]
        for i in xrange(1, len(probs)):
            u[i] = sum(u[:i]) + probs[i]

        target = random.random()
        for index, p in enumerate(u):
            if target < p:
                return index

    def get_number_of_cards_to_draw(self, player, other):
        """
        """

        f, T = self.get_f(player, other)
        b, b_index = self.get_best_move(f)
        g = self.get_sum_of_other_moves(f, b_index)
        probs = self.calculate_probabilities(f, b, b_index, g, T)
        return self.sample(probs)

    def add_move(self, p1, p2, cards_drawn):
        """
        """

        if(p1.score < self.l_target and p2.score < self.l_target):
            self.moves.append([p1.score, p2.score, p2.drew_last_turn, cards_drawn])

    def draw_card(self):
        """
        """

        return random.choice(self.cards)

    def player_plays(self, player, other):
        """
        """

        cards_to_draw = self.get_number_of_cards_to_draw(player, other)
        self.add_move(player, other, cards_to_draw)
        for i in xrange(cards_to_draw):
            player.draw(self.draw_card())

        if player.lost_game or (not player.lost_game and player.score >= self.l_target):
            self.game_over = True

        if cards_to_draw == 0:
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
                if self.game_over:
                    break
                elif self.check_no_play_made():
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
            pscore, oscore, drew, cards = element
            if current_player == 1:
                p1_array[pscore][oscore][drew][cards] += 1
            else:
                p2_array[pscore][oscore][drew][cards] += 1
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
    parser = argparse.ArgumentParser(description=('Blackjack game as described in programming '
                                                  'assignment 4 for Artificial Intelligence with '
                                                  'Prof. Davis at NYU, Spring 2019'))
    parser.add_argument('N', help='The highest value card', type=int)
    parser.add_argument('LTarget', help='The lowest winning score', type=int)
    parser.add_argument('UTarget', help='The highest winning score', type=int)
    parser.add_argument('K', help='The maximum number of cards that can be drawn per turn', type=int)
    parser.add_argument('M', help='A floating-point value', type=float)
    parser.add_argument('N_Games', help='The number of games to play', type=int)
    args = parser.parse_args()

    blackjack = Blackjack(args.N, args.LTarget, args.UTarget, args.K, args.M, args.N_Games)
    blackjack.run_simulation()
    print blackjack.win_count

if __name__ == '__main__':
    driver()