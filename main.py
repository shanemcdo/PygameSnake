import pygame
from copy import copy
from enum import Enum
from pygame.locals import *
from pygame_tools import *
from random import randrange, choice

class Direction(Enum):
    UP = 'w'
    LEFT = 'a'
    DOWN = 's'
    RIGHT = 'd'

class DeathScreen(MenuScreen):

    def __init__(self, screen: pygame.Surface, real_window_size: Point, window_size: Point, score: int):
        super().__init__(screen, real_window_size, window_size)
        self.play_again = True
        self.button_font = pygame.font.SysFont('Consolas', 13)
        self.sub_window_size = Point(200, 200)
        self.sub_window = pygame.Surface(self.sub_window_size)
        self.button_size = Point(80, 20)
        self.buttons = [
                Button(self.play_again_function, 'Play again?', Rect((10, self.sub_window_size.y - 10 - self.button_size.y), self.button_size), self.button_font),
                Button(self.exit, 'Quit', Rect((self.sub_window_size.x - 10 - self.button_size.x, self.sub_window_size.y - 10 - self.button_size.y), self.button_size), self.button_font)
                ]
        self.sub_window_rect = Rect((0, 0), self.sub_window_size)
        self.sub_window_rect.center = self.window_size.x // 2, self.window_size.y // 2

    def mouse_button_down(self, event: pygame.event.Event):
        if event.button == 1:
            mouse_pos = Point._make(pygame.mouse.get_pos())
            mouse_pos = Point(mouse_pos.x // self.window_scale.x, mouse_pos.y // self.window_scale.y)
            for i, button in enumerate(self.buttons):
                if Rect((button.rect.x + self.sub_window_rect.x, button.rect.y + self.sub_window_rect.y), button.rect.size).collidepoint(mouse_pos):
                    self.button_index = i
                    button()

    def play_again_function(self):
        self.play_again = True
        self.running = False

    def exit(self):
        self.play_again = False
        self.running = False

    def update(self):
        self.sub_window.fill((30, 30, 30))
        self.draw_buttons(self.sub_window)
        self.screen.blit(self.sub_window, self.sub_window_rect)

class PySnake(GameScreen):

    def __init__(self):
        pygame.init()
        real_size = Point(600, 600)
        super().__init__(pygame.display.set_mode(real_size), real_size, Point(real_size.x / 2, real_size.y / 2))
        self.grid_size = Point(20, 20)
        self.cell_size = Point(15, 15)
        self.reset()
        self.head_image = pygame.Surface(self.cell_size)
        self.head_image.fill('#990000')
        self.fruit_image = pygame.Surface(self.cell_size)
        self.fruit_image.fill('#000099')
        self.movement_delay = TrueEvery(5)
        self.score_font = pygame.font.SysFont('Consolas', 10)

    def update(self):
        self.draw_background()
        self.draw_head()
        self.draw_tail()
        self.draw_fruit()
        self.draw_score()
        if self.movement_delay():
            self.move()
            self.update_tail()
            if self.check_collision():
                death_screen = DeathScreen(self.real_screen, self.real_window_size, self.window_size, self.score)
                death_screen.run()
                self.reset()
                self.running = death_screen.play_again
            elif self.check_fruit():
                self.score += 1
                self.length_to_add += 2
                self.fruit = self.new_fruit()

    def key_down(self, event: pygame.event.Event):
        if event.key == K_w:
            self.direction = Direction.UP
        elif event.key == K_a:
            self.direction = Direction.LEFT
        elif event.key == K_s:
            self.direction = Direction.DOWN
        elif event.key == K_d:
            self.direction = Direction.RIGHT

    def reset(self):
        self.head = Point(self.grid_size.x // 2, self.grid_size.y // 2)
        self.previous_head = self.head
        self.tail = []
        self.direction = Direction.UP
        self.length_to_add = 2
        self.score = 0
        self.fruit = self.new_fruit()

    def update_tail(self):
        self.tail.insert(0, self.previous_head)
        if self.length_to_add > 0:
            self.length_to_add -= 1
        else:
            self.tail.pop(-1)

    def draw_background(self):
        self.screen.fill('#008000')
        for i in range(self.grid_size.y):
            for j in range(self.grid_size.x):
                if (i * self.grid_size.x + j + i) % 2:
                    self.screen.fill('#007200', ((j * self.cell_size.x, i * self.cell_size.y), self.cell_size))

    def draw_head(self):
        self.screen.blit(self.head_image, (self.head.x * self.cell_size.x, self.head.y * self.cell_size.y))

    def draw_tail(self):
        for pos in self.tail:
            self.screen.blit(self.head_image, (pos.x * self.cell_size.x, pos.y * self.cell_size.y))

    def draw_fruit(self):
        self.screen.blit(self.fruit_image, (self.fruit.x * self.cell_size.x, self.fruit.y * self.cell_size.y))

    def draw_score(self):
        self.screen.blit(self.score_font.render(f'Score: {self.score}', True, (255, 255, 255)), (2, 2))

    def move(self):
        self.previous_head = copy(self.head)
        if self.direction == Direction.UP:
            self.head.y -= 1
        elif self.direction == Direction.LEFT:
            self.head.x -= 1
        elif self.direction == Direction.DOWN:
            self.head.y += 1
        elif self.direction == Direction.RIGHT:
            self.head.x += 1

    def check_collision(self):
        if self.head.x < 0 or self.head.x >= self.grid_size.x or self.head.y < 0 or self.head.y >= self.grid_size.y or self.head in self.tail:
            return True
        return False

    def random_spot_on_board(self):
        return Point(randrange(0, self.grid_size.x), randrange(0, self.grid_size.y))

    def check_fruit(self):
        return self.fruit == self.head

    def new_fruit(self):
        possible_spots = []
        for i in range(self.grid_size.y):
            for j in range(self.grid_size.x):
                possible_spots.append(Point(j, i))
        possible_spots.remove(self.head)
        for spot in self.tail:
            possible_spots.remove(spot)
        return choice(possible_spots)


if __name__ == '__main__':
    PySnake().run()
