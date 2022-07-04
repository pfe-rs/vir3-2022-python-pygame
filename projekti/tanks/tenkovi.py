#sa ponosom vam predstavljam 
# Worms: Reloaded: bad python version

from math import dist
import math
from time import sleep
import pygame;
import numpy as np;

pygame.init();
scrw = 800;
scrh = 600;
bsize = 32; #ima manjih problema ako se ovo promeni tako da preporucujem da se ne menja (nista ne radi)

class Tenkic:
    def __init__(self, pos, color):
        self.x, self.y = pos;
        self.color = color;
        self.lives = 3;
        self.cent = (self.x + 15, self.y + 5);

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, 20, 10));

    def findSurrBlocks(self, ground):
        self.cent = (self.x + 15, self.y + 5);
        pos_x = self.cent[0] // bsize;
        b_under = ground.blocks[pos_x][ground.layout[pos_x] - 1]
        # return b_under;
        pos_y = (scrh - self.cent[1]) // bsize;
        if pos_x == 0 or pos_y >= ground.layout[pos_x - 1]: b_left = None
        else: b_left = ground.blocks[pos_x - 1][pos_y - 1]
        if pos_x == 24 or pos_y >= ground.layout[pos_x + 1]: b_right = None
        else: b_right = ground.blocks[pos_x + 1][pos_y - 1]

        return b_under, b_left, b_right;
        

    def najblizaTacka(self, djule):
        return max(self.x, min(djule.x, self.x + 30)), max(self.y, min(djule.y, self.y + 10));

    def move(self, dx):
        self.x += dx;
        
    def fall(self, ground, vy = 3):
        b_under, b_left, b_right = self.findSurrBlocks(ground);
        if b_left is not None and self.x < b_left.x + bsize:
            self.x = b_left.x + bsize;
        if b_right is not None and self.x > b_right.x - 20:
            self.x = b_right.x - 20;
        if self.y + 10 < b_under.y:
            self.vy = vy;
            self.y += self.vy;
            self.vy += g;


class Djule:
    def __init__(self, pos, vx, vy):
        self.x, self.y = pos;
        self.r = 5;
        self.vx = vx;
        self.vy = vy;
        self.hit = 0;
        self.color = (0, 0, 0)

    def moveHor(self):
        self.x += self.vx;

    def moveVert(self, g):
        self.y -= self.vy;
        self.vy -= g;

    def findClosestBlock(self, ground):
        closest_block = None;
        min_dist = 800;
        for i in range(ground.len):
            for j in range(ground.layout[i]):
                if dist((self.x, self.y), ground.blocks[i][j].cent) < min_dist:
                    closest_block = (i, j);
                    min_dist = dist((self.x, self.y), ground.blocks[i][j].cent)
        return closest_block;

    def collideGround(self, ground):
        if self.x >= scrw - self.r or self.x <= self.r:
            self.vx = -self.vx
    
        closest_block_coords = self.findClosestBlock(ground);

        if closest_block_coords == None: return;

        i, j = closest_block_coords;
        closest_block = ground.blocks[i][j]
        closest_point = closest_block.najblizaTacka(self);

        if abs(dist(closest_point, (self.x, self.y))) < self.r:
            if j > 1:
                for k in range(j, ground.layout[i]):
                    ground.blocks[i][k] = 0;
                ground.layout[i] = j;
            return True;
        else: return False;

    def tankCollision(self, t34):
        if abs(dist((self.x, self.y), t34.najblizaTacka(self))) <= self.r:
            return True;
        else: return False;
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r);


class ground:
    def __init__(self, maxh, minh, bsize, color):
        self.maxh = maxh;
        self.minh = minh;
        self.bsize = bsize;
        self.color = color;
        self.color_unbreakable = (127, 127, 127);
        self.len = scrw // self.bsize;

    class groundBlock:
        def __init__(self, pos, size):
            self.x, self.y = pos;
            self.size = size;
            self.cent = (self.x + self.size // 2, self.y + self.size // 2)

        def najblizaTacka(self, djule):
            return max(self.x, min(djule.x, self.x + self.size)), max(self.y, min(djule.y, self.y + self.size));

    def generate(self):
        self.layout = np.zeros(self.len, int);
        self.layout[0] = self.maxh;
        self.layout[self.len - 1] = self.maxh;
        for i in range(1, self.len - 1):
            self.layout[i] = int(np.random.uniform(self.minh, self.maxh));
        self.blocks = np.zeros((self.len, self.maxh), self.groundBlock);
        x = 0;
        y = scrh - self.bsize;
        for i in range(self.len):
            for j in range(self.layout[i]):
                self.blocks[i][j] = self.groundBlock((x, y), self.bsize);
                y -= self.bsize;
            x += self.bsize;
            y = scrh - self.bsize;

    def draw(self, surf):
        for i in range(self.len):
            for j in range(self.layout[i]):
                if j < 2:
                    pygame.draw.rect(surf, self.color_unbreakable, (self.blocks[i][j].x, self.blocks[i][j].y, self.bsize, self.bsize));
                else:
                    pygame.draw.rect(surf, self.color, (self.blocks[i][j].x, self.blocks[i][j].y, self.bsize, self.bsize));

bipovi = [];
bipovi.append(pygame.mixer.Sound('./assets/beep-02.wav'));  

boop = pygame.mixer.Sound('./assets/beep-03.wav');

dis = pygame.display.set_mode((scrw, scrh));
pygame.display.set_caption('Wroms: MS-DOS Edition');
fnt = pygame.font.Font('./assets/upheavtt.ttf', 32);


tlo = ground(9, 4, bsize, (100, 255, 100));
tlo.generate();
tenkovi = [];
zivoti = [];
tenkovi.append(Tenkic((tlo.blocks[0][len(tlo.blocks[0]) - 1].x, tlo.blocks[0][len(tlo.blocks[0]) - 1].y - 10), (255, 0, 0)));
tenkovi.append(Tenkic((tlo.blocks[len(tlo.blocks) - 1][len(tlo.blocks[0]) - 1].x, tlo.blocks[0][len(tlo.blocks[0]) - 1].y - 10), (0, 0, 255)));

djule = None;
theta = np.pi/4;
pow = 1;
igrac_na_redu = 1;
g = 0.0015
while tenkovi[0].lives > 0 and tenkovi[1].lives > 0:
    
    i = igrac_na_redu / 2 + 0.5;
    i = int(i);
    protivnik = (i + 1) % 2;
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            pygame.quit()

    dis.fill((127, 127, 255));
    tlo.draw(dis);
    for tenk in tenkovi:
        tenk.draw(dis);

    key = pygame.key.get_pressed();
    if key[pygame.K_d] and tenkovi[i].x < scrw - 30:
        tenkovi[i].move(4);
    elif key[pygame.K_a] and tenkovi[i].x > 0:
        tenkovi[i].move(-4);
    elif key[pygame.K_w]:
        if pow < 1.5:
            pow += .004;
    elif key[pygame.K_s]:
        if pow > 1:
            pow -= .004;
    elif key[pygame.K_UP]:
        if theta < np.pi:
            theta += 0.001 * t;
    elif key[pygame.K_DOWN]:
        if theta > 0:
            theta -= 0.001 * t;
    elif key[pygame.K_SPACE]:
        if djule is None:
            djule = Djule((tenkovi[i].x + 15, tenkovi[i].y - 5), -igrac_na_redu * pow * np.cos(theta) * t, pow * np.sin(theta) * t);
            bipovi[0].play(maxtime = 100);
        elif djule.hit > 0:
            djule = None
            igrac_na_redu *= -1;
    tenkovi[0].fall(tlo);
    tenkovi[1].fall(tlo);

    powtext = fnt.render('POW: ' + str(int((pow - 0.99) * 100)), False, (255, 255, 255));
    powtxtrect = powtext.get_rect();
    powtxtrect.center = (scrw / 2, scrh * 5 // 6);
    dis.blit(powtext, powtxtrect);

    angtext = fnt.render('DEG: ' + str(int(math.degrees(theta))) + '°', False, (255, 255, 255));
    angtextrect = angtext.get_rect();
    angtextrect.center = (scrw / 2, scrh * 5 // 6 + 34);
    dis.blit(angtext, angtextrect);

    livesred = fnt.render('O' * tenkovi[0].lives, False, (255, 0, 0));
    livesredrect = livesred.get_rect();
    livesredrect.center = (livesredrect.width // 2, scrh - livesredrect.height // 2);
    dis.blit(livesred, livesredrect);

    livesblue = fnt.render('O' * tenkovi[1].lives, False, (0, 0, 255));
    livesbluerect = livesblue.get_rect();
    livesbluerect.center = (scrw - livesbluerect.width // 2, scrh - livesbluerect.height // 2);
    dis.blit(livesblue, livesbluerect);

    if djule is not None:
        djule.draw(dis);
        djule.moveHor();
        djule.moveVert(g * t * t);
        if djule.tankCollision(tenkovi[protivnik]):
            tenkovi[protivnik].lives -= 1;
            djule = None;
            igrac_na_redu *= -1;
            boop.play(); 
        elif djule.collideGround(tlo):
            djule.hit += 1;
            djule.vx = 0;
            igrac_na_redu *= -1;
            djule = None;
            sleep(0.1);

    pygame.display.update();
    t = pygame.time.Clock().tick(60);
    t = (t // 2) * 2
    # print(t);

if tenkovi[0].lives > tenkovi[1].lives:
    txt = 'Teror crvene armije se nastavlja';
    txt_color = (255, 0, 0);
else:
    txt = 'Plava armija odnosi odlucujucu pobedu'
    txt_color = (127, 127, 255)

alpha = 255;

while alpha > 0:
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            pygame.quit()

    end_text = fnt.render(txt, False, txt_color);
    end_rect = end_text.get_rect();
    end_rect.center = (scrw // 2, scrh // 2);
    end_text.set_alpha(alpha);
    alpha -= 10;
    sleep(0.1)
    

    dis.fill((0, 0, 0));
    dis.blit(end_text, end_rect)
    pygame.display.update();