"""
blackjack.py

Implements Programming Assignment 4 for Professor Ernest Davis' Artificial Intelligence Class at
NYU GSAS, Spring 2019.

For help with usage, enter "> python blackjack.py -h" in a terminal window.

Author: Mark Xavier
"""

import argparse
import random

class Player:
    
    def __init__(self, index, u_target):
        """
        An implementation of the player class - this is simply a wrapper around scores and some
        game state updating.

        Args:
            index <int>: The player index (in this game, either 1 or 2).
            u_target <int>: The lower target to reach to win the game:

        Returns:
            <player.Player>
        """

        self.index = index
        self.u_target = u_target
        self.score = 0
        self.drew_last_turn = 1
        self.lost_game = False

    def draw(self, card):
        """
        Given a card to draw, adds the card to the player's score, then determines if the player
        has lost the game.

        Args:
            card <int>: The card that was drawn

        Returns:
            None
        """

        self.score += card
        if self.score > self.u_target:
            self.lost_game = True

    def stayed_last_turn(self):
        """
        Returns whether or not the player passed on the last turn.

        Args:
            None

        Returns:
            <bool>: True if the player passed last turn, else false.
        """

        return False if self.drew_last_turn else True

    def clear(self):
        """
        Resets any state variables for this player so that the game can be played again (such as
        the score, whether the player lost the game, etc.)

        Args:
            None

        Returns:
            None
        """

        self.score = 0
        self.drew_last_turn = 1
        self.lost_game = False

class Blackjack:

    def __init__(self, n, l_target, u_target, k, m, n_games, verbose, per_game_verbose):
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
        self.verbose = verbose
        self.per_game_verbose = per_game_verbose

        # Variables defined for the script
        self.game_over = False
        self.player_1 = Player(1, u_target)
        self.player_2 = Player(2, u_target)
        self.moves = []
        self.cards = [i for i in xrange(1, n+1)]

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

        Args:
            player <player.Player>: The player who has play
            other <player.Player>: The player who is waiting on the active player

        Returns:
            <list: float>: A list of ratios of wins to total games
            <int>: The number of games played in state p1_score, p2_score, p1_drew_last_turn
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

        Args:
            f <list: float>: A list of probabilities of win ratios, which each index in f serving as
                             the win ratio after drawing the number of cards indicated by "index".

        Returns:
            <float>: The highest win ratio
            <int>: The index in f holding the highest win ratio
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

        Args:
            f <list: float>: A list of win ratios
            best_move_index <int>: The index in f holding the move with the highest win ratio

        Returns:
            <float>: The sum of all win ratios that do not belong to best_move_index.
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

        Args:
            f <list: float>: A list of win ratios
            B <float>: The win ratio for the best move (in f)
            B_index <int>: The index of B in f, f[B_index] = B
            g <float>: The sum of win ratios belonging to moves that are not B
            T <int>: The number of games played in a given state p1_score, p2_score, p1_drew_last_turn

        Returns:
            <list: float>: A list of probabilities, with each probability describing the probability
                           of winning given drawing the number of cards specified as the index of
                           the list.
        """

        probs = [None for i in xrange(len(f))]
        p_best = (T * B + self.m) / ((T * B) + ((self.k + 1) * self.m))
        for index, value in enumerate(f):
            if index == B_index:
                probs[index] = p_best
            else:
                probs[index] = (1-p_best) * (T * value + self.m) / ((g * T) + (self.k * self.m))
        return probs

    def sample(self, probs):
        """
        Randomly (yet less randomly over time) determines the number of cards to draw.

        Args:
            probs <list: float>: The list of probabilities for winning given drawing the number of
                                 cards specified by probs[index].

        Returns:
            <int>: The number of cards to draw.
        """

        u = [None for i in xrange(len(probs))]
        u[0] = probs[0]
        for i in xrange(1, len(probs)):
            u[i] = sum(u[:i]) + probs[i]

        target = random.random()
        for index, p in enumerate(u):
            if target <= p:
                return index
        return self.k

    def get_number_of_cards_to_draw(self, player, other):
        """
        Given the current state of the game, determines the number of cards for the current player
        to draw from 0...self.k.

        Args:
            player <player.Player>: The player that is currently able to play
            other <player.Player>: The opponenent of the currently active player

        Returns:
            <int>: The number of cards to draw.
        """

        f, T = self.get_f(player, other)
        b, b_index = self.get_best_move(f)
        g = self.get_sum_of_other_moves(f, b_index)
        probs = self.calculate_probabilities(f, b, b_index, g, T)
        return self.sample(probs)

    def add_move(self, p1, p2, cards_drawn):
        """
        Adds moves that were done to a list of moves done for the game.  This list of moves is then
        used at the end of each game to update all game states traversed in the corresponding win/lose
        arrays.

        Args:
            p1 <player.Player>: The player that just played
            p2 <player.Player>: The non-active player
            cards_drawn <int>: The number of cards p1 drew.

        Returns:
            None
        """

        if(p1.score < self.l_target and p2.score < self.l_target):
            self.moves.append([p1.score, p2.score, p2.drew_last_turn, cards_drawn])

    def draw_card(self):
        """
        Draws a random number from 1 ... (N + 1).

        Args:
            None

        Returns:
            <int>: The card that was drawn for the currently active player.
        """

        return random.choice(self.cards)

    def player_plays(self, player, other):
        """
        Simulates the current active player playing the game by determining the number of cards to
        draw given the Assignment Prompt, then add that move to the list of moves and determine if
        a winner has been found.

        Args:
            player <player.Player>: The current active player
            other <player.Player>: The non-active player

        Returns:
            None - state update
        """

        cards_to_draw = self.get_number_of_cards_to_draw(player, other)
        self.add_move(player, other, cards_to_draw)
        for i in xrange(cards_to_draw):
            player.draw(self.draw_card())

        if player.lost_game or (not player.lost_game and player.score >= self.l_target):
            self.game_over = True

        if cards_to_draw == 0:
            player.drew_last_turn = 0
        else:
            player.drew_last_turn = 1

    def check_no_play_made(self):
        """
        Checks if (at a given point in time) player 1 and player 2 both passed on their last turn.

        Args:
            None

        Returns:
            <bool>: True if both players stayed their last turn, else False.
        """

        return self.player_1.stayed_last_turn() and self.player_2.stayed_last_turn()

    def play_game(self):
        """
        Plays a single game of blackjack with 2 players.

        Args:
            None

        Returns:
            None
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
        Determines the winner of the game, this is helpful if there's a draw (both players pass
        for instance) and we need to determine how to update the win/lost arrays.

        Args:
            None

        Returns:
            None
        """

        if not self.player_1.lost_game and not self.player_2.lost_game:
            if self.player_1.score >= self.l_target and self.player_1.score <= self.u_target:
                self.player_2.lost_game = True
            elif self.player_2.score >= self.l_target and self.player_2.score <= self.u_target:
                self.player_1.lost_game = True
            elif self.player_1.score < self.player_2.score:
                self.player_1.lost_game = True
            else:
                self.player_2.lost_game = True

    def update(self):
        """
        Updates the win/lose arrays after a game of blackjack has gone to completion.

        Args:
            None

        Returns:
            None
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
            current_player = (2 if current_player == 1 else 1)

    def clear(self):
        """
        Resets the game state so another game can be played after one is done.

        Args:
            None

        Returns:
            None
        """

        self.player_1.clear()
        self.player_2.clear()
        self.game_over = False
        self.moves = []

    def run_simulation(self):
        """
        Runs a simulation of a given number of games so that the program can learn the best
        strategies of any given state via simulation.

        Args:
            None

        Returns:
            None
        """

        for game in xrange(self.n_games):
            self.play_game()
            self.update()
            if self.per_game_verbose:
                self.print_game_state()
            self.clear()
        return

    def _print_moves(self):
        """
        Prints the optimal number of cards to draw given
        state == [p1_score, p2_score, p2_drew_on_last_turn == True].

        Args:
            None

        Return:
            None
        """

        for i in xrange(self.l_target):
            out_str = ''
            for j in xrange(self.l_target):
                best_move = -1
                best_move_index = -1
                win_pointer = self.win_count[i][j][1]
                for k in xrange(len(win_pointer)):
                    if best_move <= win_pointer[k]:
                        best_move = win_pointer[k]
                        best_move_index = k
                out_str += ('%d ' % (best_move_index))
            print out_str

    def _print_prob(self):
        """
        Prints the probability of winning if the best move is played in
        state == [p1_score, p2_score, p2_drew_on_last_turn == True].

        Args:
            None

        Returns:
            None
        """

        for i in xrange(self.l_target):
            out_str = ''
            for j in xrange(self.l_target):
                best_move = -1
                best_move_index = -1
                denominator = 0.0
                win_pointer = self.win_count[i][j][1]
                lost_pointer = self.lose_count[i][j][1]
                for k in xrange(len(win_pointer)):
                    if best_move <= win_pointer[k]:
                        best_move = win_pointer[k]
                        best_move_index = k
                    denominator += (win_pointer[k] + lost_pointer[k])

                out_str += ('%.4f ' % (best_move / denominator if denominator > 0 else 0.5))
            print out_str

    def _print_win_array(self):
        """
        Prints the win_array for debugging purposes.
        """

        print "\nFinal Win Array"
        for i in xrange(self.l_target):
            out_str = ''
            for j in xrange(self.l_target):
                for k in xrange(self.k + 1):
                    out_str += ('%4d ' % self.win_count[i][j][1][k])
            print out_str

    def _print_lose_array(self):
        """
        Prints the lost_array for debugging purposes.
        """

        print "\nFinal Lose Array"
        for i in xrange(self.l_target):
            out_str = ''
            for j in xrange(self.l_target):
                for k in xrange(self.k + 1):
                    out_str += ('%4d ' % self.lose_count[i][j][1][k])
            print out_str

    def print_solution(self):
        """
        Prints the final solution to the programming assignment.
        """

        self._print_moves()
        print 
        self._print_prob()
        if self.verbose:
            self._print_win_array()
            self._print_lose_array()

    def print_game_state(self):
        """
        Prints the state of the game - for debugging purposes.  Prints after each game with the
        '-e' or '--extra_verbose' option.
        """

        loser = None
        winner = None
        if self.player_1.lost_game:
            loser = self.player_1
            winner = self.player_2
        else:
            loser = self.player_2
            winner = self.player_1

        print "Stats"
        print "-----"
        print ("Highest Card = %d, Lower Target = %d, Upper Target = %d, Number of Draws = %d"
               % (self.n, self.l_target, self.u_target, self.k))
        print "Winner = %d, Score = %d" % (winner.index, winner.score)
        print "Loser = %d, Score = %d" % (loser.index, loser.score)
        print ("Player 1, 2 Passed on Last Turn: (%s, %s)"
               % (str(self.player_1.stayed_last_turn()) , str(self.player_2.stayed_last_turn())))
        for move in self.moves:
            print move

        self._print_win_array()
        self._print_lose_array()
        print "Game Done\n"

def driver():
    """
    The driver program for this script.
    """

    # Deal with command line arguments
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
    parser.add_argument('-v', '--verbose', help='run with increased console ouptut',
                        action='store_true')
    parser.add_argument('-e', '--extra-verbose', help='runs per game console output',
                        action='store_true')
    args = parser.parse_args()

    # Object instantiation and simulation running.
    blackjack = Blackjack(args.N, args.LTarget, args.UTarget, args.K, args.M, args.N_Games,
                          args.verbose, args.extra_verbose)
    blackjack.run_simulation()
    blackjack.print_solution()

if __name__ == '__main__':
    driver()