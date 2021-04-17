import random
from Program.board import Board
from Program.min_max_player import MinMaxPlayer
from Program.balls_keeper import BallKeeper
from Program.human_player import HumanPlayer
from Program.min_max_player_simple import MinMaxPlayerSimple


class Collecto:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        # self.current_player = random.randrange(0, len(self.players))
        self.current_player = 0
        # just for testing
        self.game_view = None
        self.double = None
        self.move_complete = False
        self.game_ended_bool = False
        self.counted = False
        print("Player", self.players[self.current_player].get_name(), "starts")

    def do_move(self):
        x, move = self.players[self.current_player].do_move(self.board)
        if x == 0 and move == 0 or self.game_ended():
            self.game_ended_bool = True
            return 100
        if isinstance(self.players[self.current_player], HumanPlayer):
            if self.players[self.current_player].got_move:
                self.move_complete = True
                self.players[self.current_player].got_move = False
            pass
        if x == 10 and move == 10:
            self.move_complete = False

        if (isinstance(self.players[self.current_player], MinMaxPlayer) or isinstance(self.players[self.current_player]
                , MinMaxPlayerSimple)) and len(move) > 0:
            self.move_complete = True

        if self.game_view.button_clicked or x == 2:
            self.double = True
        elif not self.game_view.button_clicked:
            self.double = False

        if not move:
            return False

        if self.move_complete and not self.game_ended():
            if not self.double:
                if self.board.check_before_do_move(move[0]):
                    self.board.do_move(move[0])
                    balls = self.board.get_adjacent_balls()
                    self.players[self.current_player].bag.add_balls_with_list(balls)
                    # print(self.players[self.current_player].bag.balls)
                    self.players[self.current_player].list_of_moves.clear()
                    self.players[self.current_player].move_complete = False
                    self.move_complete = False
                    self.change_player()
                elif not self.board.check_before_do_move(move[0]):
                    self.players[self.current_player].move_complete = True
                    self.players[self.current_player].list_of_moves.clear()
            elif self.double:
                if isinstance(self.players[self.current_player], MinMaxPlayer) or isinstance(
                        self.players[self.current_player], MinMaxPlayerSimple):
                    move1 = move[0][0]
                    move2 = move[0][1]
                elif isinstance(self.players[self.current_player], HumanPlayer):
                    move1 = move[0]
                    move2 = move[1]
                if self.board.check_before_do_move(move1, move2):
                    self.board.do_move(move1, move2)
                    balls = self.board.get_adjacent_balls()
                    self.players[self.current_player].bag.add_balls_with_list(balls)
                    self.players[self.current_player].list_of_moves.clear()
                    self.move_complete = False
                    self.change_player()
                    self.game_view.button_clicked = False
                elif not self.board.check_before_do_move(move[0], move[1]):
                    self.players[self.current_player].move_complete = True
                    self.players[self.current_player].list_of_moves.clear()
                # return
        elif self.game_ended():
            print("game ended")

    def get_points_and_winner(self):
        if not self.counted:
            self.counted = True
            points = []
            for player in self.players:
                points.append(player.bag.count_points())
            if points[0] > points[1]:
                self.players[0].win = True
                self.players[1].win = False
                return self.players[0].name, points[0]
            elif points[1] > points[0]:
                self.players[1].win = True
                self.players[0].win = False
                return self.players[1].name, points[1]
            elif points[1] == points[0]:
                self.players[1].win = True
                self.players[0].win = False
                return "No one ", points[1]
            return False, False
        else:
            pass

    def change_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def board_empty(self):
        return self.board.checks_if_board_empty()

    def reset(self):
        self.board = Board()
        self.game_view = None
        self.current_player = random.randrange(0, len(self.players))
        self.double = None
        self.move_complete = False
        self.game_ended_bool = False
        self.counted = False

    def get_board(self):
        return self.board.get_board()

    def row_length(self):
        return self.board.row_length

    def get_current_player(self):
        return self.current_player

    """
    Returns True if the game is over.
    """

    def game_ended(self):
        return not self.board.checks_if_board_empty() or not self.board.check_if_any_moves_possible()
