from Program.player import Player
from Program.balls_keeper import BallKeeper


class MinMaxPlayerSimple(Player):

    def __init__(self, name, bag):
        Player.__init__(self, name, bag)
        self.known = {}
        self.counter = 0
        self.depth = 0
        self.move_complete = None
        self.list_of_moves = []
    """
    Method called by class Collecto.
    """
    def do_move(self, board):
        return self.calculate_next_move(board)
    """
    Returns a list of single valid moves, and double of not single available."""
    def calculate_next_move(self, current_board):
        self.counter = 0
        self.depth = 0
        # for every possible move, add a pair of a min_max score and the move to a list scores.
        single, double = current_board.check_if_valid_move(current_board.board)
        if single:
            #  print("singles in min max: ", single)
            return 1, single
        elif not single and double:

            return 2, double
        else:
            return 0, 0
