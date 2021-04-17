from pygame import draw
from pygame import key
from pygame import font
from Program.human_player import HumanPlayer

from Program.helpers.constants import Constants


class GameView:

    def __init__(self, game, screen, font1):
        self.game = game
        self.row_length = self.game.board.row_length
        self.screen = screen
        screen_size = self.screen.get_size()
        self.offset = [(Constants.WINDOW_WIDTH - Constants.BOARD_SIZE) / 2,
                       0.1875 * Constants.WINDOW_HEIGHT]  # Offset to draw the board.
        grid_x = Constants.BOARD_SIZE / self.row_length
        grid_y = Constants.BOARD_SIZE / self.row_length
        self.grid_size = [grid_x, grid_y]
        self.font = font1
        self.line_width = 10
        self.button_clicked = False  # to make double moves
        self.index_space = None  # index of space selected for move
        self.space_selected = None  # if space any space is selected then it is possible to get direction.
        self.counter = 0
        self.counted = False
        self.name = None  # name of the winner, used to print text on screen.
        self.points = None  # number of point the winner has obtained.
        self.new_game = False  # to see is user want a new game
        self.size_balls = Constants.DIAMETER

    """
    Method that the main class calls to draw the entire game
    """

    def draw_game(self):
        self.draw_board()
        self.draw_status_text()
        self.draw_button()
        self.draw_ball_keeper_right()
        self.draw_ball_keeper_left()

    def resize(self):
        pass

    """
    Draws the grid for the board, if human player selects a grid it changes color.
    """

    def draw_board(self):
        if isinstance(self.game.players[self.game.current_player], HumanPlayer):
            moves = self.game.players[self.game.current_player].on_gesture_available(self.game.board)
            if moves:
                self.game.players[self.game.current_player].gesture = None
                self.game.players[self.game.current_player].gesture2 = None
                self.game.players[self.game.current_player].camara.num = None
                self.game.players[self.game.current_player].camara.two = None
                print("the moves for suggestion: ", moves)
                for move, i in enumerate(moves):
                    print(moves[move][0])

        for i, ball_or_space in enumerate(self.game.get_board()):
            x = int(i % self.row_length) * self.grid_size[0] + self.offset[0]
            y = int(i / self.row_length) * self.grid_size[1] + self.offset[1]
            if self.index_space is not None and i == self.index_space:
                color = (250, 0, 0)
            else:
                color = (0, 0, 0)
            draw.rect(self.screen, color, ((x, y), self.grid_size), int(self.line_width / 3))
            self.draw_balls(x, y, self.grid_size[0], ball_or_space)

    """
    Draws the square where the balls each player has obtained during the game on the right side of screen
    """
    def draw_ball_keeper_right(self):
        keeper_x = Constants.WINDOW_WIDTH * 0.2
        keeper_y = Constants.BOARD_SIZE * 1.1
        keeper_size = [keeper_x, keeper_y]
        x = Constants.WINDOW_WIDTH * 0.025 + Constants.WINDOW_WIDTH * 0.75
        y = Constants.WINDOW_HEIGHT * 0.5625 - keeper_y / 2
        if self.game.players[self.game.current_player].name == self.game.players[1].name:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        if self.game.game_ended_bool:
            color = (0, 0, 0)
        draw.rect(self.screen, color, ((x, y), keeper_size), int(self.line_width / 2))
        for i, ball in enumerate(self.game.players[1].bag.balls):
            x_ball = int(i % self.size_balls) * keeper_x / self.size_balls + x
            y_ball = int(i / self.size_balls) * keeper_x / self.size_balls + y
            self.draw_balls(x_ball, y_ball, keeper_x / self.size_balls, ball)
        font1 = font.SysFont(font.get_fonts()[0], int(keeper_x * 0.2))
        text = font1.render(self.game.players[1].name, True, (0, 0, 0))
        self.screen.blit(text, (x + 0.005 * x, y - y * 0.7))

    """
    Draws the square where the balls each player has obtained during the game on the left side of screen
    """
    def draw_ball_keeper_left(self):
        keeper_x = Constants.WINDOW_WIDTH * 0.2
        keeper_y = Constants.BOARD_SIZE * 1.1
        keeper_size = [keeper_x, keeper_y]
        x = Constants.WINDOW_WIDTH * 0.025
        y = Constants.WINDOW_HEIGHT * 0.5625 - keeper_y / 2
        if self.game.players[self.game.current_player].name == self.game.players[0].name:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        if self.game.game_ended_bool:
            color = (0, 0, 0)
        draw.rect(self.screen, color, ((x, y), keeper_size), int(self.line_width / 2))
        for i, ball in enumerate(self.game.players[0].bag.balls):
            x_ball = int(i % self.size_balls) * keeper_x / self.size_balls + x
            y_ball = int(i / self.size_balls) * keeper_x / self.size_balls + y
            self.draw_balls(x_ball, y_ball, keeper_x / self.size_balls, ball)
        font1 = font.SysFont(font.get_fonts()[0], int(keeper_x * 0.2))
        text = font1.render(self.game.players[0].name, True, (0, 0, 0))
        self.screen.blit(text, (x + 0.005 * x, y - y * 0.7))

    """
    Draws the balls on the board
    """

    def draw_balls(self, x, y, size, ball):
        if ball.color == Constants.BLUE:
            color = (0, 0, 255)
        elif ball.color == Constants.YELLOW:
            color = (255, 255, 0)
        elif ball.color == Constants.RED:
            color = (255, 0, 0)
        elif ball.color == Constants.ORANGE:
            color = (255, 127, 0)
        elif ball.color == Constants.PURPLE:
            color = (127, 0, 127)
        elif ball.color == Constants.WHITE:  # this is actually green
            color = (0, 255, 0)
        elif ball.color == Constants.EMPTY:
            color = (255, 255, 255)
        radius = int(size / 2)
        draw.circle(self.screen, color, [int(x + radius), int(y + radius)], radius, self.line_width * 0)

    """
    Draws the button Double Move for the human player
    """

    def draw_button(self):
        button_x = self.grid_size[0] * 3
        button_y = self.grid_size[0] / 2
        button_size = [button_x, button_y]
        x = Constants.WINDOW_WIDTH / 2 - button_x / 2
        y = Constants.WINDOW_HEIGHT - 0.03125 * Constants.WINDOW_HEIGHT - button_y / 2
        if self.button_clicked:
            draw.rect(self.screen, (255, 0, 0), ((x, y), button_size), int(self.line_width / 3))
        else:
            draw.rect(self.screen, (0, 0, 0), ((x, y), button_size), int(self.line_width / 3))
        font1 = font.SysFont(font.get_fonts()[0], int(button_y * 0.7))
        if self.game.game_ended_bool:
            text = font1.render("NEW GAME", True, (0, 0, 0))
            self.screen.blit(text, (x + 0.15 * x, y))
            if self.button_clicked:
                self.new_game = True
        else:
            text = font1.render("MAKE DOUBLE MOVE", True, (0, 0, 0))
            self.screen.blit(text, (x + 0.005 * x, y))

    """
    If game has finalized it shows the winner and the points he has gotten.
    """

    def draw_status_text(self):
        if not self.game.game_ended_bool:
            text = self.font.render(self.game.players[self.game.current_player].name + "'s turn", True, (0, 0, 0))
            self.screen.blit(text, (self.offset[0], self.offset[1]/5))
        elif self.game.game_ended_bool:
            if not self.counted:
                self.counted = True
                name, points = self.game.get_points_and_winner()
                self.name = name
                self.points = points
            text = self.font.render(self.name + " WON with `" + str(self.points) + " points", True, (0, 0, 0))
            self.screen.blit(text, (self.offset[0], self.offset[1] / 5))

    def on_mouse_clicked(self, pos):
        x_new = int((pos[0] - self.offset[0]) / self.grid_size[0])
        y_new = int((pos[1] - self.offset[1]) / self.grid_size[1])
        button_x = self.grid_size[0] * 3
        button_y = self.grid_size[0] / 2
        button_size = [button_x, button_y]
        x = Constants.WINDOW_WIDTH / 2 - button_x / 2
        y = Constants.WINDOW_HEIGHT - 0.03125 * Constants.WINDOW_HEIGHT - button_y / 2
        # print(x, pos[0], x + button_x, y, pos[1], y + button_y, y < pos[1] < y + button_y, x < pos[0] < x + button_x)
        if -1 < x_new < self.game.row_length():
            if -1 < y_new < self.game.row_length():
                if self.space_selected:
                    self.index_space = None
                    self.space_selected = False
                elif not self.space_selected or self.space_selected is None:
                    self.index_space = x_new + self.row_length * y_new
                    self.space_selected = True
        # make a button and change color when pressed and activate set double move
        if x < pos[0] < x + button_x:  # 717 < pos[0] < 717 + 50:
            if y < pos[1] < y + button_y:  # 391 < pos[1] < 391 + 20:
                if self.button_clicked:

                    self.button_clicked = False
                    #  print("Enter single move")
                elif not self.button_clicked or self.button_clicked is None:
                    self.button_clicked = True
                    self.game.move_complete = False

                    #  print("Please make two moves")

    """
    'on_keys_pressed()' handles the keyboard's input from user.
    It makes the move for the human player.
    Requires a space is selected in the ball.
    """

    def on_keys_pressed(self, input_keys):
        # if space is selected then a move is possible
        if self.space_selected:
            if not self.button_clicked:
                if Constants.K_UP in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.UP)
                elif Constants.K_DOWN in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.DOWN)
                elif Constants.K_LEFT in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.LEFT)
                elif Constants.K_RIGHT in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.RIGHT)
                self.space_selected = False
                self.game.players[self.game.current_player].move_complete = True
                self.game.move_complete = True

            elif self.button_clicked and self.counter <= 2:
                if Constants.K_UP in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.UP)
                elif Constants.K_DOWN in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.DOWN)
                elif Constants.K_LEFT in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.LEFT)
                elif Constants.K_RIGHT in input_keys:
                    self.game.players[self.game.current_player].set_move(self.index_space, Constants.RIGHT)
                self.space_selected = False
                self.counter += 1
                if self.counter >= 2:
                    self.game.players[self.game.current_player].move_complete = True
                    self.game.move_complete = True
                    self.counter = 0
