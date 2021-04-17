class Constants:
    """
    Constant class that contains static variables
    """
    # Dimensions.
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    BOARD_SIZE = WINDOW_WIDTH/2
    DIAMETER = 4
    # Colors for balls.
    YELLOW = "y"
    WHITE = "g"
    RED = "r"
    BLUE = "b"
    ORANGE = "o"
    PURPLE = "p"
    EMPTY = " "
    COLORS = [YELLOW, WHITE, RED, BLUE, ORANGE, PURPLE]
    # Directions for moves.
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
    # Types of moves.
    SINGLE = 1
    DOUBLE = 2
    MOVE_TYPE = [SINGLE, DOUBLE]
    # Keyboard events.
    K_UP = 1073741906
    K_RIGHT = 1073741903
    K_DOWN = 1073741905
    K_LEFT = 1073741904
