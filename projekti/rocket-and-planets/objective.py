import pygame

green = (87, 245, 66)
blue = (66, 108, 245)


class Objective:
    objectives = []

    def __init__(self, position, display):
        self.position = position
        self.display = display
        self.captured = False
        self.radius = 50
        Objective.objectives.append(self)

    def draw(self):
        color = blue
        if self.captured:
            color = green
        pygame.draw.circle(self.display, color, self.position.as_tuple(), self.radius)

    def update(self, delta_time):
        pass
