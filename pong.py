import arcade
import os
import random

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong Game"

PADDLE_SPEED = 5
BALL_SPEED = 4

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Initialize variables and game state
        self.all_sprites = None
        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        self.left_up_pressed = False
        self.left_down_pressed = False
        self.right_up_pressed = False
        self.right_down_pressed = False
        self.game_started = False
        self.score_left = 0
        self.score_right = 0
        self.max_points = 5 
        self.game_over = False
        self.sound_applause = None
        self.applause_played = False

    def setup(self):
        # Initialize game objects and sounds
        self.all_sprites = arcade.SpriteList()

        # Ask player for number of rounds to win
        while True:
            try:
                rounds = int(input("Enter the number of points to win: "))
                if rounds > 0:
                    self.max_points = rounds
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        # Load sound effects
        self.sound_paddle = arcade.load_sound(os.path.join("sounds", "paddle.wav"))
        self.sound_wall = arcade.load_sound(os.path.join("sounds", "wall.wav"))
        self.sound_applause = arcade.load_sound(os.path.join("sounds", "aplause.wav"))

        # Create left paddle
        self.left_paddle = arcade.SpriteSolidColor(10, 100, arcade.color.WHITE)
        self.left_paddle.center_x = 30
        self.left_paddle.center_y = SCREEN_HEIGHT // 2
        self.all_sprites.append(self.left_paddle)

        # Create right paddle
        self.right_paddle = arcade.SpriteSolidColor(10, 100, arcade.color.WHITE)
        self.right_paddle.center_x = SCREEN_WIDTH - 30
        self.right_paddle.center_y = SCREEN_HEIGHT // 2
        self.all_sprites.append(self.right_paddle)

        # Create ball
        self.ball = arcade.SpriteCircle(10, arcade.color.WHITE)
        self.ball.center_x = SCREEN_WIDTH // 2
        self.ball.center_y = SCREEN_HEIGHT // 2
        self.ball.change_x = 0
        self.ball.change_y = 0
        self.all_sprites.append(self.ball)

    def on_draw(self):
        # Clear screen and draw all sprites
        self.clear()
        self.all_sprites.draw()

        # Draw score
        score_text = f"{self.score_left}     {self.score_right}"
        arcade.draw_text(score_text,
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
                        arcade.color.WHITE, font_size=30, anchor_x="center")

        # Display game over message if necessary
        if self.game_over:
            winner_text = ""
            if self.score_left >= self.max_points:
                winner_text = "Left Player Wins!"
            elif self.score_right >= self.max_points:
                winner_text = "Right Player Wins!"
            arcade.draw_text(winner_text,
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80,
                            arcade.color.YELLOW, font_size=40, anchor_x="center")
        else:
            # Display start message
            if not self.game_started:
                arcade.draw_text("Press SPACE to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                                arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_update(self, delta_time):
        # Update ball position
        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y

        # Ball bounces off top and bottom walls
        if self.ball.top > SCREEN_HEIGHT or self.ball.bottom < 0:
            self.ball.change_y *= -1
            arcade.play_sound(self.sound_wall)

        # Check collision with left paddle
        if arcade.check_for_collision(self.ball, self.left_paddle):
            self.ball.left = self.left_paddle.right
            self.ball.change_x = abs(self.ball.change_x)
            arcade.play_sound(self.sound_paddle)

        # Check collision with right paddle
        if arcade.check_for_collision(self.ball, self.right_paddle):
            self.ball.right = self.right_paddle.left
            self.ball.change_x = -abs(self.ball.change_x)
            arcade.play_sound(self.sound_paddle)

        # Move left paddle
        if self.left_up_pressed and self.left_paddle.top < SCREEN_HEIGHT:
            self.left_paddle.center_y += PADDLE_SPEED
        if self.left_down_pressed and self.left_paddle.bottom > 0:
            self.left_paddle.center_y -= PADDLE_SPEED

        # Move right paddle
        if self.right_up_pressed and self.right_paddle.top < SCREEN_HEIGHT:
            self.right_paddle.center_y += PADDLE_SPEED
        if self.right_down_pressed and self.right_paddle.bottom > 0:
            self.right_paddle.center_y -= PADDLE_SPEED

        # Check if ball goes out of bounds
        if self.ball.left < 0:
            self.score_right += 1
            self.reset_ball()
            self.game_started = False

        elif self.ball.right > SCREEN_WIDTH:
            self.score_left += 1
            self.reset_ball()
            self.game_started = False

        # Check for game over
        if self.score_left >= self.max_points or self.score_right >= self.max_points:
            self.game_over = True
            self.game_started = False
            self.ball.change_x = 0
            self.ball.change_y = 0

            if not self.applause_played:
                arcade.play_sound(self.sound_applause)
                self.applause_played = True

    def on_key_press(self, key, modifiers):
        # Start game when SPACE is pressed
        if not self.game_started and key == arcade.key.SPACE:
            self.ball.change_x = random.choice([-BALL_SPEED, BALL_SPEED])
            self.ball.change_y = random.choice([-BALL_SPEED, BALL_SPEED])
            self.game_started = True

        # Paddle controls
        if key == arcade.key.W:
            self.left_up_pressed = True
        elif key == arcade.key.S:
            self.left_down_pressed = True
        elif key == arcade.key.UP:
            self.right_up_pressed = True
        elif key == arcade.key.DOWN:
            self.right_down_pressed = True

        # Restart game with R
        elif key == arcade.key.R:
            self.score_left = 0
            self.score_right = 0
            self.game_over = False
            self.reset_ball()
            self.game_started = False
            self.applause_played = False

    def on_key_release(self, key, modifiers):
        # Stop paddle movement when keys are released
        if key == arcade.key.W:
            self.left_up_pressed = False
        elif key == arcade.key.S:
            self.left_down_pressed = False
        elif key == arcade.key.UP:
            self.right_up_pressed = False
        elif key == arcade.key.DOWN:
            self.right_down_pressed = False

    def reset_ball(self):
        # Reset ball position and stop movement
        self.ball.center_x = SCREEN_WIDTH // 2
        self.ball.center_y = SCREEN_HEIGHT // 2
        self.ball.change_x = 0
        self.ball.change_y = 0

def main():
    game = PongGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
