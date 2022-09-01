import pygame
import math
import random
wScreen = 800
hScreen = 600

dis = pygame.display.set_mode((wScreen,hScreen))
pygame.display.set_caption('Projectile Motion')
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

class Tile:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    
    def find_optimal_dot(self, ball):
        return max(self.x, min(ball.x, self.x+self.width)), max(self.y, min(ball.y, self.y+self.height))
class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(dis, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(dis, self.color, (self.x,self.y), self.radius-1)


    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        angle = ang
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)


        return (newx, newy)
        
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
    def colTIle():
        for brick in bricks:
            if brick.visible:
                golfBall.tile_collision(brick)

    def bounce(startx,starty,ang,time,power):
        if startx>=762 and starty>=250 :
            if pos[1] > golfBall.y:
                angle = (math.pi * 2) - angle
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

                distX = velx * time
                distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                newx = round(distX - startx)
                newy = round(starty - distY)
                
            elif pos[1] < golfBall.y:
                angle = (math.pi * 2) - angle
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

                distX = velx * time
                distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                newx = round(distX + startx)
                newy = round(starty + distY)
                
        if startx>=762 and starty>=250 and startx<=472:
            if  pos[0] < golfBall.x:
                angle = (math.pi * 2) - angle
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

                distX = velx * time
                distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                newx = round(distX - startx)
                newy = round(starty - distY)
                
            elif pos[0] < golfBall.x:
                angle = math.pi + abs(angle)
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

                distX = velx * time
                distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                newx = round(distX + startx)
                newy = round(starty + distY)
                
            if starty>=250 and startx<=472:
                if  pos[0] < golfBall.x:
                    angle = (math.pi * 2) - angle
                    velx = math.cos(angle) * power
                    vely = math.sin(angle) * power

                    distX = velx * time
                    distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                    newx = round(distX - startx)
                    newy = round(starty - distY)
                    
            elif pos[0] < golfBall.x:
                angle = math.pi + abs(angle)
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

                distX = velx * time
                distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

                newx = round(distX + startx)
                newy = round(starty + distY)
                
        return(newx,newy)



def redrawWindow():
    dis.fill((255,255,255))
    golfBall.draw(dis)
    zid1.draw(dis)
    zid2.draw(dis)
    zid3.draw(dis)
    pygame.draw.line(dis,(0,0,0),line[0],line[1])
    for brick in bricks:
        brick.draw(dis)
    pygame.display.update() 

def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    

    return angle


golfBall = ball(300,494,5,(0,0,0))
BLACK = (0,0,0)
WHITE = (255,255,255)
BALL_TILE_COLOR = (94,119,3)
BACKGROUND_COLOR = (255, 255, 255)
run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
zid1 = Tile(767, 255, 10, 300, BLACK)
zid2 = Tile(467, 551, 310, 10, BLACK)
zid3 = Tile(467, 255, 10, 300, BLACK)
step_x = wScreen // 16
step_y = hScreen //20
brick_size = 20

bricks = []
rect=Tile(1,1,5,5,BLACK)
brick_colors = [(239, 62, 91), (75, 37, 109), (63,100,126),(209, 42, 81),(63,50,126),(129, 32, 21)]
for i in range(-1, 5):
    for j in range(1, 7):
        curr_brick = Brick(539+i*step_x,320 + j*step_y, brick_size, brick_size, brick_colors[j-1])
        bricks.append(curr_brick)
while run:
    clock.tick(200)
    if shoot:
        if golfBall.y < 600 - golfBall.radius:
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]
        else:
            shoot = False
            time = 0
            run=False

    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = golfBall.x
                y = golfBall.y
                pos =pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/6
                angle = findAngle(pos)
                if pos[1] < golfBall.y and pos[0] > golfBall.x:
                    angle = abs(angle)
                elif pos[1] < golfBall.y and pos[0] < golfBall.x:
                     angle = math.pi - angle
                elif pos[1] > golfBall.y and pos[0] < golfBall.x:
                    angle = math.pi + abs(angle)
                elif pos[1] > golfBall.y and pos[0] > golfBall.x:
                    angle = (math.pi * 2) - angle
    ball.colTIle()

    #if golfBall.x>460:
      #  po=ball.bounce(golfBall.x,golfBall.y,angle,time,power)
       # golfBall.x = po[0]
        #golfBall.y = po[1]

       
    #collide1 = pygame.Rect.colliderect(zid2,zid1)
    #if collide1:
     #   print('ide')



pygame.quit()
quit()