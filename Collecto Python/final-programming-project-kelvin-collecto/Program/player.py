import random as rnd
from Program.balls_keeper import BallKeeper

class Player:

    def __init__(self, name, bag):
        self.name = name
        self.bag = bag
        self.points = 0
        self.win = None

    def do_move(self, board):
        # TODO define how to move
        """
        int(input("Where do you want to place your move"))
        """
        rnd.seed()
        return int(rnd.random() * 49)

    def set_result(self):
        pass

    def get_name(self):
        return self.name

    def set_move(self, move):
        pass

    def check_points(self):
        # TODO count points
        counter = 0

    def update_points(self):
        # TODO udates points after each move
        self.points += 1