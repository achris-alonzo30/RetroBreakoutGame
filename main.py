import pygame
import random
import os

# App Dimension
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title
pygame.display.set_caption("Atari Breakout Game")

# -------------------------------------------------------------------------------------------------------------------- #
# Initialize Pygame font module
pygame.font.init()
# Set Font
font_path = os.path.join(os.path.dirname(__file__), "font", "Minecraft.ttf")
font = pygame.font.Font(font_path, 50)

# -------------------------------------------------------------------------------------------------------------------- #
# Images dimensions
paddle_dimension = (200, 40)
ball_dimension = (40, 40)
health_dimension = (50, 50)
slime_dimension = (100, 75)
extra_health_dimension = (78, 72)
coin_dimension = (100, 75)
title_dimension = (400, 300)

# Load Images
background_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "background.png")), (WIDTH, HEIGHT))
paddle_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "main_paddle.png")), paddle_dimension)
ball_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "ball.png")), ball_dimension)
health_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "health.png")), health_dimension)
slime_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "slime.png")), slime_dimension)
extra_health_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "extra_health.png")),
                                            extra_health_dimension)
coin_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "coin.png")), coin_dimension)
title_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "title.png")), (WIDTH, HEIGHT))

# -------------------------------------------------------------------------------------------------------------------- #
# Constant Variables
SCORE = 0
FPS = 60
BALL_VEL = 5
PADDLE_VEL = 10
HEALTH_COUNT = 3
SLIME_ROW_COUNT = 5
SLIME_COLUMN_COUNT = 9
COIN_ROW = random.randint(0, SLIME_ROW_COUNT - 1)  # Randomly choose a row for the unique object
COIN_COLUMN = random.randint(0, SLIME_COLUMN_COUNT - 1)  # Randomly choose a column for the unique object
EXTRA_HEALTH_ROW = random.randint(0, SLIME_ROW_COUNT - 1)  # Randomly choose a row for the unique object
EXTRA_HEALTH_COLUMN = random.randint(0, SLIME_COLUMN_COUNT - 1)  # Randomly choose a column for the unique object

while EXTRA_HEALTH_ROW == COIN_ROW and EXTRA_HEALTH_COLUMN == COIN_COLUMN:
    EXTRA_HEALTH_ROW = random.randint(0, SLIME_ROW_COUNT - 1)
    EXTRA_HEALTH_COLUMN = random.randint(0, SLIME_COLUMN_COUNT - 1)


# -------------------------------------------------------------------------------------------------------------------- #
# Main Game Objects
class Ball:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, ball_dimension[0], ball_dimension[1])
        self.dx = dx
        self.dy = dy

    def reset_position(self):
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - 80


class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, direction):
        if direction == "LEFT" and self.rect.x > 0:  # Move to the left
            self.rect.x -= PADDLE_VEL
        elif direction == "RIGHT" and self.rect.x < WIDTH - self.rect.width:  # Move to the right
            self.rect.x += PADDLE_VEL

    def reset_position(self):
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - 40


# -------------------------------------------------------------------------------------------------------------------- #
#  Function when the game round finish
def increase_velocity():
    global BALL_VEL, PADDLE_VEL
    BALL_VEL *= 1.5
    PADDLE_VEL *= 1.2


# -------------------------------------------------------------------------------------------------------------------- #
# Initialize the objects in the window
def draw_window(paddle, ball, health, text, slimes, coins, extra_healths):
    WIN.blit(background_image, (0, 0))
    WIN.blit(text, (765, 20))
    WIN.blit(paddle_image, (paddle.rect.x, paddle.rect.y))
    WIN.blit(ball_image, (ball.rect.x, ball.rect.y))

    health_spacing = 15  # Spacing between health images
    for i in range(HEALTH_COUNT):
        x = health.x + i * (health_dimension[0] + health_spacing)
        y = health.y
        WIN.blit(health_image, (x, y))

    slime_spacing = 10  # Spacing between slime images
    for slime in slimes:
        WIN.blit(slime_image, (slime.x, slime.y))

    for coin in coins:
        WIN.blit(coin_image, (coin.x, coin.y))

    for extra_health in extra_healths:
        WIN.blit(extra_health_image, (extra_health.x, extra_health.y))

    pygame.display.update()


# -------------------------------------------------------------------------------------------------------------------- #
# Ball Movement Mechanics
def ball_handle_movement(ball):
    ball.rect.x += ball.dx
    ball.rect.y += ball.dy


def handle_collisions(ball, paddle, slimes, coins, extra_healths):
    global HEALTH_COUNT, SCORE

    # Collision with paddle
    if ball.rect.colliderect(paddle.rect):
        # When ball hits the paddle, the ball moves in the opposite direction
        ball.dy = -ball.dy

    # Collision with walls ( EAST, WEST )
    if ball.rect.x <= 0 or ball.rect.x >= WIDTH - ball.rect.width:
        ball.dx = -ball.dx
    # Collision with walls ( NORTH )
    if ball.rect.y <= 0:
        ball.dy = -ball.dy

    # Ball passes below paddle ( SOUTH )
    if ball.rect.y >= HEIGHT:
        # Decrease player health here
        HEALTH_COUNT -= 1
        ball.reset_position()
        paddle.reset_position()

    # Collision with slime
    for slime in slimes:
        if ball.rect.colliderect(slime):
            ball.dy = -ball.dy
            slimes.remove(slime)
            SCORE += 1

    # Collision with coin
    for coin in coins:
        # Score multiplier here
        if ball.rect.colliderect(coin):
            ball.dy = -ball.dy
            coins.remove(coin)
            SCORE *= 2

    # Collision with heart
    for extra_health in extra_healths:
        if ball.rect.colliderect(extra_health):
            ball.dy = -ball.dy
            extra_healths.remove(extra_health)
            # Add extra health here
            if HEALTH_COUNT < 3:
                HEALTH_COUNT += 1  # But if user has 3 healths then don't add more

    # Update the score text
    score_text = font.render(str(SCORE), True, 'white')
    return score_text


# -------------------------------------------------------------------------------------------------------------------- #
def generate_objects(slimes, coins, extra_healths):
    slime_spacing = 10  # Spacing between slime images
    for i in range(SLIME_ROW_COUNT):
        for j in range(SLIME_COLUMN_COUNT):
            x = 10 + j * (slime_dimension[0] + slime_spacing)
            y = 100 + i * (slime_dimension[1] + slime_spacing)

            if i == COIN_ROW and j == COIN_COLUMN:
                # Add unique coin object
                coins.append(pygame.Rect(x, y, coin_dimension[0], coin_dimension[1]))
            elif i == EXTRA_HEALTH_ROW and j == EXTRA_HEALTH_COLUMN:
                # Add unique extra_health object
                extra_healths.append(pygame.Rect(x, y, extra_health_dimension[0], extra_health_dimension[1]))
            else:
                # Add regular slime object
                slimes.append(pygame.Rect(x, y, slime_dimension[0], slime_dimension[1]))


# -------------------------------------------------------------------------------------------------------------------- #
# Main Function
def play_game():
    # Set position of paddle, ball, and health
    paddle = Paddle(WIDTH // 2 - 100, HEIGHT - 40, 200, 40)
    ball = Ball(WIDTH // 2 - 20, HEIGHT - 80, BALL_VEL, -BALL_VEL)
    health = pygame.Rect(275, 20, 50, 50)

    # Create respective variables for the objects
    slimes = []
    coins = []
    extra_healths = []
    generate_objects(slimes, coins, extra_healths)

    # Set clock for FPS
    clock = pygame.time.Clock()

    # Main Loop
    is_game_over = False
    while not is_game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = True

        # Move the paddle
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            paddle.move("LEFT")
        if keys_pressed[pygame.K_RIGHT]:
            paddle.move("RIGHT")

        # Move the ball
        ball_handle_movement(ball)

        # Handle collisions and update score text
        score_text = handle_collisions(ball, paddle, slimes, coins, extra_healths)
        draw_window(paddle, ball, health, score_text, slimes, coins, extra_healths)

        # Game is over
        if HEALTH_COUNT == 0:
            is_game_over = True
            pygame.quit()

        # Check if all objects are removed
        if len(slimes) == 0 and len(coins) == 0 and len(extra_healths) == 0:
            global SCORE
            SCORE *= 2
            generate_objects(slimes, coins, extra_healths)
            paddle.reset_position()
            ball.reset_position()
            increase_velocity()

    pygame.quit()


# Title Screen
def title_screen():
    text_font = pygame.font.Font(font_path, 60)

    run = True
    while run:
        WIN.blit(title_image, (0, 0))

        prompt_text = text_font.render("Do you want to play? \n Yes or No", True, 'white')
        WIN.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2,
                               HEIGHT // 2 + prompt_text.get_height() + 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    run = False
                    play_game()
                elif event.key == pygame.K_n:
                    run = False
                    pygame.quit()


if __name__ == "__main__":
    title_screen()
