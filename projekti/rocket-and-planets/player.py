import math
import pygame

import global_vars
from vector import Vector
from planet import Planet
from objective import Objective


class Player:
    def __init__(self, display, start_position=Vector(0, 0), move_speed=0.5, turn_speed=0.01):
        self.position = start_position
        self.velocity = Vector(0, 0)
        self.move_speed = move_speed
        self.turn_speed = turn_speed
        self.display = display
        self.direction = -3.14 / 2
        self.color = (255, 255, 255)
        self.scale = 10
        self.mass = 50
        self.throttle_power = 0.03
        self.engine_on = False

    def update(self, delta_time):
        # Input handling
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.direction += self.turn_speed * delta_time
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.direction -= self.turn_speed * delta_time

        # Calculate forces, velocity, and new position
        resultant = Vector(0, 0)

        self.engine_on = False
        if pygame.key.get_pressed()[pygame.K_UP]:
            resultant += Vector(math.cos(self.direction), math.sin(self.direction)) * self.throttle_power
            self.engine_on = True

        for planet in Planet.planets:
            diff = planet.position - self.position
            distance = diff.magnitude
            g_force = diff.normalized() * (global_vars.gravitational_constant * self.mass * planet.mass / (distance ** 2))
            resultant += g_force

        acceleration = resultant / self.mass
        self.velocity += acceleration * delta_time
        self.position += self.velocity * delta_time

        # Boundary check
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x = 0
        elif self.position.x > global_vars.screen_w:
            self.position.x = global_vars.screen_w
            self.velocity.x = 0
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y = 0
        elif self.position.y > global_vars.screen_h:
            self.position.y = global_vars.screen_h
            self.velocity.y = 0

        # Collision detection
        for planet in Planet.planets:
            if (self.position - planet.position).magnitude <= planet.radius:
                global_vars.lost = True
                global_vars.game_over = True

        # Check for objectives
        for objective in Objective.objectives:
            if (self.position - objective.position).magnitude < objective.radius:
                objective.captured = True

                all_captured = True
                for objective_again in Objective.objectives:
                    if not objective_again.captured:
                        all_captured = False

                if all_captured:
                    global_vars.won = True
                    global_vars.game_over = True

    def draw(self):
        # Drawing the fire
        if self.engine_on:
            back_point = self.position + Vector(math.cos(self.direction + math.pi), math.sin(self.direction + math.pi)) * self.scale * 2
            front_left_point = self.position + Vector(math.cos(self.direction + 2.5), math.sin(self.direction + 2.5)) * self.scale * 0.7
            front_right_point = self.position + Vector(math.cos(self.direction - 2.5), math.sin(self.direction - 2.5)) * self.scale * 0.7
            pygame.draw.polygon(self.display, (255, 94, 0), points=[
                back_point.as_tuple(),
                front_left_point.as_tuple(),
                front_right_point.as_tuple()
            ])

        # Drawing the ship
        front_point = self.position + Vector(math.cos(self.direction), math.sin(self.direction)) * self.scale
        back_left_point = self.position + Vector(math.cos(self.direction + 2.5), math.sin(self.direction + 2.5)) * self.scale
        back_right_point = self.position + Vector(math.cos(self.direction - 2.5), math.sin(self.direction - 2.5)) * self.scale
        pygame.draw.polygon(self.display, self.color, points=[
            (front_point.x, front_point.y),
            (back_left_point.x, back_left_point.y),
            (back_right_point.x, back_right_point.y)
        ])
