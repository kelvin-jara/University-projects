import pygame
import sys
from Program.helpers.constants import Constants
from Program.helpers.keyborad_handler import KeyboardHandler
from Program.collecto import Collecto
from Program.human_player import HumanPlayer
from Program.min_max_player import MinMaxPlayer
from Program.min_max_player_simple import MinMaxPlayerSimple
from Program.balls_keeper import BallKeeper
from Program.game_view import GameView
import concurrent.futures


class Game:
    def __init__(self):
        # init Pygame
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.keyboard_handler = KeyboardHandler()
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 50)
        self.time = pygame.time.get_ticks()
        self.bag1 = BallKeeper()
        self.bag2 = BallKeeper()
        self.player1 = MinMaxPlayerSimple("AI 1", self.bag1)
        # self.player2 = MinMaxPlayerSimple("AI 2", self.bag2)
        self.player2 = HumanPlayer("Human 2", self.bag2)
        self.game = Collecto(self.player1, self.player2)
        self.game_view = GameView(self.game, self.screen, self.font)
        self.game.game_view = self.game_view

    """
        Method 'game_loop' will be executed every frame to drive
        the display and handling of events in the background. 
        In Processing this is done behind the screen. Don't 
        change this, unless you know what you are doing.
        """

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.handle_events()
        self.update_game(delta_time)
        self.draw_components()

    """
        Method 'update_game' is there to update the state of variables 
        and objects from frame to frame.
        """

    def update_game(self, dt):
        if not self.game.game_ended_bool:
            self.game.do_move()
        if self.game_view.new_game:
            self.game_view.new_game = False
            self.reset()

    """
        Method 'draw_components' is similar is meant to contain 
        everything that draws one frame. It is similar to method
        void draw() in Processing. Put all draw calls here. Leave all
        updates in method 'update'
        """

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.game_view.draw_game()
        pygame.display.flip()

    def reset(self):
        self.__init__()

    """
    Method 'handle_event' loop over all the event types and 
    handles them accordingly. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """

    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)
        self.game_view.on_keys_pressed(self.keyboard_handler.pressed)

    """
    This method will remove a released button 
    from list 'keyboard_handler.pressed'.
    """

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    """
    Similar to void mouseMoved() in Processing
    """

    def handle_mouse_motion(self, event):
        pass

    """
    Similar to void mousePressed() in Processing
    """

    def handle_mouse_pressed(self, event):
        self.game_view.on_mouse_clicked(pygame.mouse.get_pos())

    """
    Similar to void mouseReleased() in Processing
    """

    def handle_mouse_released(self, event):
        pass


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
