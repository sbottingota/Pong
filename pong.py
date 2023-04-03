import random

import pygame

from pygame.locals import (
    K_UP, K_DOWN,
    K_w, K_s,
    QUIT
)


BG_COLOR = (255,) * 3
FG_COLOR = (0,) * 3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

PADDLE_X = SCREEN_WIDTH / 15
PADDLE_Y = SCREEN_HEIGHT / 2

PADDLE_WIDTH = SCREEN_WIDTH / 30
PADDLE_HEIGHT = SCREEN_HEIGHT / 5

SPEED_MULTIPLIER = 2


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((width, height))
        self.image.fill(FG_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.collidepoint(self.rect.x, 0):
            self.rect.y += SPEED_MULTIPLIER

        elif self.rect.collidepoint(self.rect.x, SCREEN_HEIGHT):
            self.rect.y -= SPEED_MULTIPLIER


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((r * 2,) * 2, pygame.SRCALPHA)
        self.image = self.image.convert_alpha()

        pygame.draw.circle(self.image, FG_COLOR, (r, r), r)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.dx = random.choice((-1, 1))
        self.dy = random.choice((random.uniform(1, -0.7), random.uniform(0.7, 1)))

        self.radius = r

    def update(self):
        self.rect.x += self.dx * SPEED_MULTIPLIER
        self.rect.y += self.dy * SPEED_MULTIPLIER

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()


sprites = pygame.sprite.Group()

left_paddle = Paddle(
    PADDLE_X, PADDLE_Y,
    PADDLE_WIDTH, PADDLE_HEIGHT,
    sprites
)
right_paddle = Paddle(
    SCREEN_WIDTH - 2 * PADDLE_X, PADDLE_Y,
    PADDLE_WIDTH, PADDLE_HEIGHT,
    sprites
)

ball = Ball(
    SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
    SCREEN_WIDTH / 40,
    sprites
)

while True:
    if any([event.type == QUIT for event in pygame.event.get()]):
        break

    screen.fill(BG_COLOR)

    keys_pressed = pygame.key.get_pressed()
    # left paddle controls
    if keys_pressed[K_w]:
        left_paddle.rect.y -= SPEED_MULTIPLIER

    if keys_pressed[K_s]:
        left_paddle.rect.y += SPEED_MULTIPLIER

    # right paddle controls
    if keys_pressed[K_UP]:
        right_paddle.rect.y -= SPEED_MULTIPLIER

    if keys_pressed[K_DOWN]:
        right_paddle.rect.y += SPEED_MULTIPLIER


    if ball.rect.colliderect(left_paddle.rect)\
            or ball.rect.colliderect(right_paddle.rect):
        ball.dx *= -1
        ball.dy *= random.uniform(0.8, 1.2)

    if not (0 < ball.rect.y and ball.rect.y + ball.rect.height < SCREEN_HEIGHT):
        ball.dy *= random.uniform(-1.2, -0.8)

    if not 0 < ball.rect.x < SCREEN_WIDTH:
        break

    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()

    clock.tick(120)

pygame.quit()

