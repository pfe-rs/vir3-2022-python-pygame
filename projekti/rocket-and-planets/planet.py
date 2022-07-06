import pygame
from vector import Vector
import global_vars


class Planet:
    planets = []

    def __init__(self, position, start_velocity, radius, color, display):
        self.position = position
        self.velocity = start_velocity
        self.radius = radius
        self.color = color
        self.mass = self.radius ** 2 * global_vars.planet_density
        self.slowdown_quotient = 0.7
        self.speedup_quotient = 3
        self.display = display
        Planet.planets.append(self)

    def update(self, delta_time):
        self.move(delta_time)
        self.check_collision()
        self.draw()

    def move(self, delta_time):
        resultant = Vector(0, 0)

        for planet in Planet.planets:
            if planet.position == self.position:
                continue

            diff = planet.position - self.position
            distance = diff.magnitude
            g_force = diff.normalized() * (global_vars.gravitational_constant * self.mass * planet.mass / (distance ** 2))
            resultant += g_force

        acceleration = resultant / self.mass
        self.velocity += acceleration * delta_time

        self.position += self.velocity * delta_time

    def check_collision(self):
        # Boundary check
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x *= -1
            self.velocity *= self.slowdown_quotient
        elif self.position.x + self.radius > global_vars.screen_w:
            self.position.x = global_vars.screen_w - self.radius
            self.velocity.x *= -1
            self.velocity *= self.slowdown_quotient
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y *= -1
            self.velocity *= self.slowdown_quotient
        elif self.position.y + self.radius > global_vars.screen_h:
            self.position.y = global_vars.screen_h - self.radius
            self.velocity.y *= -1
            self.velocity *= self.slowdown_quotient

        # Bouncing off of other planets
        for planet in Planet.planets:
            if self.position == planet.position:
                continue

            center_diff = self.position - planet.position
            if center_diff.magnitude < self.radius + planet.radius:
                # Elastic collision
                # self.position += center_diff.normalized() * (self.radius + planet.radius - center_diff.magnitude) * 1.3
                #
                # my_v_parallel = center_diff.normalized() * Vector.dot(self.velocity, center_diff) / center_diff.magnitude
                # my_v_normal = self.velocity - my_v_parallel
                # other_v_parallel = center_diff.normalized() * Vector.dot(planet.velocity, center_diff) / center_diff.magnitude
                # other_v_normal = self.velocity - other_v_parallel
                #
                # my_v_parallel = my_v_parallel.normalized() * (((self.mass - planet.mass) / (self.mass + planet.mass)) * my_v_parallel.magnitude + (2 * planet.mass / (self.mass + planet.mass)) * other_v_parallel.magnitude)
                # self.velocity = my_v_parallel * 1.3 + my_v_normal
                #
                # other_v_parallel = other_v_parallel.normalized() * (((planet.mass - self.mass) / (planet.mass + self.mass)) * other_v_parallel.magnitude + (2 * self.mass / (planet.mass + self.mass)) * my_v_parallel.magnitude)
                # planet.velocity = other_v_parallel * 1.3 + other_v_normal

                if center_diff.y == 0:
                    mirror_vector = Vector(0, 1)
                    self.bounce(mirror_vector)
                    planet.bounce(mirror_vector, self)
                else:
                    mirror_vector = Vector(1, - center_diff.x / center_diff.y)
                    self.bounce(mirror_vector)
                    planet.bounce(mirror_vector)

    def bounce(self, mirror_vector):
        # TODO: Turn this into an absolutely elastic collision
        mirror_vector = mirror_vector.normalized()
        self.velocity = mirror_vector * Vector.dot(self.velocity, mirror_vector) * self.speedup_quotient - self.velocity

    def draw(self):
        pygame.draw.circle(self.display, self.color, (self.position.x, self.position.y), self.radius)




