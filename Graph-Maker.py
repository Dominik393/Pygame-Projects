import math
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# Używane kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 0, 10)
BLUE = (10, 40, 230)
GREEN = (0, 230, 90)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Graph Maker")

class Point:
    def __init__(self, position, size = 7, color = WHITE):
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.color = color
        self.scale = 1

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)

    def check(self):
        if self.x - self.size <= mouse[0] <= self.x + self.size and self.y - self.size <= mouse[1] <= self.y + self.size:
            return True
        return False


class Graph:
    def __init__(self, points, connections = None, scale = 1):
        self.points = [point for point in points]
        self.connections = [conn for conn in connections]
        self.scale = scale

    def draw(self):
        if self.connections is not None:
            for conn in self.connections:
                pygame.draw.line(screen,WHITE,(self.points[conn[0]].x, self.points[conn[0]].y),(self.points[conn[1]].x, self.points[conn[1]].y))

        for i in range(len(self.points)):
            self.points[i].draw()


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

def generate_random_graph(no_points):
    points = [Point([random.randint(1, SCREEN_WIDTH/10 -10)*10, random.randint(1, SCREEN_HEIGHT/10 -10)*10]) for _ in range(no_points)]
    no_conn = random.randint(0,no_points*(no_points-1)/2)
    connections = []
    for i in range(no_conn):
        pair = [random.randint(0,no_points-1), random.randint(0,no_points-1)]
        while pair in connections or [pair[1],pair[0]] in connections or pair[0] == pair[1]:
            pair = [random.randint(0,no_points-1), random.randint(0,no_points-1)]
        connections.append(pair)

    return Graph(points,connections)

def generate_polygon(no_vert, size = 100):
    points = [Point([SCREEN_WIDTH/2 + size*math.cos((2*math.pi/no_vert)*i) ,SCREEN_HEIGHT/2 + size*math.sin((2*math.pi/no_vert)*i)]) for i in range(no_vert)]
    connections = [[i, i+1] for i in range(no_vert-1)]
    connections.append([0,no_vert-1])

    return Graph(points,connections)

def screen_update():
    screen.fill(BLACK)
    current_graph.draw()
    przycisk.draw()
    pygame.display.flip()


punkt1 = Point((700,400))
punkt2 = Point((200,400))
punkt3 = Point((300,200))
punkt4 = Point((700,100))

graf = Graph([punkt1,punkt2,punkt3,punkt4], [(1,2),(1,0),(1,3)])
grafik = generate_random_graph(100)

n = 6
poligon = generate_polygon(n, 300)

przycisk = Button((SCREEN_WIDTH-250, SCREEN_HEIGHT-100),(200,50),GREEN,"Zwiększ")

current_graph = poligon
holding = False
already_checked = False
id_of_held_point = -1
running = True
current_graph.draw()
przycisk.draw()
pygame.display.flip()
while running:
    clock.tick()
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding = True
            if przycisk.check():
                n+=1
                current_graph = generate_polygon(n,300)
                screen_update()
        if event.type == pygame.MOUSEBUTTONUP:
            holding = False
            already_checked = False

    if holding and not already_checked:
        for i in range(len(current_graph.points)):
            if current_graph.points[i].check():
                id_of_held_point = i
                already_checked = True

    if already_checked:
        current_graph.points[id_of_held_point].x = mouse[0]
        current_graph.points[id_of_held_point].y = mouse[1]
        screen_update()


pygame.quit()
