import pygame
import random

pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 10, 0)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNEK")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.direction = 'right'
        self.speed = 1
        self.size = 50
        self.tail_blocks = None

    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.size, self.size), 2)
        if self.tail_blocks is not None:
            for tail in self.tail_blocks:
                pygame.draw.rect(window, WHITE, (tail.x, tail.y, self.size, self.size))
                pygame.draw.rect(window, BLACK, (tail.x, tail.y, self.size, self.size),2)

    def update(self):
        if self.tail_blocks is not None:
            for i in range(len(self.tail_blocks)-1, 0, -1):
                self.tail_blocks[i].x = self.tail_blocks[i-1].x
                self.tail_blocks[i].y = self.tail_blocks[i-1].y
            self.tail_blocks[0].x = self.x
            self.tail_blocks[0].y = self.y

        if self.direction == 'right':
            self.x += self.speed * self.size
        elif self.direction == 'left':
            self.x -= self.speed * self.size
        elif self.direction == 'down':
            self.y += self.speed * self.size
        else:
            self.y -= self.speed * self.size

    def is_out(self):
        if self.x < 0 or self.x > SCREEN_WIDTH - self.size:
            return True
        if self.y < 0 or self.y > SCREEN_HEIGHT - self.size:
            return True
        return False

    def self_collision(self):
        if self.tail_blocks is not None:
            for tail in self.tail_blocks:
                if tail.x == self.x and tail.y == self.y:
                    return True
            return False

    def grow(self):
        if self.tail_blocks is None:
            self.tail_blocks = [(Tail(self.x, self.y))]
        else:
            last = self.tail_blocks[len(self.tail_blocks)-1]
            self.tail_blocks.append(Tail(last.x, last.y))

class Tail:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

class Apple:
    def __init__(self):
        self.x = 800
        self.y = 200
        self.size = 50

    def draw(self):
        pygame.draw.rect(window,RED,(self.x, self.y, self.size, self.size))

    def update(self):
        self.x = random.randint(1,25) * 50
        self.y = random.randint(1, 14) * 50


    def collision(self, snake):
        if self.x == snake.x and self.y == snake.y:
            return True
        return False


snek = Snake()
apko = Apple()
next_move = 'right'
timer = 0
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if snek.direction != 'left':
                    next_move = 'right'
            if event.key == pygame.K_LEFT:
                if snek.direction != 'right':
                    next_move = 'left'
            if event.key == pygame.K_DOWN:
                if snek.direction != 'up':
                    next_move = 'down'
            if event.key == pygame.K_UP:
                if snek.direction != 'down':
                    next_move = 'up'

    timer += 1

    window.fill(BLACK)
    if timer == 10:
        snek.direction = next_move
        snek.update()
        if snek.x < 0 or snek.x > SCREEN_WIDTH:
            running = False
        if snek.is_out() or snek.self_collision():
            running = False
            break
        if apko.collision(snek):
            snek.grow()
            apko.update()
        timer = 0
    apko.draw()
    snek.draw()
    pygame.display.flip()

pygame.quit()