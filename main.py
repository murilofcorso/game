import pygame
import sys
from configs import *
from map import Map
from debug import debug
from objects.enemy import Enemy

# Initialize Pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

map = Map()

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        # Cap the frame rate
        dt = clock.tick(60)

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        # (Insert game logic here)
        for sprite in map.visible_sprites:
            sprite.update(events, dt)

        # Draw background
        screen.fill(BG_COLOR)
        # (Insert drawing code here)
        for sprite in map.visible_sprites:
            sprite.draw()
            if type(sprite) == Enemy:
                debug(sprite.health)
                debug(f"{sprite.status} {sprite.last_status}", 30)
                debug(sprite.current_frame, 50)
                
        map.check_attack_collisions()
        map.set_player_enemy_distance()
        

        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
