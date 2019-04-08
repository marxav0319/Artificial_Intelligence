"""
"""

class Blackjack:

    def __init__(self, n_cards, l_target, u_target):
        """
        """

        self.n_cards = n_cards
        self.l_target = l_target
        self.u_target = u_target
        self.cards = range(1, n_cards + 1)
        self.play = [[0 for i in xrange(l_target)] for j in xrange(l_target)]
        self.prob = [[0 for i in xrange(l_target)] for j in xrange(l_target)]

        self.fill_moves()

    def compute_probability(self, p1_score, p2_score):
        """
        """

        prob_p1_wins = 0.0
        prob_p2_wins = 0.0
        for card in self.cards:
            if p1_score + card > self.u_target:
                prob_p2_wins = 1.0
            elif p1_score + card >= self.l_target:
                prob_p2_wins = 0.0
            else:
                prob_p2_wins = self.prob[p2_score][p1_score + card]
            prob_p1_wins = prob_p1_wins + (1 - prob_p2_wins) / self.n_cards

        return prob_p1_wins

    def compute_move(self, p1_score, p2_score):
    """
    """

    if p1_score < p2_score:
        self.play[p1_score][p2_score] = True
        self.prob[p1_score][p2_score] = self.compute_probability()
    else:
        p1_wins_drawing = self.compute_probability()
        p2_wins_staying = 1 - p1_wins_prob

        if p1_wins_drawing > p1_wins_staying:
            self.play[p1_score][p2_score] = True
            self.prob[p1_score][p2_score] = p1_wins_drawing
        else:
            self.play[p1_score][p2_score] = False
            self.prob[p1_score][p2_score] = p1_wins_staying

    return

    def fill_moves(self):
        """
        """

        for i in xrange(self.l_target * 2, -1, -1):
            outstr = ''
            start_col = max(0, i - self.l_target)
            count = min(i, self.l_target - start_col, self.l_target)
            for j in xrange(0, count):
                p1_score = start_col + j
                p2_score = min(self.l_target, i) - j - 1
                self.compute_move(p1_score, p2_score)
                # outstr += '(%d, %d) ' % (p1_score, p2_score)
            print outstr + '\n'

    def __str__(self):
        """
        """

        return ''

def main():
    """
    """

    blackjack = Blackjack(10, 21, 25)
    # for row in blackjack.play:
    #     print row


if __name__ == '__main__':
    main()