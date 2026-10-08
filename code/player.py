from pygame import FRect

from settings import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_frames, groups):
        super().__init__(groups)

        self.image: pygame.surface.Surface = player_frames[0]
        self.rect: FRect = self.image.get_frect()

        self.direction = pygame.math.Vector2()

    def update(self, delta_time):
        pressed_keys = pygame.key.get_pressed()
        self.direction.x = int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])
        self.direction.y = int(pressed_keys[pygame.K_s]) - int(pressed_keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

        self.rect.center += self.direction * 100 * delta_time
