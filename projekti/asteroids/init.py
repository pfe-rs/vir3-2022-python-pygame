import pygame
import glob
import math
import random

pygame.init()

bulletpng = pygame.image.load("./assets/bullet.png")

theindex = None
ast_nfts = []
for i, path in enumerate(glob.glob("./assets/asteroid*")):
    if path.endswith("11.png") and theindex == None:
        theindex = i
    ast_nfts.append(pygame.image.load(path))

sounds = {
    "fire": pygame.mixer.Sound("./assets/fire.wav"),
    "smallboom": pygame.mixer.Sound("./assets/smallboom.wav"),
    "mediumboom": pygame.mixer.Sound("./assets/mediumboom.wav"),
    "largeboom": pygame.mixer.Sound("./assets/largeboom.wav"),
    "life": pygame.mixer.Sound("./assets/life.wav"),
    "beat1": pygame.mixer.Sound("./assets/beat1.wav"),
    "beat2": pygame.mixer.Sound("./assets/beat2.wav")
}
for k in sounds:
    sounds[k].set_volume(0.2)


players = {
    "normal": pygame.image.load(
        "./assets/ship1.png"),
    "accelerating": pygame.image.load(
        "./assets/ship2.png")
}
sizes = ["smallboom", "mediumboom", "largeboom"]

bullets = []
asteroids = []


def towards(n, mod, center=0, span=0):
    if n < center:
        if n > center - mod:
            n = center
        else:
            if span != 0 and n + mod < center - span:
                n = center - span
            else:
                n += mod
    else:
        if n < center + mod:
            n = center
        else:
            if span != 0 and n - mod > center + span:
                n = center + span
            else:
                n -= mod
    return n


def span(n, mod, span, fallback=True):
    if abs(n + mod) > span:
        if abs(n) < span or fallback:
            n = span if mod > 0 else -span
    elif mod != 0:
        n += mod
    return n


def wrap(n, mod, max, give=0, min=0):
    if n + mod > max + give:
        n = min - give
    elif n + mod < min - give:
        n = max + give
    else:
        n += mod
    return n


tolerance = 4
ignorevless = 0.005


class Player:
    def __init__(self, x, y, vmax, acc, fric, dang, vblt):
        self.angle = 0

        image, image2 = players["normal"], players["accelerating"]

        self.img_stat = image.convert_alpha()
        self.img_acc = image2.convert_alpha()
        self.image = self.img_stat
        self.rect = image.get_rect(center=(round(x), round(y)))
        self.mask = pygame.mask.from_surface(image)

        self.givex = self.image.get_width() / 2 + tolerance
        self.givey = self.image.get_height() / 2 + tolerance

        width, height = image.get_size()
        pygame.draw.rect(image, (255, 0, 0), [
                         0, 0, width, height], 1)
        self.vmax = vmax
        self.fric = fric
        self.isacc = False
        self.acc = acc
        self.vx = 0
        self.vy = 0

        self.died = False

        self.vblt = vblt
        self.dang = dang

        self.x = x
        self.y = y

    def forward(self):
        self.isacc = True
        self.updateimg()

        angle = math.radians(self.angle + 90)
        xmult = math.cos(angle)
        ymult = -math.sin(angle)

        vmax = self.vmax
        xmod = self.acc * xmult
        ymod = self.acc * ymult

        self.vx = span(self.vx, xmod, abs(xmult * vmax), False)
        self.vy = span(self.vy, ymod, abs(ymult * vmax), False)

    def draw(self, surface, idle):
        if not idle:
            vx, vy = self.vx, self.vy

            if abs(self.vx) < ignorevless:
                self.vx = 0
            if abs(self.vy) < ignorevless:
                self.vy = 0

            width, height = surface.get_size()

            self.x = wrap(self.x, vx, width, self.givex, -self.givex)
            self.y = wrap(self.y, vy, height, self.givey, -self.givey)

            valpha = math.atan2(vy, vx) - math.pi
            xmult = math.cos(valpha)
            ymult = math.sin(valpha)

            vmax, fric = self.vmax, self.fric

            self.vx = span(vx, xmult * fric, vmax, False)
            self.vy = span(vy, ymult * fric, vmax, False)

        self.rect.center = (round(self.x), round(self.y))
        self.updateimg()
        if self.isacc:
            self.isacc = False
        surface.blit(self.image, self.rect)

    def updateimg(self):
        angle = self.angle
        if round(angle) == 0:
            self.image = self.img_acc if self.isacc else self.img_stat
            self.mask = pygame.mask.from_surface(self.image)
            rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = pygame.transform.rotate(
                (self.img_acc if self.isacc else self.img_stat).copy(), angle)
            self.mask = pygame.mask.from_surface(self.image)
            rect = self.image.get_rect(center=self.rect.center)
        self.rect = rect

    def rotate(self, angle):
        if angle > 360:
            angle -= 360
        elif angle < 0:
            angle += 360
        self.angle = angle
        self.updateimg()

        return self.angle

    def rotate_r(self):
        return self.rotate(self.angle - self.dang)

    def rotate_l(self):
        return self.rotate(self.angle + self.dang)

    def shoot(self):
        angle = math.radians(self.angle + 90)
        xmult = math.cos(angle)
        ymult = -math.sin(angle)

        bx, by = self.rect.center
        bx += self.image.get_width() / 2 * xmult
        by += self.image.get_height() / 2 * ymult

        bullets.append(Bullet(bulletpng,
                              bx, by, self.angle, self.vblt))
        sounds["fire"].play()

    def kill(self, _):
        self.died = True
        sounds["largeboom"].play()


WHITE = (255, 255, 255)


class Bullet:
    def __init__(self, image, x, y, angle, v):
        self.image = image.convert_alpha()
        self.rect = image.get_rect(center=(round(x), round(y)))
        self.mask = pygame.mask.from_surface(image)

        self.x = x
        self.y = y

        self.angle = angle
        self.v = v

        self.givex = self.image.get_width() / 2 + tolerance
        self.givey = self.image.get_height() / 2 + tolerance

        self.frames = 0

    def draw(self, surface, idle):
        if not idle:
            angle = math.radians(self.angle + 90)
            xmult = math.cos(angle)
            ymult = -math.sin(angle)

            width, height = surface.get_size()

            self.x = wrap(self.x, self.v * xmult,
                          width, self.givex, -self.givex)
            self.y = wrap(self.y, self.v * ymult,
                          height, self.givey, -self.givey)

            self.rect.center = (round(self.x), round(self.y))
            self.frames += 1

        surface.blit(self.image, self.rect)

    # ?? ??   ?  ? ? ?? ? ??   ?   ?? ??  ????  ??   ??
    def colliding(self, body):
        # ?? ??   ??? ??  ? ?? ?  ? ???  ?? ?? ? ? ?  ?
        x, y = self.rect.topleft
        # ??????  ???? ? ?  ????  ? ??  ???  ?? ? ?? ??
        tx, ty = body.rect.topleft

        # ??  ? ?? ?     ??????    ??? ????  ? ? ?? ???
        return bool(self.mask.overlap(
            body.mask, (round(tx - x), round(ty - y)))
        )


class Asteroid:
    def __init__(self, image, size, x, y, rot, angle, v):
        self.image = image = pygame.transform.rotozoom(
            image.convert_alpha(), rot, 0.5 + size * 0.5)
        self.rect = image.get_rect(center=(round(x), round(y)))
        self.mask = pygame.mask.from_surface(image)

        self.x = x
        self.y = y
        self.size = size
        self.rot = rot
        self.angle = angle
        self.v = v

        self.givex = self.image.get_width() / 2 + tolerance
        self.givey = self.image.get_height() / 2 + tolerance

    def draw(self, surface, idle):
        if not idle:
            angle = math.radians(self.angle + 90)
            xmult = math.cos(angle)
            ymult = -math.sin(angle)

            width, height = surface.get_size()

            self.x = wrap(self.x, self.v * xmult,
                          width, self.givex, -self.givex)
            self.y = wrap(self.y, self.v * ymult,
                          height, self.givey, -self.givey)

            self.rect.center = (round(self.x), round(self.y))

        surface.blit(self.image, self.rect)

    def colliding(self, thing):
        x, y = self.rect.topleft
        tx, ty = thing.rect.topleft

        return bool(self.mask.overlap(
            thing.mask, (round(tx - x), round(ty - y)))
        )

    def kill(self, body):
        asteroids.remove(self)
        if isinstance(body, Bullet):
            bullets.remove(body)

        if not len(sizes) > self.size:
            sounds[sizes[-1]].play()
        else:
            sounds[sizes[self.size]].play()

        if not self.size > 0:
            return

        rand = random.random
        size = self.size - 1

        for _ in range(2):
            rot = math.floor(rand() * 360)
            angle = math.floor(rand() * 360)
            dpos = 1 + math.floor(rand() * 3)

            list = ast_nfts
            if theindex:
                list = ast_nfts.copy()
                list.pop(theindex)
            img = random.choice(list)

            asteroids.append(Asteroid(
                img, size, self.x, self.y, rot, angle, dpos))
