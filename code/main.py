import pygame

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Game!")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill((20, 20, 20))
    pygame.display.update()

pygame.quit()
