import pygame 
import random
import time

class Tile:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, dx):
        self.x += dx
    
    def find_optimal_dot(self, ball):
        return max(self.x, min(ball.x, self.x+self.width)), max(self.y, min(ball.y, self.y+self.height))

class Ball:
    def __init__(self, x, y, radius, dx, dy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.color = color
        self.std_dev = 0.3
        self.timer = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self, surface, player, bricks):
        self.x += self.dx
        self.y += self.dy
        self.bounce(surface, player, bricks)

    def bounce(self, surface, player, bricks):
        if self.x+self.radius>surface.get_width() or self.x < self.radius:
            self.dx*=-1
            self.dx +=random.gauss(0, self.std_dev)
        if self.y+self.radius>surface.get_height() or self.y < self.radius:
            self.dy*=-1
            self.dy +=random.gauss(0, self.std_dev)
        self.tile_collision(player)
        for brick in bricks:
            if brick.visible:
                self.tile_collision(brick)


    def tile_collision(self, other):
        optimal_x, optimal_y = other.find_optimal_dot(self)

        if self.isPointInCircle(optimal_x, optimal_y):
            if optimal_x == other.x or optimal_x==other.x + other.width:
                self.dx*=-1
                self.dx +=random.gauss(0, self.std_dev)
                if isinstance(other, Brick):
                    other.visible = False
            
            if optimal_y == other.y or optimal_y==other.y + other.height:
                self.dy*=-1
                self.dy +=random.gauss(0, self.std_dev)
                if isinstance(other, Brick):
                    other.visible = False


    def isPointInCircle(self, point_x, point_y):
        return (point_x-self.x)**2+(point_y-self.y)**2<self.radius**2

    def checkLives(self, surface):
        eps = 5
        curr_time = time.time()
        dt = curr_time-self.timer
        if self.y + self.radius >= surface.get_height()-eps and dt>2:
            self.timer = curr_time
            return True
        return False
        


class Brick:
    def __init__(self, x, y, width, heigth, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.color = color
        self.visible = True

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height)) 
    
    def find_optimal_dot(self, ball):
        return max(self.x, min(ball.x, self.x+self.width)), max(self.y, min(ball.y, self.y+self.height))




pygame.init()

screen_w = 800
screen_h = 600

dis = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption('Breakout')
game_over = False

BLACK = (0,0,0)
WHITE = (255,255,255)
BALL_TILE_COLOR = (94,119,3)
BACKGROUND_COLOR = (201, 201, 201)


tile_w = 100
tile_h = 20
player = Tile(screen_w//2-tile_w//2, screen_h-50, tile_w, tile_h, BALL_TILE_COLOR)

rand_dx = random.random()
rand_dy = random.random()
ball_r = 20
ball = Ball(screen_w//2, screen_h//2, ball_r, rand_dx, rand_dy, BALL_TILE_COLOR)

step_x = screen_w // 16
step_y = screen_h //20
brick_size = 20

bricks = []

brick_colors = [(239, 62, 91), (75, 37, 109), (63,100,126)]
for i in range(-4, 5):
    for j in range(1, 4):
        curr_brick = Brick(screen_w//2+i*step_x, j*step_y, brick_size, brick_size, brick_colors[j-1])
        bricks.append(curr_brick)

lives = 1
font = pygame.font.Font('freesansbold.ttf', 20)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            pygame.quit()


    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_RIGHT]:
        player.move(2)
    if keys_pressed[pygame.K_LEFT]:
        player.move(-2)

    ball.move(dis, player, bricks)
    if ball.checkLives(dis):
        lives-=1


    if lives==0:
        game_over = True


    text = font.render(f"Lives: {lives}", True, BLACK, BACKGROUND_COLOR)


    if player.x<0:
        player.x = 0
    if player.x+player.width > screen_w:
        player.x = screen_w-player.width

    dis.fill(BACKGROUND_COLOR)
    player.draw(dis)
    ball.draw(dis)
    dis.blit(text, (screen_w-100, 50))

    for brick in bricks:
        brick.draw(dis)


    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            pygame.quit()
    dis.fill(BLACK)
    text = font.render("GAME OVER", True, WHITE, BLACK)
    dis.blit(text, (screen_w//2-100, screen_h//2))
    pygame.display.update()
    
