import pygame
import random
import math

import init

screen_w = 960
screen_h = 600

dis = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_icon(pygame.image.load(
    "./assets/ship2.png"))
pygame.display.set_caption("asteroids")

player = init.Player(screen_w // 2, screen_h // 2, 4, 0.15, 0.025, 5, 8)

ast_nfts = init.ast_nfts


a_f = False
a_rl = False
a_rr = False
a_sh = False

sh_c = 0
ast_c = 0


def forward(player):
    global a_f
    if not a_f:
        a_f = True
        player.forward()


def rotate_l(player):
    global a_rl
    global a_rr
    if not a_rl or a_rr:
        a_rl = True
        a_rr = True
        player.rotate_l()


def rotate_r(player):
    global a_rr
    global a_rl
    if not a_rr or a_rl:
        a_rr = True
        a_rl = True
        player.rotate_r()


def shoot(player):
    global a_sh
    global sh_c
    global maxbs
    if not a_sh and sh_c == 0:
        sh_c = 6
        if len(bullets) < maxbs:
            player.shoot()


def reset():
    global a_f
    global a_rl
    global a_rr
    global a_sh
    a_f = False
    a_rl = False
    a_rr = False
    a_sh = False


asteroids = init.asteroids
bullets = init.bullets


def summon():
    global maxasts
    if not len(asteroids) < maxasts:
        return

    rand = random.random

    i = random.randint(0, len(ast_nfts) - 1)
    img = ast_nfts[i]

    size = 1 if init.theindex != None and i == init.theindex else math.floor(
        rand() * 4)
    rot = math.floor(rand() * 360)
    angle = math.floor(rand() * 360)
    dpos = 1 + math.floor(rand() * 3)

    width = img.get_width() / 2
    height = img.get_height() / 2

    x = math.ceil(screen_w + width)
    y = math.ceil(screen_h + height)

    if rand() < width / (width + height):
        x = (width + x) * rand()
        y = y if rand() < 0.5 else y + height
    else:
        x = x if rand() < 0.5 else x + width
        y = y + rand() * height

    asteroids.append(init.Asteroid(
        img, size, x, y, rot, angle, dpos))


def addscore(n, mod, milestone, func):
    m = n % milestone
    if not m + mod < milestone:
        func((m + mod) // milestone)
    return n + mod


def reward(n):
    global lives
    global invincible
    global fps
    init.sounds["life"].play()
    lives += n
    invincible = n * fps


def collided(asteroid):
    body = None
    if asteroid.colliding(player):
        body = player
    else:
        for bullet in bullets.copy():
            if asteroid.colliding(bullet):
                body = bullet
                break

    if not body or player.died:
        return

    if isinstance(body, init.Player) and not invincible:
        global highscore
        global resetin
        global lives
        global score
        global grace
        global ast_c
        global idle
        global fps
        body.kill(asteroid)
        lives -= 1
        if lives:
            idle = fps * 2
            resetin = fps
        else:
            if score > highscore:
                highscore = score
            idle = -1
            ast_c = -1
            grace = round(fps * 1.5)
    elif isinstance(body, init.Bullet):
        score = addscore(score, scoretable[asteroid.size] if len(
            scoretable) > asteroid.size else scoretable[-1], rewardevery, reward)
        asteroid.kill(body)


pressevents = {
    pygame.K_w: forward,
    pygame.K_UP: forward,
    pygame.K_a: rotate_l,
    pygame.K_LEFT: rotate_l,
    pygame.K_d: rotate_r,
    pygame.K_RIGHT: rotate_r,
}

downevents = {
    pygame.K_SPACE: shoot,
    pygame.K_RETURN: shoot,
    pygame.K_KP_ENTER: shoot,
}

began = False
fsize = 20
font = pygame.font.SysFont("monospace", fsize, True)

gameoverfsize = 42
gameoverfont = pygame.font.SysFont("monospace", 42, True)

BACKGROUND_COLOR = (16, 16, 32)
TEXT_COLOR = (224, 224, 224)
TERRIFYING_COLOR = (255, 224, 224)


scoretable = [100, 70, 20, 10]
rewardevery = 8000
harderevery = 200

invincible = 0
resetin = 0
highscore = 0
score = 0

grace = 0

startlives = 3
lives = startlives

fps = 60
maxbs = 4
maxasts = 20

clock = pygame.time.Clock()
defmtime = round(fps * 1.5)
mtime = defmtime

over = False

idletime = 60
idle = idletime
running = True
while running:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT or ev.type == pygame.WINDOWCLOSE:
            running = False
            pygame.quit()
    if not running:
        break

    dis.fill(BACKGROUND_COLOR)
    if not began:
        title = font.render("ASTEROIDS",
                            True, TEXT_COLOR)
        dis.blit(title, title.get_rect(center=(screen_w // 2, screen_h // 4)))

        info = font.render("Press SPACE to play.",
                           True, TEXT_COLOR)
        dis.blit(info, info.get_rect(center=(screen_w // 2, screen_h // 2)))

        controls = font.render("A/D or LEFT/RIGHT to rotate. W or UP to thrust",
                               True, TEXT_COLOR)
        dis.blit(controls, controls.get_rect(
            center=(screen_w // 2, screen_h - screen_h // 4 - screen_h // 16)))

        controls = font.render("SPACE, RETURN or ENTER to shoot",
                               True, TEXT_COLOR)
        dis.blit(controls, controls.get_rect(
            center=(screen_w // 2, screen_h - screen_h // 4)))

        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            began = True
        clock.tick(fps)
        continue

    if not resetin < 0:
        if resetin == 0:
            player.x, player.y = screen_w // 2, screen_h // 2
            player.vx, player.vy = 0, 0
            player.angle = 0
            player.isacc = False
            player.died = False
            invincible = fps * 2
        resetin -= 1

    if sh_c:
        sh_c -= 1

    if not idle > 0:
        if not lives:
            if not over:
                over = True
        else:
            if invincible:
                invinfo = font.render(f"invincible - {round(invincible / fps, 1)}s",
                                      True, TEXT_COLOR)
                dis.blit(invinfo, invinfo.get_rect(
                    midtop=(screen_w // 2, fsize)))
                invincible -= 1

            pressed = pygame.key.get_pressed()
            for k in pressevents:
                if pressed[k]:
                    pressevents[k](player)
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    key = int(ev.key)
                    if key in downevents:
                        downevents[key](player)
            reset()

    if ast_c > 0:
        ast_c -= 1
    elif not over:
        ast_c = fps * 3 - score // harderevery + \
            math.floor(random.random() * (fps * 4 - score // harderevery))
        summon()

    for b in bullets.copy():
        if b.frames >= 60:
            bullets.remove(b)
            continue
        b.draw(dis, idle)

    for a in asteroids.copy():
        if collided(a):
            continue
        a.draw(dis, idle)

    lifeinfo = font.render(f"lives: {lives} | score: {score} | high: {highscore}",
                           True, TEXT_COLOR)
    dis.blit(lifeinfo, lifeinfo.get_rect(
        midtop=(screen_w // 2, 0)))

    player.draw(dis, idle)

    if over:
        gameovertext = gameoverfont.render(
            "GAME OVER", True, TERRIFYING_COLOR)
        dis.blit(gameovertext, gameovertext.get_rect(
            center=(screen_w // 2, screen_h // 2)
        ))

        scoreinfo = font.render(
            f"HIGH SCORE: {highscore}", True, TERRIFYING_COLOR)
        dis.blit(scoreinfo, scoreinfo.get_rect(
            center=(screen_w // 2, screen_h -
                    screen_h // 4 - screen_h // 8)
        ))

        if grace > 0:
            grace -= 1
        else:
            overinfo = font.render(
                "Press SPACE to play again", True, TERRIFYING_COLOR)
            dis.blit(overinfo, overinfo.get_rect(
                center=(screen_w // 2, screen_h - screen_h // 4)
            ))

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                invincible = 0
                resetin = 0
                score = 0

                over = False
                lives = startlives
                idle = idletime

                asteroids.clear()
                bullets.clear()

    if mtime > 0:
        mtime -= 1
        if mtime == 45:
            init.sounds["beat1"].play()
        elif mtime == 0:
            init.sounds["beat2"].play()
    else:
        mtime = defmtime

    if idle > 0:
        idle -= 1

    pygame.display.update()
    clock.tick(fps)
