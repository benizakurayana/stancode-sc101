"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels) 75
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self._window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self._paddle = GRect(width=paddle_width, height=paddle_height, x=(self._window.width - paddle_width) / 2,
                             y=self._window.height - paddle_offset - paddle_height)
        self._paddle.filled = True
        self._window.add(self._paddle)

        # Center a filled ball in the graphical window
        self._ball = GOval(ball_radius * 2, ball_radius * 2)
        self._ball.filled = True
        self._window.add(self._ball, x=(self._window.width - ball_radius * 2) / 2,
                         y=(self._window.height - ball_radius * 2) / 2)
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners
        onmouseclicked(self.click_start)
        onmousemoved(self.move_paddle)
        # Draw bricks
        self._brick_width = brick_width
        self._brick_height = brick_height
        for i in range(brick_rows):
            for j in range(brick_cols):
                brick = self.make_brick(j)
                self._window.add(brick, x=i * (brick_width + brick_spacing),
                                 y=brick_offset + j * (brick_height + brick_spacing))
        # Start ball
        self._start_ball = False
        # Number of bricks
        self._num_bricks = brick_rows * brick_cols
        # Game message
        self._message = GLabel("CLICK TO START")
        self._message.x = (self._window.width - self._message.width) / 2
        self._message.y = self._window.height * 2 / 3 + self._message.height / 2
        self._window.add(self._message)
        # Game end
        self._game_over = False

        # Item
        self._item = GRect(ball_radius * 2, ball_radius * 2)
        self._item.filled = True
        # Scoreboard
        self._scoreboard = GLabel("Score: ")
        self._scoreboard.x = 0
        self._scoreboard.y = self._window.height
        self._scoreboard.font = "arial-16"
        self._window.add(self._scoreboard)
        # Lives
        self._lives = GLabel("Lives:   ")
        self._lives.x = self._window.width - self._lives.width * 2
        self._lives.y = self._window.height
        self._lives.font = "arial-16"
        self._window.add(self._lives)

    def make_brick(self, j):
        brick = GRect(self._brick_width, self._brick_height)
        brick.filled = True
        if 0 <= j < 2:
            brick.fill_color = 'red'
            brick.color = 'red'
        elif 2 <= j < 4:
            brick.fill_color = 'orange'
            brick.color = 'orange'
        elif 4 <= j < 6:
            brick.fill_color = 'yellow'
            brick.color = 'yellow'
        elif 6 <= j < 8:
            brick.fill_color = 'green'
            brick.color = 'green'
        elif 8 <= j < 10:
            brick.fill_color = 'blue'
            brick.color = 'blue'
        return brick

    def move_paddle(self, event):
        if self._paddle.width / 2 < event.x < self._window.width - self._paddle.width / 2:
            self._paddle.x = event.x - self._paddle.width / 2

    def click_start(self, event):
        if not self._start_ball and not self.game_over:
            self._window.remove(self._message)
            self._start_ball = True
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

    # def get_vx(self):
    #     return self.__dx
    #
    # def get_vy(self):
    #     return self.__dy

    def end_game_message(self, result):
        if result == 1:
            self._window.remove(self._ball)
            self._window.remove(self._paddle)
            self._message.text = "YOU WIN!"
            self._window.add(self._message)
        elif result == 0:
            self._window.remove(self._ball)
            self._window.remove(self._paddle)
            self._message.text = "YOU LOSE"
            self._window.add(self._message)

    @property
    def vx(self):
        return self.__dx

    @vx.setter
    def vx(self, rate):
        self.__dx = self.__dx * rate

    @property
    def vy(self):
        return self.__dy

    @vy.setter
    def vy(self, rate):
        self.__dy = self.__dy * rate

    @property
    def window(self):
        return self._window

    @property
    def ball(self):
        return self._ball

    @property
    def paddle(self):
        return self._paddle

    @property
    def message(self):
        return self._message

    @property
    def num_bricks(self):
        return self._num_bricks

    @property
    def start_ball(self):
        return self._start_ball

    @start_ball.setter
    def start_ball(self, value):
        self._start_ball = value

    @property
    def game_over(self):
        return self._game_over

    @game_over.setter
    def game_over(self, value):
        self._game_over = value

    @property
    def item(self):
        return self._item

    @property
    def scoreboard(self):
        return self._scoreboard

    @scoreboard.setter
    def scoreboard(self, value):
        self.scoreboard = value

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self.lives = value

    @property
    def brick_width(self):
        return self._brick_width

    @property
    def paddle_width(self):
        return self._paddle.width
    @paddle.setter
    def paddle_width(self,rate):
        self._window.remove(self._paddle)
        self._paddle._width = self._paddle._width * rate
        self._window.add(self._paddle)