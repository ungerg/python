import pygame
from random import randint, uniform

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
        self.speed = 400

        self.laser_ready = True
        self.last_shot_time = 0
        self.laser_cooldown = 300

    def start_cooldown_timer(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.laser_cooldown:
                self.laser_ready = True

    def update(self, delta_timed):
        pressed_keys = pygame.key.get_pressed()
        self.direction.x = int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])
        self.direction.y = int(pressed_keys[pygame.K_s]) - int(pressed_keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

        self.rect.center += self.direction * self.speed * delta_time
        if self.rect.centery >= WINDOW_HEIGHT:
            self.rect.centery = WINDOW_HEIGHT

        if pygame.mouse.get_just_pressed()[0] and self.laser_ready:
            laser_sound.play()
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            self.laser_ready = False
            self.last_shot_time = pygame.time.get_ticks()

        self.start_cooldown_timer()


class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups) -> None:
        super().__init__(groups)

        self.image: pygame.Surface = surface
        self.rect: pygame.FRect = self.image.get_frect(midbottom=position)

    def update(self, delta_time):
        self.rect.centery -= 400 * delta_time

        if self.rect.midbottom[1] <= 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups) -> None:
        super().__init__(groups)

        self.original_surface = surface
        self.image: pygame.Surface = surface
        self.rect: pygame.FRect = self.image.get_frect(center=position)

        self.creation_time = pygame.time.get_ticks()
        self.time_to_live_ms = 2000

        self.speed = randint(350, 550)
        self.direction = pygame.Vector2(uniform(-0.6, 0.6), 1)
        self.rotation_speed = randint(30, 400)
        self.current_angle = 0

    def update(self, delta_time):
        self.rect.center += self.speed * self.direction * delta_time

        self.current_angle += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(
            self.original_surface, self.current_angle, 1
        )
        self.rect = self.image.get_frect(center=self.rect.center)

        if self.rect.midbottom[1] <= 0:
            self.kill()


class ExplosionAnimation(pygame.sprite.Sprite):
    def __init__(self, frames, position, groups):
        super().__init__(groups)

        self.frames: list[pygame.Surface] = frames
        self.current_frame = 0

        self.image = frames[self.current_frame]
        self.rect = self.image.get_frect(center=position)

    def update(self, delta_time):
        self.current_frame += 30 * delta_time

        if self.current_frame < len(self.frames):
            self.image = self.frames[int(self.current_frame) % len(self.frames)]
        else:
            self.kill()


def check_collisions(add_to_score):

    if pygame.sprite.spritecollide(
        sprite=player,
        group=meteor_sprites,
        dokill=True,
        collided=pygame.sprite.collide_mask,  # type: ignore
    ):
        # player.kill()
        damage_sound.play()
        print("killed!")

    for laser in laser_sprites:
        hit_meteors = pygame.sprite.spritecollide(
            sprite=laser,
            group=meteor_sprites,
            dokill=True,
            collided=pygame.sprite.collide_mask,  # type: ignore
        )

        if hit_meteors:
            explosion_sound.play()
            add_to_score(100)
            laser.kill()
            ExplosionAnimation(explosion_frames, laser.rect.midtop, all_sprites)


def display_score(score):
    score_surface = font.render(str(int(score)), True, "#1252db")
    score_rect = score_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

    display_surface.blit(score_surface, score_rect)
    pygame.draw.rect(
        display_surface,
        "#1252db",
        score_rect.inflate(30, 20).move(0, -4),
        3,
        3,
    )


def add_to_score(amount):
    global score
    score += amount


pygame.init()
display_surface: pygame.Surface = pygame.display.set_mode(
    size=(WINDOW_WIDTH, WINDOW_HEIGHT)
)
pygame.display.set_caption("Python Game!")

meteor_surface = pygame.image.load("images/meteor.png").convert_alpha()
star_surface = pygame.image.load("images/star.png").convert_alpha()
laser_surface = pygame.image.load("images/laser.png").convert_alpha()
font = pygame.font.Font("images/Oxanium-Bold.ttf", 20)
explosion_frames = [
    pygame.image.load(f"images/explosion/{i}.png").convert_alpha() for i in range(21)
]
laser_sound = pygame.mixer.Sound("audio/laser.wav")
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
explosion_sound.set_volume(0.1)
damage_sound = pygame.mixer.Sound("audio/damage.ogg")
damage_sound.set_volume(0.1)
game_music = pygame.mixer.Sound("audio/game_music.wav")
game_music.set_volume(0.05)
game_music.play()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(num_stars):
    Star(star_surface, all_sprites)

player = Ship(all_sprites)

running = True
clock = pygame.time.Clock()
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)
score: float = 0

while running and player:
    delta_time: float = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

        if event.type == meteor_event:
            Meteor(
                meteor_surface,
                (randint(0, WINDOW_WIDTH), -20),
                (all_sprites, meteor_sprites),
            )

    all_sprites.update(delta_time)

    check_collisions(add_to_score)

    # re-draw the background every frame so we don't get blurring
    display_surface.fill((20, 20, 20))

    score += clock.get_time() / 100
    display_score(score)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
