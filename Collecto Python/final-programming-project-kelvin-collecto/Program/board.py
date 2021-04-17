import math
import copy
import random
from Program.ball import Ball
from Program.helpers.constants import Constants
from Program.space import Space

'''
  -   -   - 
| 0  | 1  | 2  | 3  | 4  | 5  | 6  |
  -   -   -
| 7  | 8  | 9 | 10 | 11 | 12 | 13 |
  -   -   -
| 14 | 15 | 16 | 17 | 18 | 19 | 20 |
  -   -   -
| 21 | 22 | 23 | 24 | 25 | 26 | 27 |
  -   -   -
| 28 | 29 | 30 | 31 | 32 | 33 | 34 |
  -   -   -
| 35 | 36 | 37 | 38 | 89 | 40 | 41 |
  -   -   -
| 42 | 43 | 44 | 45 | 46 | 47 | 48 |
'''

class Board:

    def __init__(self):
        self.balls = []
        self.final_balls = []
        self.board = [Space()] * 25
        # 25, 49, 121, 168
        self.row_length = int(math.sqrt(len(self.board)))
        self.extra = self.row_length/2 + 1
        print("Extra is :", int(self.extra), "row length: ", self.row_length, "board length: ", len(self.board))
        # make board with balls
        self.create_legal_valid_board()

    """"Move balls in game, move is tuple like: move = (index, direction, single or double), 
    index = 1..48, direction =[up, right, down, left], single/double = 1/2"""
    def move_neighbor_balls(self, move, board):
        neighbor_index = self.get_neighbors_in_desired_direction(move)
        # raw_of_current_ball_to_move = self.get_current_column(move[0])
        last_neighbor_index = 0
        while True:  # while there is a neighbor in the desired direction
            if neighbor_index == last_neighbor_index:
                break
            if neighbor_index > len(board) - 1 or neighbor_index < 0:
                break
            neighbor_move = (neighbor_index, move[1])
            last_neighbor_index = neighbor_index
            self.move_ball_to_empty(neighbor_move, board)
            neighbor_index = self.get_neighbors_in_desired_direction(neighbor_move)
            # print(neighbor_move)

    """
    Used to get all index of neighbors in the direction specified by the move "move = (index, direction)". 
    """
    def get_neighbors_in_desired_direction(self, move):
        index = move[0]
        raw_of_current_ball_to_move = self.get_current_column(move[0])
        if move[1] == 0:
            index = move[0] + self.row_length
        elif move[1] == 1:  # right
            index_before = move[0] - 1
            if index_before in raw_of_current_ball_to_move :
                index = move[0] - 1
        elif move[1] == 2:  # down
            index = move[0] - self.row_length
        elif move[1] == 3:  # left
            index_before = move[0] + 1
            if index_before in raw_of_current_ball_to_move:
                index = index_before
        return index
    """
    Given a index it returns a list of the neighbors in the same column.
    """
    def get_current_column(self, position):
        list_index_of_raw = []

        i = 1
        while True and (position + i) < len(self.board):  # to the right of index
            if ((position + i) % self.row_length) == 0:
                break
            list_index_of_raw.append(position + i)
            i += 1
        i = 1
        while True and (position - i) > 0:  # to the left of index
            list_index_of_raw.append(position-i)
            if (position - i) % self.row_length == 0:
                break
            i += 1
        list_index_of_raw.append(position)
        return list_index_of_raw
    """
    Given an index and direction, this method moves the object in the index to the furthest empty space in the desires 
    direction.
    """
    def move_ball_to_empty(self, move, board):  # move any ball in a desired direction to empty space
        new_index = self.get_index_in_direction(move, board)
        if new_index != move[0]:
            board[new_index] = board[move[0]]
            board[move[0]] = Space()
    """
    Gives index of the further empty space in the direction specified in the move.
    """
    def get_index_in_direction(self, move, board):
        index = move[0]
        raw_of_current_ball_to_move = self.get_current_column(move[0])  # list of indices in the same column.
        if move[1] == 0:  # up
            x = 1
            while True:
                if move[0]-self.row_length*x >= 0 and board[move[0]-self.row_length*x].color == Constants.EMPTY:
                    index = move[0] - self.row_length*x
                    x += 1
                else:
                    break
        elif move[1] == 1:  # right
            x = 1
            while True:
                if move[0] + x < len(board) and board[move[0] + x].color == Constants.EMPTY:
                    sure = move[0] + x
                    if sure in raw_of_current_ball_to_move:
                        index = sure
                    x += 1
                else:
                    break
        elif move[1] == 2:  # down
            x = 1
            while True:
                if move[0] + self.row_length*x < len(board) and board[move[0] + self.row_length*x].color == Constants.EMPTY:
                    index = move[0] + self.row_length*x
                    x += 1
                else:
                    break
        elif move[1] == 3:  # left
            x = 1
            while True:
                if move[0] - x >= 0 and board[move[0] - x].color == Constants.EMPTY:
                    sure = move[0] - x
                    if sure in raw_of_current_ball_to_move:
                        index = sure
                    x += 1
                else:
                    break
        return index
    """
    Before doing a move with method do_move(), the move is first checked here.
    The method return True if the move is in a list valid moves and False otherwise.
    This method uses the board of this class ( self.board) to find the valid moves.
    """
    def check_before_do_move(self, *args):
        if len(args) == 1:
            move = (args[0][0], args[0][1], 1)
        else:
            move = [(args[0][0], args[0][1], 1), (args[1][0], args[1][1], 2)]
        single, double = self.check_if_valid_move(self.board)
        if len(args) == 1:
            if move in single:
                return True
        elif len(args) == 2:
            if move in double:
                return True
        return False
    """
    This method is used by the class Collecto to make changes in the board given one or two moves.
    """
    def do_move(self, *args):
        if len(args) == 1:
            move = (args[0][0], args[0][1], 1)
        else:
            move = [(args[0][0], args[0][1], 1), (args[1][0], args[1][1], 2)]
            move2 = (args[1][0], args[1][1], 2)
        # get list of single and double moves
        single, double = self.check_if_valid_move(self.board)
        # print("\n", "single: ", single, "double: ", double, "move :", move)
        # check if move is in single move list or in double mov list or if the list are empty

        # if move is single move
        if len(args) == 1:
            if move in single:
                self.move_ball_to_empty(move, self.board)  # first move the desired ball
                self.move_neighbor_balls(move, self.board)  # move the neighbors
                # get index of balls with adjacent balls
                # put the balls in a list
        # elif double move is the list of double move
        elif len(args) == 2:
            if move in double:
            # do first move
                self.move_ball_to_empty(move[0], self.board)
                self.move_neighbor_balls(move[0], self.board)
            # do second move
                self.move_ball_to_empty(move[1], self.board)
                self.move_neighbor_balls(move[1], self.board)
            #   put the balls in a list and change the object from ball to space

    """
    This method is used to check a move before it is made, this method is almost the same as,
    check before do move(), the difference is that this method can be outside this class, 
    a move and a board s given as arguments, which means this method does not use the board of this class."""
    def check_before_do_move_outside(self, *args, board):

        if len(args) == 1:
            move = (args[0][0], args[0][1], 1)
        else:
            move = [(args[0][0], args[0][1], 1), (args[1][0], args[1][1], 2)]
        single, double = self.check_if_valid_move(board)
        if len(args) == 1:
            if move in single:
                return True
        elif len(args) == 2:
            if move in double:
                return True
        return False
    """
    Similar with do_move(), makes a move but it is given a board as argument, this board can be specdified outside 
    this class, but the advantage is that it uses some of the methods defined here."""
    def do_move_outside(self, *args, board):
        if len(args) == 1:
            move = (args[0][0], args[0][1], 1)
        else:
            move = [(args[0][0], args[0][1], 1), (args[1][0], args[1][1], 2)]
            move2 = (args[1][0], args[1][1], 2)
        # get list of single and double moves
        single, double = self.check_if_valid_move(board)
        # print("\n", "single: ", single, "double: ", double, "move :", move)
        # check if move is in single move list or in double mov list or if the list are empty

        # if move is single move
        if len(args) == 1:
            if move in single:
                self.move_ball_to_empty(move, board)  # first move the desired ball
                self.move_neighbor_balls(move, board)  # move the neighbors
                # get index of balls with adjacent balls
                # put the balls in a list
        # elif double move is the list of double move
        elif len(args) == 2:
            if move in double:
            # do first move
                self.move_ball_to_empty(move[0], board)
                self.move_neighbor_balls(move[0], board)
            # do second move
                self.move_ball_to_empty(move[1], board)
                self.move_neighbor_balls(move[1], board)
            #   put the balls in a list and change the object from ball to space

    """
    This method returns a list of balls that have neighbors with similar color, this checks the boad: self.board.
    """
    def get_adjacent_balls(self):
        list_of_balls = []
        indexes = []
        for i, ball_or_space in enumerate(self.board):
            move = (i, None)
            if self.check_if_ball_has_adjacents(move, self.board):
                list_of_balls.append(ball_or_space)
                indexes.append(i)

        for i in indexes:
            self.board[i] = Space()
        return list_of_balls

    """
    This method returns a list of balls that have neighbors with similar color, this checks a board given as 
    argument then this method can be used outside this class.
    """
    def get_adjacent_balls_outside(self, board):
        list_of_balls = []
        indexes = []
        for i, ball_or_space in enumerate(board):
            move = (i, None)
            if self.check_if_ball_has_adjacents(move, board):
                list_of_balls.append(ball_or_space)
                indexes.append(i)

        for i in indexes:
            board[i] = Space()
        return list_of_balls

    def do_move_inside(self, move, board):
        self.move_ball_to_empty(move, board)  # first move the desired ball
        self.move_neighbor_balls(move, board)  # move the neighbors
    """
    Returns a list with valid moves given a board of type list.
    """
    def check_if_valid_move(self, board):
        # make a list for single and double
        single_moves = []
        double_moves = []
        moves = self.get_possible_moves(board)
        for i, move in enumerate(moves):
            board_copy1 = self.copy_of_board(board)
            self.do_move_inside(move, board_copy1)
            if self.check_if_board_has_adjacents(board_copy1):
                new_move = (move[0], move[1], Constants.SINGLE)
                single_moves.append(new_move)
                moves2 = self.get_possible_moves(board_copy1)
                for move2 in moves2:
                    board_copy2 = self.copy_of_board(board_copy1)
                    self.do_move_inside(move2, board_copy2)
                    # index = (self.get_index_in_direction(move2, board_copy2), board_copy2)
                    #if move != move2:
                        # if self.check_if_ball_has_adjacents(index, board_copy2):
                    if self.check_if_board_has_adjacents(board_copy2):
                        new_move = [(move[0], move[1], Constants.SINGLE), (move2[0], move2[1], Constants.DOUBLE)]
                        double_moves.append(new_move)
                    #elif move == move2:
                    #    print("Never really expected first ")
                    #    pass
            elif not self.check_if_board_has_adjacents(board_copy1):
                moves2 = self.get_possible_moves(board_copy1)
                for move2 in moves2:
                    board_copy2 = self.copy_of_board(board_copy1)
                    self.do_move_inside(move2, board_copy2)
                    # index = (self.get_index_in_direction(move2, board_copy2), board_copy2)

                    # if self.check_if_ball_has_adjacents(index, board_copy2):
                    if self.check_if_board_has_adjacents(board_copy2):
                        new_move = [(move[0], move[1], Constants.SINGLE), (move2[0], move2[1], Constants.DOUBLE)]
                        double_moves.append(new_move)
        return single_moves, double_moves
    """
    Given a move and a board it checks if the board has balls with similar color.
    """
    def check_if_ball_has_adjacents(self, move, board):
        # check if the ball with the index and its surroundings are the same
        # if move[1] == 0:  # up
        raw_of_current_ball_to_move = self.get_current_column(move[0])
        if isinstance(board[move[0]], Ball):
            if move[0] - self.row_length >= 0 and board[move[0] - self.row_length].color == board[move[0]].color:
                return True
            # elif move[1] == 1:  # right
            elif move[0] + 1 < len(board) and board[move[0] + 1].color == board[move[0]].color:
                index = move[0] + 1
                if index in raw_of_current_ball_to_move:
                    return True
            # elif move[1] == 2:  # down
            elif move[0] + self.row_length < len(board) and board[move[0] + self.row_length].color == board[move[0]].color:
                return True
            # elif move[1] == 3:  # left
            elif move[0] - 1 >= 0 and board[move[0] - 1].color == board[move[0]].color:
                index = move[0] - 1
                if index in raw_of_current_ball_to_move:
                    return True
        #   check is ball is in list of balls
        # return true if a similar ball is found in a specified direction
        # otherwise return False
        return False
    """
    Checks if a board given as argument has balls with similar neighbors.
    Returns True is there are and False otherwise.
    """
    def check_if_board_has_adjacents(self, board):
        for i, ball_or_space in enumerate(board):
            move = (i, None)
            if self.check_if_ball_has_adjacents(move, board):
                return True
        return False



    def get_possible_moves(self, board):
        # make a tuple list for moves
        moves = []
        # check if each ball has balls in the surroundings
        index = 0
        for ball_or_space in board:
            if not isinstance(ball_or_space, Space):
                directions = Constants.DIRECTIONS
                for direction in directions:
                    if direction == 0:  # check up
                        if index - self.row_length >= 0 and board[index - self.row_length].color == Constants.EMPTY:
                            move = (index, direction)
                            moves.append(move)
                    elif direction == 1:  # check right
                        if index + 1 < len(board) and board[index + 1].color == Constants.EMPTY:
                            move = (index, direction)
                            moves.append(move)

                    elif direction == 2:  # check down
                        if index + self.row_length < len(board) and board[index + self.row_length].color == Constants.EMPTY:
                            move = (index, direction)
                            moves.append(move)

                    elif direction == 3:  # check left
                        if index - 1 >= 0 and board[index - 1].color == Constants.EMPTY:
                            move = (index, direction)
                            moves.append(move)
            index += 1
        return moves

    """
    Returns true is there there is not emtpy spaces in the board.
    """
    # TODO check is method is neccesary.
    def checks_if_board_empty(self):
        for ball_or_space in self.board:
            if ball_or_space == Space():
                return False
        return True
    """
    return true there are move possible using the board: self.board
    """
    def check_if_any_moves_possible(self):
        single, double = self.check_if_valid_move(self.board)
        if not single and not double:
            return False
        return True
    """
    This method checks is there are moves available in a board given as argument.
    """
    def check_if_any_moves_possible_ouside(self, board):
        single, double = self.check_if_valid_move(board)
        if not (single and double):
            return False
        return True
    """
    Checks if the given index is inside the board.
    """
    def check_index_in_board(self, index):
        if index > len(self.board) or index < len(self.board):
            return False
        return True

    """
    Makes a list of balls with 6 different colors.
    """
    def make_balls(self):
        for i in range(0, int((len(self.board) - 1) / 6)):  # self.row_length + 1

            for color in Constants.COLORS:
                self.balls.append(Ball(color))
    """
    This method populates a board of type list.
    """
    def create_board(self):
        self.board = [Space()] * self.row_length*self.row_length
        self.balls.clear()
        self.make_balls()
        random.shuffle(self.balls)
        for i in range(0, len(self.board)):
            counter = 0
            while True:
                try:
                    if self.balls[counter].color != self.board[i - 1].color and self.balls[counter].color != self.board[i - self.row_length].color:
                        break
                    elif self.balls[counter].color != self.board[i - 1].color and i > self.row_length*self.row_length - self.extra:
                        break
                except IndexError as i:
                    z = i
                    break
                counter += 1
            if self.balls:
                try:
                    ball = self.balls.pop(counter)
                except IndexError as e:
                    ball = self.balls.pop(counter-1)
                    i = len(self.board)-2
                self.final_balls.append(ball)
                if i != (self.row_length*self.row_length - 1)/2:
                    self.board[i] = ball
                elif i == (self.row_length*self.row_length - 1)/2:
                    self.board[len(self.board)-1] = ball
    """
    This method makes a valid board at the beginning of the game.
    """
    def create_legal_valid_board(self):
        counter = 0
        while not self.check_valid_board():
            self.create_board()
            counter += 1
            print(counter)
            if counter > 100:
                break
    """
    Check is the initial board has not neighbors with the same color.
    This is one of the rules of the game.
    """
    def check_valid_board(self):
        board = self.board
        for i in range(0, len(self.board)):
            try:
                if board[i] == board[i + 1]:
                    return False
                elif board[i] == board[i - 1]:
                    return False
                elif board[i] == board[i + self.row_length]:
                    return False
                elif board[i] == board[i - 1]:
                    return False
            except IndexError as e:
                z = e
        return True

    def get_board(self):
        return self.board
    """
    This method is to make a string representation of the board.
    The method is used outside this class.
    """
    def board_to_string(self):
        field = self.get_board()
        print("\n---------------------------")
        for i in range(0, len(field)):
            if i % self.row_length == 0:
                print(" ")
            if self.board[i].color == " ":
                print("|" + " " + "|", end='')
            else:
                print("|" + field[i].color + "|", end='')
        print("\n")
    """
    Method to make a string representation of the board. 
    This method can be used internally.
    """
    def board_to_string_inside(self, board):
        field = board
        print("\n---------------------------")
        for i in range(0, len(field)):
            if i % self.row_length == 0:
                print(" ")
            if board[i].color == " ":
                print("|" + " " + "|", end='')
            else:
                print("|" + field[i].color + "|", end='')
        print("\n")
    """
    Check is the board is empty.
    """
    def board_empty(self):
        for i in range(0, len(self.board)):
            if self.board[i] != " ":
                return False
        return True
    """
    Makes a copy the the board of type list.
    Given as argument a board.
    """
    def copy_of_board(self, board):
        return copy.copy(board)
    """
    Makes a coy of the the class.
    """
    def deep_copy(self):
        return copy.deepcopy(self)

"""
board = Board()
board.board_to_string()
"""