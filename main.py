import pygame
import sys
from configs import *
from objects.player import Player
import os
from debug import debug

# Initialize Pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

p = Player()

# Main loop
def main():
    # os.system("cls")
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        # (Insert game logic here)
        p.update()

        # Draw everything
        screen.fill(BG_COLOR)
        # (Insert drawing code here)
        p.draw(dt)
        debug(p.status)
        debug(p.facing, 30)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        # dt = clock.tick(60)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
