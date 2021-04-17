from Program.player import Player
from Program.balls_keeper import BallKeeper

THRESHOLD = 1


class MinMaxPlayer(Player):

    def __init__(self, name, bag):
        Player.__init__(self, name, bag)
        self.known = {}
        self.counter = 0
        self.depth = 0
        self.move_complete = None
        self.list_of_moves = []

    def do_move(self, board):
        return self.calculate_next_move(board)

    def calculate_next_move(self, current_board):
        self.counter = 0
        self.depth = 0
        # for every possible move, add a pair of a min_max score and the move to a list scores.
        score_move_pairs = []
        single, double = current_board.check_if_valid_move(current_board.board)

        if single:
            print("single length", len(single))
            for i, next_move in enumerate(single):
                self.counter = 0
                depth = 0
                next_score = self.min_max(current_board, next_move, depth)
                score_move_pairs.append((next_score, next_move))
            print("outside counter: " + str(self.counter))
            # print(self.known.keys())
            # if there is no score/move pair, return 0
            if not score_move_pairs:
                self.move_complete = False
                return []
            # otherwise
            else:
                # compute the max score/move
                print("score move pairs: ", score_move_pairs)
                highest_score, best_move = max(score_move_pairs)
                # return the move
                self.move_complete = True
                print("AI returns: ", max(score_move_pairs))
                move = max(score_move_pairs)
                return 1, [move[1]]
        elif not single and double:
            return 2, double
        else:
            return 0, 0

    """
    NORMAL MIN MAX
    """

    def min_max(self, current_board, move, depth):
        self.counter += 1
        board = current_board.deep_copy()
        if board.check_before_do_move(move):
            board.do_move(move)
        balls = board.get_adjacent_balls()
        if depth > THRESHOLD:
            # print("heurisic: ", len(balls))
            return len(balls)
        score = []
        single, double = current_board.check_if_valid_move(board.board)
        for moves in single:
            score.append(self.max_min(board, moves, depth + 1))
        if score:
            return max(score)
        return 0


    def max_min(self, current_board, move, depth):
        self.counter += 1
        board = current_board.deep_copy()
        if board.check_before_do_move(move):
            board.do_move(move)
        balls = board.get_adjacent_balls()
        # check is any other move possible
        if depth > THRESHOLD:
            # print("heuristic: ", len(balls))
            return len(balls)
        score = []
        single, double = current_board.check_if_valid_move(board.board)

        for moves in single:
            score.append(self.min_max(board, moves, depth + 1))

        if score:
            return min(score)
        return 0
