from Program.player import Player
from Program.camara import Camara
import concurrent.futures
import threading


class HumanPlayer(Player):

    def __init__(self, name, bag):
        Player.__init__(self, name, bag)
        self.next_move = []
        self.list_of_moves = []
        # initialize an Camara object and run it i a new Thread
        self.camara = Camara()
        x = threading.Thread(target=self.camara.get_gestures)
        x.start()
        self.pos = None
        self.dir = None
        self.current_move = None
        self.move_complete = None
        self.gesture = None
        self.gesture2 = None
        self.got_move = False

    """
    Does a move if the human player has clicked on a space and give a direction 
    or if the desires gestures has been given"""

    def do_move(self, board):
        # single = self.on_gesture_available(board)
        if self.move_complete:  # or single is True:
            self.move_complete = False
            self.gesture = None
            self.gesture2 = None
            self.camara.num = None
            self.camara.two = None
            num = 1
            if len(self.list_of_moves) > 1:
                num = 2
            return num, self.list_of_moves
        return 10, 10

    def set_move(self, pos, dir):
        move = (pos, dir)
        self.list_of_moves.append(move)

    def set_move_position(self, pos):
        self.pos = pos

    def set_move_direction(self, dir):
        self.dir = dir

    def on_gesture_available(self, board):
        single, double = board.check_if_valid_move(board.board)
        self.gesture = self.camara.get_num()
        self.gesture2 = self.camara.get_two()
        if self.gesture == 4 and self.got_move is False:  # 4 for thumb up
            if self.gesture2 == 10:  # 10 for ok
                if single:
                    # self.set_move(single[0][0], single[0][1])
                    self.got_move = True
                    return single
                elif double:
                    pass
