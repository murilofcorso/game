import pygame
from objects.player import Player
from objects.enemy import Enemy


class Map:
    def __init__(self):
        self.visible_sprites = pygame.sprite.Group()
        self.collidable_sprites = pygame.sprite.Group()


        self.player = Player([self.visible_sprites, self.collidable_sprites])
        self.enemy = Enemy([self.visible_sprites, self.collidable_sprites])
        

    def check_attack_collisions(self):
        for sprite in self.visible_sprites:
            if type(sprite) == Player and sprite.status == sprite.ATTACKING:
                for collidable_sprite in self.collidable_sprites:
                    if sprite.attack_hitbox.colliderect(collidable_sprite.hitbox):
                        if collidable_sprite.is_vulnerable():
                            collidable_sprite.take_damage()
                            collidable_sprite.hitbox.x += 70 * sprite.facing[0]
                