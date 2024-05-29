import pygame
from objects.character import Character
from configs import *

class Enemy(Character):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"

    ANIMATION_SPEED = 100

    def __init__(self, groups):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()

        self.scale = 4
        self.width = 19 * self.scale
        self.height = 34 * self.scale
        self.sprites = {}
        self._load_sprites()

        self.status = self.ATTACKING
        self.facing = pygame.Vector2()
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-50*self.scale, -32*self.scale)
        self.hitbox.bottomleft = (150, SCREEN_HEIGHT-50)

        self.offsets = {}
        self.flipped_sprite_offsets = {
            self.IDLE: 0,
            self.WALKING: 0,
            self.ATTACKING: 0,
        }

        self.animation_speed = self.ANIMATION_SPEED
        self.time_since_last_frame = 0
        self.current_frame = 0


    def _load_sprites(self):
        self.sprites[self.IDLE] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-idle.png", 4, "horizontal", 64, 64)
        self.sprites[self.WALKING] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-walk.png", 12, "horizontal", 64, 64)
        self.sprites[self.ATTACKING] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-attack.png", 13, "horizontal", 64, 64)


    def update(self, events, dt):
        self.dt = dt
        self.events = events