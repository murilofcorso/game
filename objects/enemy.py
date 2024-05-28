import pygame
from objects.character import Character

class Enemy(Character):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"

    ANIMATION_SPEED = 100

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.width = 19
        self.height = 34
        self.scale = 7
        self.sprites = {}
        self._load_sprites()

        self.status = self.IDLE
        self.facing = "right"
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()
        self.sprite_offsets = {
            self.IDLE: (20, 14),
            self.WALKING: (20, 14),
            self.ATTACKING: (20, 14)
        }
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