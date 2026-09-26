import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


def start_game() -> None:
    pygame.init()
    display_surface: pygame.Surface = pygame.display.set_mode(
        size=(WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Vampire Game!")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False


pygame.quit()
