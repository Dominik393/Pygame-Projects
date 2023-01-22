import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

# Używane kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 0, 10)
BLUE = (10, 40, 230)
GREEN = (0, 230, 90)

# Deklaracja zmiennych odpowiadających za okienko
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
circles_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
circles_screen.set_colorkey(BLACK)
trail_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
trail_screen.set_colorkey(BLACK)
pygame.display.set_caption("Fourier Series")

class Circle:
    def __init__(self, radius, position, color, speed = 1, offset = 0):
        self.radius = radius
        self.position = [position[0], position[1]]
        self.color = color
        self.speed = speed
        self.point_pos = [position[0] + radius, position[1] + radius]
        self.offset = offset
        self.time = offset
        self.last_point_pos = [position[0], position[1]]
        self.scale = 1

    def update(self):
        self.time += 0.001 * self.speed
        self.last_point_pos = [self.point_pos[0], self.point_pos[1]]
        self.point_pos[0]= self.position[0] + self.radius*math.cos(self.time)
        self.point_pos[1] = self.position[1] + self.radius*math.sin(self.time)


    def draw(self, color = RED, pointless = False):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)
        #pygame.draw.line(screen, self.color, self.position, self.point_pos)
        if not pointless:
            pygame.draw.line(trail_screen, color, self.last_point_pos, self.point_pos, 3)
            pygame.draw.circle(screen, WHITE, self.point_pos, 6)


class Chain:
    def __init__(self, circles, color = RED, scale = 1):
        self.circles = circles
        self.color = color
        self.scale = scale

    def update(self):
        self.circles[0].update()
        for i in range(1,len(self.circles)):
            self.circles[i].position = self.circles[i-1].point_pos
            self.circles[i].update()

    def draw(self):
        for i in range(len(self.circles)-1):
            self.circles[i].draw(self.color, True)
        self.circles[len(self.circles)-1].draw(self.color)

    def reset(self):
        for i in range(len(self.circles)):
            self.circles[i].time = self.circles[i].offset


class Button:
    def __init__(self, position, size, color, text="", font=("Arial",32)):
        self.position = position
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(font[0],font[1])
        self.text = text

    def draw(self, color = None):
        if color is None:
            color = self.color
        pygame.draw.rect(screen, color, [self.position[0], self.position[1], self.size[0], self.size[1]])
        middle = (self.position[0]+self.size[0]/2-self.font.size(self.text)[0]/2, self.position[1]+self.size[1]/2-self.font.size(self.text)[1]/2)
        screen.blit(self.font.render(self.text, True, WHITE), middle)

    def check(self):
        if self.position[0] <= mouse[0] <= self.position[0] + self.size[0] and self.position[1] <= mouse[1] <= self.position[1] + self.size[1]:
            return True
        return False


def clear(chain):
    screen.fill(BLACK)
    trail_screen.fill(BLACK)
    chain.reset()


running = True
time = 0
kolo = Circle(150, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), WHITE, 10)
kolko = Circle(80, (0,0),WHITE, 12)
koleczko = Circle(40,(0,0), WHITE, 24)
lancuch = Chain([kolo,kolko,koleczko], GREEN)


kwadrat = Circle(150, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), WHITE, 20)
kwadrat2 = Circle(150, (0,0), WHITE, -20)
kwadrat3 = Circle(15, (0,0), WHITE, 6)
kwadratuch = Chain([kwadrat,kwadrat2], BLUE)


n=20
kola = [Circle(5*n-5*x,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),WHITE,random.randint(-12,12), random.randint(0,12)) for x in range(n)]
lancuszek = Chain(kola, GREEN)

przycisk = Button((SCREEN_WIDTH-155,SCREEN_HEIGHT-55), (130,40), GREEN, "RESET",("Helvetica", 35))

right_bottom = [0,0]

chain = lancuszek
last_element = len(chain.circles)-1
chain.update()
while running:
    clock.tick()
    mouse = pygame.mouse.get_pos()

    # Żeby dało się zamknąć
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if przycisk.check():
                clear(chain)
                chain.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                clear(chain)
                chain.update()


    right_bottom[0] = max(right_bottom[0], chain.circles[last_element].point_pos[0]+5)
    right_bottom[1] = max(right_bottom[1], chain.circles[last_element].point_pos[1]+5)



    screen.fill(BLACK)
    screen.blit(trail_screen, (0,0), (0,0, right_bottom[0],right_bottom[1]))
    chain.update()
    chain.draw()

    if przycisk.check():
        przycisk.draw()
    else:
        przycisk.draw(RED)


    # To aktualizuje obraz
    print(clock.get_fps())
    pygame.display.flip()


pygame.quit()