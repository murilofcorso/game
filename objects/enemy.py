import pygame
from objects.character import Character
from configs import *

class Enemy(Character):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"
    TAKING_DAMAGE = "taking_damage"

    ANIMATION_SPEED = 100

    def __init__(self, groups):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()

        self.health = 100
        self.speed = 2

        self.scale = 4
        self.width = 19 * self.scale
        self.height = 34 * self.scale
        self.sprites = {}
        self._load_sprites()

        self.status = self.IDLE
        self.facing = pygame.Vector2((1, 0))
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-50*self.scale, -32*self.scale)
        self.hitbox.bottomleft = (150, SCREEN_HEIGHT-50)

        self.offsets = {}
        self.flipped_sprite_offsets = {
            self.IDLE: 0,
            self.WALKING: 0,
            self.ATTACKING: 0,
            self.TAKING_DAMAGE: 0
        }

        self.animation_speed = self.ANIMATION_SPEED
        self.time_since_last_frame = 0
        self.current_frame = 0

        self.vulnerable = True
        self.enemy_cooldowns = {
            "HIT_COOLDOWN": 300
        }
        self.hit_tick = 0


    def _load_sprites(self):
        self.sprites[self.IDLE] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-idle.png", 4, "horizontal", 64, 64)
        self.sprites[self.WALKING] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-walk.png", 12, "horizontal", 64, 64)
        self.sprites[self.ATTACKING] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-attack.png", 13, "horizontal", 64, 64)
        self.sprites[self.TAKING_DAMAGE] = self._load_sprite_sheet("sprites\skeleton-enemy\skeleton-take-damage.png", 3, "horizontal", 64, 64)


    def take_damage(self):
        self.health -= 10
        self.vulnerable = False
        self.current_frame = 0
        self.status = self.TAKING_DAMAGE
        self.hit_tick = pygame.time.get_ticks()


    def is_vulnerable(self):
        return self.vulnerable


    def cooldowns(self):
        current_tick = pygame.time.get_ticks()
        if not self.is_vulnerable():
            if current_tick - self.hit_tick > self.enemy_cooldowns["HIT_COOLDOWN"]:
                self.vulnerable = True
                self.status = self.IDLE


    def move(self):
        self.hitbox.x += self.speed * self.facing[0]


    def update(self, events, dt):
        self.dt = dt
        self.events = events
        self.cooldowns()