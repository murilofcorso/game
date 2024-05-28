import pygame

pygame.init()
spritesheet = pygame.image.load("sprites/skeleton-enemy/Skeleton enemy.png")

def separate_sprites(filepath, sprite_amount, direction="vertical", sprites_width=200, sprites_height=64):
    spritesheet = pygame.image.load(filepath)
    for i in range(sprite_amount):
        frame = spritesheet.subsurface(pygame.Rect(0, i * sprites_height, sprites_width, sprites_height))
        pygame.image.save(frame, f"{i}.png")



separate_sprites("sprites/skeleton-enemy/Skeleton enemy.png", 5, sprites_width=832)