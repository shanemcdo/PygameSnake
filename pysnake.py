import pygame
from copy import copy
from enum import Enum
from pygame.locals import *
from pygame_tools import *
from random import randrange, choice

class Direction(Enum):
    UP = 0
    LEFT = 270
    DOWN = 180
    RIGHT = 90

class DeathScreen(MenuScreen):

    def __init__(self, screen: pygame.Surface, game_screen: pygame.Surface, real_window_size: Point, window_size: Point, score: int):
        super().__init__(screen, real_window_size, window_size)
        self.screen = game_screen
        self.button_font = pygame.font.SysFont('Consolas', 13)
        self.sub_window_size = Point(200, 100)
        self.sub_window = pygame.Surface(self.sub_window_size, flags = SRCALPHA)
        self.button_size = Point(85, 20)
        self.buttons = [
                Button(self.play_again, 'Play again?', Rect((10, self.sub_window_size.y - 10 - self.button_size.y), self.button_size), self.button_font, border_radius = 8, border_size = 1),
                Button(sys.exit, 'Quit', Rect((self.sub_window_size.x - 10 - self.button_size.x, self.sub_window_size.y - 10 - self.button_size.y), self.button_size), self.button_font, border_radius = 8, border_size = 1)
                ]
        self.sub_window_rect = Rect((0, 0), self.sub_window_size)
        self.title_text = pygame.font.SysFont('Consolas', 24).render('You Died!', True, (255, 255, 255))
        self.title_pos = Point(self.sub_window_rect.centerx - self.title_text.get_width() / 2, self.sub_window_rect.top + 10)
        self.sub_title_text = pygame.font.SysFont('Consolas', 20).render(f'score: {score}', True, (255, 255, 255))
        self.sub_title_pos = Point(self.sub_window_rect.centerx - self.sub_title_text.get_width() / 2, self.sub_window_rect.top + 40)
        self.sub_window_rect.center = self.window_size.x // 2, self.window_size.y // 2

    def mouse_button_down(self, event: pygame.event.Event):
        if event.button == 1:
            mouse_pos = Point._make(pygame.mouse.get_pos())
            mouse_pos = Point(mouse_pos.x // self.window_scale.x, mouse_pos.y // self.window_scale.y)
            for i, button in enumerate(self.buttons):
                if Rect((button.rect.x + self.sub_window_rect.x, button.rect.y + self.sub_window_rect.y), button.rect.size).collidepoint(mouse_pos):
                    self.button_index = i
                    button()

    def play_again(self):
        self.running = False

    def update(self):
        self.draw_buttons(self.sub_window)
        self.sub_window.blit(self.title_text, self.title_pos)
        self.sub_window.blit(self.sub_title_text, self.sub_title_pos)
        self.screen.blit(self.sub_window, self.sub_window_rect)

class MainMenu(MenuScreen):

    def __init__(self):
        pygame.init()
        real_size = Point(600, 600)
        pygame.display.set_icon(pygame.image.load('assets/logo.png'))
        super().__init__(pygame.display.set_mode(real_size), real_size, Point(real_size.x / 2, real_size.y / 2))
        self.background = pygame.image.load('assets/background.png')
        self.game = PySnake(self)
        font = pygame.font.SysFont('consolas', 25)
        self.buttons = [
                Button(self.game.run, 'Start', Rect(20, 230, 120, 50), font, highlight_color = None, border_size = 2, border_radius = 20),
                Button(sys.exit, 'Exit', Rect(160, 230, 120, 50), font, highlight_color = None, border_size = 2, border_radius = 20),
                ]

    def update(self):
        self.screen.blit(self.background, (0, 0))
        super().update()

    def key_down(self, _event: pygame.event.Event):
        pass

class PySnake(GameScreen):

    def __init__(self, parent):
        super().__init__(parent.real_screen, parent.real_window_size, parent.window_size)
        self.grid_size = Point(20, 20)
        self.cell_size = Point(15, 15)
        self.reset()
        head_image = pygame.image.load('assets/head.png')
        self.head_images = {
                Direction.UP: head_image,
                Direction.LEFT: pygame.transform.rotate(head_image, 90),
                Direction.DOWN: pygame.transform.rotate(head_image, 180),
                Direction.RIGHT: pygame.transform.rotate(head_image, 270),
                }
        tail_image = pygame.image.load('assets/tail.png')
        self.tail_images = {
                Direction.UP: tail_image,
                Direction.LEFT: pygame.transform.rotate(tail_image, 90),
                Direction.DOWN: pygame.transform.rotate(tail_image, 180),
                Direction.RIGHT: pygame.transform.rotate(tail_image, 270),
                }
        tail_curve_right_image = pygame.image.load('assets/tail_curve_right.png')
        self.tail_curve_right_images = {
                Direction.UP: tail_curve_right_image,
                Direction.LEFT: pygame.transform.rotate(tail_curve_right_image, 90),
                Direction.DOWN: pygame.transform.rotate(tail_curve_right_image, 180),
                Direction.RIGHT: pygame.transform.rotate(tail_curve_right_image, 270),
                }
        tail_curve_left_image = pygame.image.load('assets/tail_curve_left.png')
        self.tail_curve_left_images = {
                Direction.UP: tail_curve_left_image,
                Direction.LEFT: pygame.transform.rotate(tail_curve_left_image, 90),
                Direction.DOWN: pygame.transform.rotate(tail_curve_left_image, 180),
                Direction.RIGHT: pygame.transform.rotate(tail_curve_left_image, 270),
                }
        tail_end_image = pygame.image.load('assets/tail_end.png')
        self.tail_end_images = {
                Direction.UP: tail_end_image,
                Direction.LEFT: pygame.transform.rotate(tail_end_image, 90),
                Direction.DOWN: pygame.transform.rotate(tail_end_image, 180),
                Direction.RIGHT: pygame.transform.rotate(tail_end_image, 270),
                }
        self.fruit_image = pygame.image.load('assets/fruit.png')
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
                DeathScreen(self.real_screen, self.screen, self.real_window_size, self.window_size, self.score).run()
                self.reset()
            elif self.check_fruit():
                self.score += 1
                self.length_to_add += 2
                self.fruit = self.new_fruit()

    def key_down(self, event: pygame.event.Event):
        if event.key == K_w and self.last_direction != Direction.DOWN:
            self.direction = Direction.UP
        elif event.key == K_a and self.last_direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif event.key == K_s and self.last_direction != Direction.UP:
            self.direction = Direction.DOWN
        elif event.key == K_d and self.last_direction != Direction.LEFT:
            self.direction = Direction.RIGHT

    def reset(self):
        self.head = Point(self.grid_size.x // 2, self.grid_size.y // 2)
        self.previous_head = self.head
        self.tail = []
        self.direction = Direction.UP
        self.last_direction = self.direction
        self.length_to_add = 2
        self.score = 0
        self.fruit = self.new_fruit()

    def update_tail(self):
        self.tail.insert(0, (self.previous_head, self.previous_direction, self.last_direction))
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
        self.screen.blit(self.head_images[self.last_direction], (self.head.x * self.cell_size.x, self.head.y * self.cell_size.y))

    def draw_tail(self):
        prev_pos = self.head
        prev_direction = self.last_direction
        for pos, direction, next_direction in self.tail:
            if pos == self.tail[-1][0]:
                self.screen.blit(self.tail_end_images[next_direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
            elif direction == prev_direction:
                self.screen.blit(self.tail_images[direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
            else:
                if direction == Direction.RIGHT or direction == Direction.UP:
                    if prev_pos.x + prev_pos.y - pos.x - pos.y < 0:
                        self.screen.blit(self.tail_curve_left_images[direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
                    else:
                        self.screen.blit(self.tail_curve_right_images[direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
                else:
                    if prev_pos.x + prev_pos.y - pos.x - pos.y < 0:
                        self.screen.blit(self.tail_curve_right_images[direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
                    else:
                        self.screen.blit(self.tail_curve_left_images[direction], (pos.x * self.cell_size.x, pos.y * self.cell_size.y))
            prev_pos = pos
            prev_direction = direction

    def draw_fruit(self):
        self.screen.blit(self.fruit_image, (self.fruit.x * self.cell_size.x, self.fruit.y * self.cell_size.y))

    def draw_score(self):
        self.screen.blit(self.score_font.render(f'Score: {self.score}', True, (255, 255, 255)), (2, 2))

    def move(self):
        self.previous_head = copy(self.head)
        self.previous_direction = self.last_direction
        self.last_direction = self.direction
        if self.direction == Direction.UP:
            self.head.y -= 1
        elif self.direction == Direction.LEFT:
            self.head.x -= 1
        elif self.direction == Direction.DOWN:
            self.head.y += 1
        elif self.direction == Direction.RIGHT:
            self.head.x += 1

    def check_collision(self):
        if self.head.x < 0 or self.head.x >= self.grid_size.x or self.head.y < 0 or self.head.y >= self.grid_size.y or self.head in [pos for pos, _direction, _next_direction in self.tail]:
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
        for spot, _direction, _next_direction in self.tail:
            possible_spots.remove(spot)
        return choice(possible_spots)


if __name__ == '__main__':
    MainMenu().run()
