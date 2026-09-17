import pygame
from random import randint

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

num_stars = 20


class Star(pygame.sprite.Sprite):
    def __init__(self, surface, groups) -> None:
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect: pygame.FRect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

        self.direction = pygame.math.Vector2()
        self.speed = 350

        self.laser_ready = True
        self.last_shot_time = 0
        self.laser_cooldown = 400

    def start_cooldown_timer(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.laser_cooldown:
                self.laser_ready = True

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.direction.x = int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])
        self.direction.y = int(pressed_keys[pygame.K_s]) - int(pressed_keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * delta_time

        if pygame.mouse.get_just_pressed()[0] and self.laser_ready:
            Laser(laser_surface, self.rect.midtop, all_sprites)
            self.laser_ready = False
            self.last_shot_time = pygame.time.get_ticks()

        self.start_cooldown_timer()


class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups) -> None:
        super().__init__(groups)

        self.image = surface
        self.rect: pygame.FRect = self.image.get_frect(midbottom=position)

    def update(self):
        self.rect.centery -= 400 * delta_time

        if self.rect.midbottom[1] <= 0:
            self.kill()


pygame.init()
display_surface: pygame.Surface = pygame.display.set_mode(
    size=(WINDOW_WIDTH, WINDOW_HEIGHT)
)
pygame.display.set_caption("Python Game!")


meteor_surface = pygame.image.load("images/meteor.png").convert_alpha()
meteor_rect = meteor_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

all_sprites = pygame.sprite.Group()

star_surface = pygame.image.load("images/star.png").convert_alpha()
for i in range(num_stars):
    Star(star_surface, all_sprites)

player = Ship(all_sprites)
laser_surface = pygame.image.load("images/laser.png").convert_alpha()

running = True
clock = pygame.time.Clock()
while running:
    delta_time: float = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    all_sprites.update()

    # re-draw the background every frame so we don't get blurring
    display_surface.fill((20, 20, 20))

    display_surface.blit(meteor_surface, meteor_rect)

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
