import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        return self / self.magnitude

    def as_tuple(self):
        return self.x, self.y

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return f'Vector({self.x}, {self.y})'
