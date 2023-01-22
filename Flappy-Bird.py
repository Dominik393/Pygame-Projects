import pygame
import random

pygame.init()
SCREEN_WIDTH = 920
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (50, 190, 255)
GREEN = (0, 210, 0)
YELLOW = (200, 200, 50)

class Bird:
    def __init__(self):
        self.y = SCREEN_HEIGHT/2
        self.x = 100
        self.velocity = 0
        self.gravity = 0.25
        self.lift = -8
        self.radius = 40

    def draw(self):
        pygame.draw.circle(window, YELLOW, (self.x,self.y), self.radius)
        pygame.draw.circle(window, BLACK, (self.x, self.y), self.radius, 2)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0

    def flap(self):
        self.velocity = self.lift


class Pipe:
    def __init__(self):
        self.gap = 245
        self.width = 70
        self.y = random.randint(SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200)
        self.x = SCREEN_WIDTH
        self.speed = 3

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
            self.y = random.randint(SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200)

    def draw(self):
        pygame.draw.rect(window, GREEN, (self.x,0,self.width,self.y - self.gap/2))
        pygame.draw.rect(window, BLACK, (self.x, 0, self.width, self.y - self.gap / 2), 2)
        pygame.draw.rect(window, GREEN, (self.x,self.y + self.gap/2, self.width, SCREEN_HEIGHT/2 + 200))
        pygame.draw.rect(window, BLACK, (self.x, self.y + self.gap / 2, self.width, SCREEN_HEIGHT / 2 + 200), 2)

    def collision(self, bird):
        margin_of_error = 0.85
        if self.x <= bird.x + bird.radius*margin_of_error and bird.x - bird.radius*margin_of_error <= self.x + self.width:
            if self.y - self.gap/2 >= bird.y - bird.radius*margin_of_error or bird.y + bird.radius*margin_of_error >= self.y + self.gap/2:
                return True
        return False


def Game_Update(screen, bird, pipes):
    screen.fill(BLUE)
    bird.update()
    bird.draw()
    for pipe in pipes:
        pipe.update()
        if pipe.collision(bird):
            return False
        pipe.draw()
    pygame.display.flip()
    return True

def Game_Restart(bird, pipes):
    bird.y = SCREEN_HEIGHT/2
    bird.velocity = 0

    pipes[0].x = SCREEN_WIDTH
    pipes[1].x = SCREEN_WIDTH*(1.33) + 40
    pipes[2].x = SCREEN_WIDTH*(1.66) + 80



def main():
    bird = Bird()
    pipe1 = Pipe()
    pipe2 = Pipe()
    pipe2.x = SCREEN_WIDTH*1.33 + 40
    pipe3 = Pipe()
    pipe3.x = SCREEN_WIDTH*1.66 + 80
    running = True
    game_loop = True
    while running:
        while game_loop:
            clock.tick(60)
            game_loop = Game_Update(window, bird, [pipe1, pipe2, pipe3])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()

            print(clock.get_fps())
        #   END OF GAME_LOOP

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Game_Restart(bird, [pipe1, pipe2, pipe3])
                    game_loop = True

    pygame.quit()

if __name__ == "__main__":
    main()
