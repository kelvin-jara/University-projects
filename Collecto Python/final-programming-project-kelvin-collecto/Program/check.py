from Program.ball import Ball
from Program.helpers.constants import Constants
from Program.board import Board
from Program.space import Space
from Program.balls_keeper import BallKeeper
from Program.min_max_player import MinMaxPlayer



bag = BallKeeper()
board = Board()
min_max_player = MinMaxPlayer("Min Max", bag)
x, move = min_max_player.do_move(board)
print("type: ", x, "move: ", move)
board.do_move(move)
board.board_to_string()
print("balls :", len(board.get_adjacent_balls()))

"""

for i, spaces in enumerate(board.board):
    board.board[i] = Space()
# board.board_to_string()
ball1 = Ball(Constants.RED)
ball2 = Ball(Constants.WHITE)
ball3 = Ball(Constants.ORANGE)
ball4 = Ball(Constants.WHITE)

board.board[22] = ball1
board.board[5] = ball2
board.board[0] = ball3
board.board[7] = ball4

print("initial board")
board.board_to_string()

min_max_player = MinMaxPlayer("Min Max", bag)
# move = min_max_player.do_move(board)
move1 = (0, 3)
print("last move: ", move1)
print("Last print")
board.move_ball_to_empty(move1, board.board)
board.board_to_string()
"""









""""
def get_possible_moves(self):
    # TODO get rigth moves
    moves = []
    for i in range(len(self.board)):
        if self.board[i] == " ":
            moves.append(i)
    return moves


def move_is_legal(self, move):
    if self.check_move_in_board(move[0]):
        if self.check_direction_in_board():
            return True
    return False


def check_move_in_board(self, move):
    try:
        move = int(move)
        if not (-1 < move < 49):
            raise ValueError
    except:
        return False
    return True


def check_single_move(self):
    # TODO checks if there is single move
    single_move = False
    return single_move


def check_double_move(self):
    # TODO checks if there is double move
    double_move = False
    return double_move
"""

"""
THIS CODE IS GOOD FOR CHECKING IF BOARD IS VALID
    def get_possible_moves(self, board):
        # make a tuple list for moves
        moves = []
        # check if each ball has balls in the surroundings
        index = 0
        for ball_or_space in board:
            directions = Constants.DIRECTIONS
            for direction in directions:
                if directions == 0:  # check up
                    if index - 7 > 0 and ball_or_space.color == board[index - 7].color:
                        move = (index, direction)
                        moves.append(move)
                elif direction == 1:  # check right

                    if index + 1 < len(self.board) and ball_or_space.color == board[index + 1].color:
                        move = (index, direction)
                        moves.append(move)

                elif direction == 2:  # check down
                    if index + 7 < len(self.board) and board[index + 7].color == ball_or_space.color:
                        move = (index, direction)
                        moves.append(move)

                elif direction == 3:  # check left
                    if index - 1 > 0 and ball_or_space.color == board[index - 1].color:
                        move = (index, direction)
                        moves.append(move)
            index += 1

        return moves
"""