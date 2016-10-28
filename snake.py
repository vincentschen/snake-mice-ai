# https://github.com/ternus/pygame-examples/blob/master/snake.py

import pygame
import sys
import time
import random

from pygame.locals import *

FPS = 15
pygame.init()
fpsClock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((0, 0, 0))
clock = pygame.time.Clock()

GRIDSIZE = 10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

def manhattan_distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return abs(dx) + abs(dy)

class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (0, 128, 0)
        self.cur_target = None

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.mice_eaten = 0
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def grow(self, addendum):
        self.length += addendum

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), \
                (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

class Mouse(object):
    def __init__(self, reward = 3):
        self.color = (255, 255, 255)
        self.position = (0, 0)
        self.randomize()
        self.reward = reward

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, \
                         random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def move(self, rand = True):
        if rand:
            cur = self.position
            x, y = random.choice([UP, DOWN, LEFT, RIGHT])
            self.position = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), \
                              (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        else:
            # TODO: Provide alternative to random movement
            pass

    def draw(self, surf):
        draw_box(surf, self.color, self.position)

class Game(object):
    def __init__(self, mice_count = 5):
        self.snake = Snake()
        self.mice = []
        for i in range(mice_count):
            self.mice.append(Mouse()) 
        self.move_parity = 0
        self.lose()

    def lose(self):
        self.snake.lose()

    def check_eat(self, snake, mouse):
        if snake.get_head_position() == mouse.position:
            snake.grow(mouse.reward)
            snake.cur_target = None
            mouse.randomize()
            snake.mice_eaten += 1

    def orient_snake(self):
        if self.snake.cur_target == None:
            closest_mouse = min(self.mice, key=lambda mouse: \
                                manhattan_distance(mouse.position, self.snake.get_head_position())) 
            self.snake.cur_target = closest_mouse
        else:
            closest_mouse = self.snake.cur_target
        snake_pos = self.snake.get_head_position()
        mouse_pos = closest_mouse.position
        dx = snake_pos[0] - mouse_pos[0]
        dy = snake_pos[1] - mouse_pos[1]
        if dy > 0:
            # going up ?
            if dx > 0:
                # going left ?
                if abs(dy) > abs(dx):
                    direction = UP if self.snake.direction != DOWN else LEFT
                else:
                    direction = LEFT if self.snake.direction != RIGHT else UP
            else:
                # going right ?
                if abs(dy) > abs(dx):
                    direction = UP if self.snake.direction != DOWN else RIGHT
                else:
                    direction = RIGHT if self.snake.direction != LEFT else UP
        else:
            # going down ?
            if dx > 0:
                # going left ?
                if abs(dy) > abs(dx):
                    direction = DOWN if self.snake.direction != UP else LEFT
                else:
                    direction = LEFT if self.snake.direction != RIGHT else DOWN
            else:
                # going right ?
                if abs(dy) > abs(dx):
                    direction = DOWN if self.snake.direction != UP else RIGHT
                else:
                    direction = RIGHT if self.snake.direction != LEFT else DOWN
        self.snake.point(direction)

    def tick(self):
        self.orient_snake()
        self.snake.move()
        for mouse in self.mice:
            if self.move_parity:
                mouse.move()
                self.move_parity = 0
            else:
                self.move_parity = 1
            self.check_eat(self.snake, mouse)
            self.snake.draw(surface)
            mouse.draw(surface)
        

if __name__ == '__main__':
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        surface.fill((0, 0, 0))
        game.tick()
        font = pygame.font.Font(None, 36)
        text = font.render(str(game.snake.mice_eaten), 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)
