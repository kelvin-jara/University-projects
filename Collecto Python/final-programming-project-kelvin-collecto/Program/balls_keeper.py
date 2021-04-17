from Program.helpers.constants import Constants

class BallKeeper:
    def __init__(self):
        self.balls = []
        self.num_of_balls = len(self.balls)
        self.white_balls = []
        self.red_balls = []
        self.blue_balls = []
        self.yellow_balls = []
        self.orange_balls = []
        self.purple_balls = []
        self.points = 0
        self.counted = False

    def add_balls_with_list(self, list_of_balls_to_add):
        for ball in list_of_balls_to_add:
            self.balls.append(ball)

    def classify_balls(self):
        for ball in self.balls:
            if ball.color == Constants.WHITE:
                self.white_balls.append(ball)
            elif ball.color == Constants.RED:
                self.red_balls.append(ball)
            elif ball.color == Constants.BLUE:
                self.blue_balls.append(ball)
            elif ball.color == Constants.YELLOW:
                self.yellow_balls.append(ball)
            elif ball.color == Constants.ORANGE:
                self.orange_balls.append(ball)
            elif ball.color == Constants.PURPLE:
                self.purple_balls.append(ball)

    def count_points(self):
        if not self.counted:
            self.counted = True
            self.classify_balls()
            if len(self.balls) >= 14:
                self.points += int(len(self.white_balls)/3)
                self.points += int(len(self.red_balls) / 3)
                self.points += int(len(self.blue_balls) / 3)
                self.points += int(len(self.yellow_balls) / 3)
                self.points += int(len(self.orange_balls) / 3)
                self.points += int(len(self.purple_balls) / 3)
            return self.points
        else:
            pass

