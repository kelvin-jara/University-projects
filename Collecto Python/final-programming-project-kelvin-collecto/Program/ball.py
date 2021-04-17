from Program.helpers.constants import Constants
class Ball:
    def __init__(self, color):
        self.color = color
        self.neighbors = []
        self.diameter = Constants.DIAMETER
        self.position = 0

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors

