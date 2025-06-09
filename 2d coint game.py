
import pygame
import random
import sys
import os
import platform
import time

# Beep sound for Windows
if platform.system() == "Windows":
    import winsound

pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT + 70))
pygame.display.set_caption("2D Teleport Game with Enemies")

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()

# Load high score
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

# Save high score
def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Initial values
player_x, player_y = 2, 2
coin_x, coin_y = random.randint(0, 4), random.randint(0, 4)
enemy_x, enemy_y = random.randint(0, 4), random.randint(0, 4)
score = 0
high_score = load_high_score()
timer = 30  # 30 seconds per level
start_time = time.time()
level = 1
enemy_speed = 30  # lower is faster

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Timer check
    time_left = max(0, timer - int(time.time() - start_time))

    if time_left == 0:
        level += 1
        start_time = time.time()
        enemy_speed = max(10, enemy_speed - 2)
        timer = 30

    # Draw grid
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Draw coin
    pygame.draw.circle(screen, GOLD, (coin_x * CELL_SIZE + CELL_SIZE // 2, coin_y * CELL_SIZE + CELL_SIZE // 2), 20)

    # Draw enemy
    pygame.draw.rect(screen, RED, (enemy_x * CELL_SIZE, enemy_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display score and timer
    score_text = font.render(f"Score: {score}  High: {high_score}  Time: {time_left}s  Level: {level}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT + 10))

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                player_y += 1
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                player_x += 1

    # Coin collect
    if player_x == coin_x and player_y == coin_y:
        score += 1
        if platform.system() == "Windows":
            winsound.Beep(800, 150)
        coin_x, coin_y = random.randint(0, 4), random.randint(0, 4)

    # Enemy random movement
    if random.randint(1, enemy_speed) == 1:
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and enemy_y > 0:
            enemy_y -= 1
        elif direction == "down" and enemy_y < GRID_SIZE - 1:
            enemy_y += 1
        elif direction == "left" and enemy_x > 0:
            enemy_x -= 1
        elif direction == "right" and enemy_x < GRID_SIZE - 1:
            enemy_x += 1

    # Enemy collision
    if player_x == enemy_x and player_y == enemy_y:
        score = 0
        start_time = time.time()  # reset level time
        if platform.system() == "Windows":
            winsound.Beep(300, 300)
        enemy_x, enemy_y = random.randint(0, 4), random.randint(0, 4)

    # Save high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    clock.tick(10)

pygame.quit()
sys.exit()
