import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        player_frames = [
            pygame.image.load(f"images/player/down/{i}.png").convert_alpha()
            for i in range(4)
        ]
        print(player_frames)

        self.all_sprites = pygame.sprite.Group()
        self.player = Player(player_frames, groups=self.all_sprites)

        self.clock = pygame.time.Clock()

    def start_game(self) -> None:
        pygame.display.set_caption("Vampire Game!")

        running = True

        while running:
            delta_time = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False

            self.all_sprites.update(delta_time)

            # re-draw the background every frame so we don't get blurring
            self.display_surface.fill((20, 20, 20))

            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

        pygame.quit()
