import pygame
from enum import Enum
from pygame.locals import *
from pygame_tools import *
from random import randrange

class Direction(Enum):
    UP = 'w'
    LEFT = 'a'
    DOWN = 's'
    RIGHT = 'd'

class PySnake(GameScreen):

    def __init__(self):
        pygame.init()
        real_size = Point(600, 600)
        super().__init__(pygame.display.set_mode(real_size), real_size, Point(real_size.x / 2, real_size.y / 2))
        self.grid_size = Point(20, 20)
        self.cell_size = Point(15, 15)
        self.head = Point(self.grid_size.x // 2, self.grid_size.y // 2)
        self.direction = Direction.UP
        self.length = 0
        self.fruit = self.random_spot_on_board()
        self.head_image = pygame.Surface(self.cell_size)
        self.head_image.fill('blue')
        self.movement_delay = TrueEvery(5)

    def update(self):
        self.draw_background()
        self.draw_head()
        if self.movement_delay():
            self.move()

    def key_down(self, event: pygame.event.Event):
        if event.key == K_w:
            self.direction = Direction.UP
        elif event.key == K_a:
            self.direction = Direction.LEFT
        elif event.key == K_s:
            self.direction = Direction.DOWN
        elif event.key == K_d:
            self.direction = Direction.RIGHT

    def draw_background(self):
        self.screen.fill('#008000')
        for i in range(self.grid_size.y):
            for j in range(self.grid_size.x):
                if (i * self.grid_size.x + j + i) % 2:
                    self.screen.fill('#007200', ((j * self.cell_size.x, i * self.cell_size.y), self.cell_size))

    def draw_head(self):
        self.screen.blit(self.head_image, (self.head.x * self.cell_size.x, self.head.y * self.cell_size.y))

    def move(self):
        if self.direction == Direction.UP:
            self.head.y -= 1
        elif self.direction == Direction.LEFT:
            self.head.x -= 1
        elif self.direction == Direction.DOWN:
            self.head.y += 1
        elif self.direction == Direction.RIGHT:
            self.head.x += 1

    def random_spot_on_board(self):
        return Point(randrange(0, self.grid_size.x), randrange(0, self.grid_size.y))

if __name__ == '__main__':
    PySnake().run()
