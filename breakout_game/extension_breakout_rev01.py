"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from extension_breakoutgraphics_rev01 import BreakoutGraphics
import random

FRAME_RATE = 10  # 100 frames per second
NUM_LIVES = 3  # Number of attempts


def main():
    graphics = BreakoutGraphics()
    vx = 0
    vy = 0
    lives = NUM_LIVES
    num_bricks = graphics.num_bricks
    item_falling = False
    item_caught = False
    score = 0
    item_score = 0

    # Add the animation loop here!
    while True:
        # Update: ball movement
        if graphics.start_ball:
            graphics.ball.move(graphics.vx, graphics.vy)
        # Update: item
        if item_falling:
            graphics.item.move(0, 3)
        # Update: score
        if item_caught:
            score += item_score
            item_score = 0
            item_caught = False
        graphics.scoreboard.text = f"Score: {score}"
        # Update: lives
        graphics.lives.text = f"Lives: {lives}"
        # Check: end game conditions
        if lives == 0:
            graphics.game_over = True
            graphics.end_game_message(0)
            break
        if num_bricks == 0:
            graphics.game_over = True
            graphics.end_game_message(1)
            break
        # Check: ball's collision with walls
        if graphics.ball.x <= 0 or graphics.ball.x >= graphics.window.width - graphics.ball.width:
            graphics.vx = -1
            if graphics.ball.x < 0:  # To prevent ball from sticking to wall
                graphics.ball.x = 0
            if graphics.ball.x > graphics.window.width - graphics.ball.width:
                graphics.ball.x = graphics.window.width - graphics.ball.width
        if graphics.ball.y <= 0:
            graphics.vy = -1
            if graphics.ball.y < 0:  # To prevent ball from sticking to wall
                graphics.ball.y = 0
        # Check: ball's collision with paddle and bricks
        for i in range(2):
            for j in range(2):
                ball_vertex_x = graphics.ball.x + graphics.ball.width * j
                ball_vertex_y = graphics.ball.y + graphics.ball.height * i
                obj = graphics.window.get_object_at(ball_vertex_x, ball_vertex_y)
                if obj is not None:
                    if obj is graphics.paddle:
                        # To prevent ball from stuck in paddle
                        if graphics.vy > 0:
                            graphics.vy = -1
                        # If ball going right hitting paddle's left part, change ball direction to left, and vice versa
                        if graphics.vx > 0 and graphics.ball.x + graphics.ball.width / 2 < obj.x + obj.width / 2:
                            graphics.vx = -1
                        elif graphics.vx < 0 and graphics.ball.x + graphics.ball.width / 2 > obj.x + obj.width / 2:
                            graphics.vx = (-1)
                    elif obj is graphics.item or obj is graphics.scoreboard or obj is graphics.lives:
                        pass
                    else:
                        graphics.vy = (-1)
                        graphics.window.remove(obj)
                        score += 100
                        num_bricks -= 1
                        # Trigger item falling
                        if random.random() < 0.5 and not item_falling:
                            if random.random() < 0.4:
                                graphics.item.fill_color = 'green'
                                item_score = 50
                            else:
                                graphics.item.fill_color = 'red'
                                item_score = -50
                            graphics.window.add(graphics.item,
                                                x=ball_vertex_x + (graphics.brick_width - graphics.item.width) / 2,
                                                y=ball_vertex_y)
                            item_falling = True
                    break
        # Check: item's collision with paddle
        # get_object_at() doesn't work here, so I figured out another way
        for i in range(4):
            item_vertex_x = graphics.item.x + graphics.item.width * (i % 2)
            item_vertex_y = graphics.item.y + graphics.item.height * (i // 2)
            if graphics.paddle.x <= item_vertex_x <= graphics.paddle.x + graphics.paddle.width and \
                    graphics.paddle.y <= item_vertex_y <= graphics.paddle.y + graphics.paddle.height:
                item_caught = True
                graphics.window.remove(graphics.item)
                item_falling = False
                break

        # Check: item falls out
        if graphics.item.y >= graphics.window.height - graphics.item.height:
            graphics.window.remove(graphics.item)
            item_falling = False
        # Check: ball falls out
        if graphics.ball.y >= graphics.window.height - graphics.ball.height:
            graphics.ball.x = (graphics.window.width - graphics.ball.width) / 2
            graphics.ball.y = (graphics.window.height - graphics.ball.height) / 2
            graphics.vx = 0
            graphics.vy = 0
            graphics._start_ball = False
            lives -= 1
            graphics.window.remove(graphics.item)

        # Pause
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
