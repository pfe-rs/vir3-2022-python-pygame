import pygame
import time
import random
import math

from planet import Planet
from player import Player
from vector import Vector
from objective import Objective
import global_vars

# Initialize pygame stuff
pygame.init()

display = pygame.display.set_mode((global_vars.screen_w, global_vars.screen_h))
pygame.display.set_caption('Space mission')

# Set colors
BACKGROUND_COLOR = (6, 0, 36)

# Set up main game loop

last_frame_time = time.perf_counter()

# Set up game objects
game_objects = []

for i in range(global_vars.number_of_capture_points):
    rand_position = Vector(random.randint(0, global_vars.screen_w), random.randint(0, global_vars.screen_h))
    game_objects.append(Objective(rand_position, display))

planet_colors = [
    (240, 96, 43),
    (240, 252, 8),
    (31, 2, 219),
    (240, 17, 236),
]

for i in range(global_vars.number_of_planets):
    rand_position = Vector(random.randint(0, global_vars.screen_w), random.randint(0, global_vars.screen_h))
    rand_direction = random.random() * math.pi * 2
    rand_speed = random.random() * 0.3
    rand_radius = random.randint(10, 30)
    rand_color = random.randint(0, len(planet_colors) - 1)
    game_objects.append(
        Planet(
            rand_position,
            Vector(math.cos(rand_direction), math.sin(rand_direction)) * rand_speed,
            rand_radius,
            planet_colors[rand_color],
            display
        )
    )

game_objects.append(Player(display, Vector(global_vars.screen_w / 2, global_vars.screen_h / 2)))

# TODO: Add end screen

# Game loop
while not global_vars.game_over:
    # Basic set up
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            global_vars.game_over = True

    keys_pressed = pygame.key.get_pressed()

    # Delta time stuff
    current_time = time.perf_counter()
    delta_time = (current_time - last_frame_time) * 1000
    last_frame_time = current_time

    pygame.draw.line(display, (255, 255, 255), (0, 0), (250, 250))

    # Updating all objects
    for game_object in game_objects:
        game_object.update(delta_time)

    # Drawing all objects
    display.fill(BACKGROUND_COLOR)
    for game_object in game_objects:
        game_object.draw()
    pygame.display.update()


if global_vars.won or global_vars.lost:
    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
                quit_game = True

        display.fill(BACKGROUND_COLOR)
        font = pygame.font.Font('freesansbold.ttf', 20)
        if global_vars.won:
            text = font.render("ALL POINTS CAPTURED", True, (255, 255, 255), BACKGROUND_COLOR)
        else:
            text = font.render("GAME OVER", True, (255, 255, 255), BACKGROUND_COLOR)
        display.blit(text, (global_vars.screen_w // 2 - text.get_width() // 2, global_vars.screen_h // 2 - text.get_height() // 2))
        pygame.display.update()
