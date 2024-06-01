import pygame
from objects.entity import Entity
from configs import *

class Enemy(Entity):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"
    TAKING_DAMAGE = "taking_damage"
    DIYING = "diying"

    ANIMATION_SPEED = 100
    ATTACK_ANIMATION_SPEED = 90

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
            self.TAKING_DAMAGE: 0,
            self.DIYING: 0
        }

        self.animation_speed = self.ANIMATION_SPEED
        self.time_since_last_frame = 0
        self.current_frame = 0

        self.vulnerable = True
        self.enemy_cooldowns = {
            "HIT_COOLDOWN": 400
        }
        self.hit_tick = 0

        self.distance_player = 0

    def _load_sprites(self):
        self.sprites[self.IDLE] = self._load_sprite_sheet("sprites/skeleton-enemy/skeleton-idle.png", 4, "horizontal", 64, 64)
        self.sprites[self.WALKING] = self._load_sprite_sheet("sprites/skeleton-enemy/skeleton-walk.png", 12, "horizontal", 64, 64)
        self.sprites[self.ATTACKING] = self._load_sprite_sheet("sprites/skeleton-enemy/skeleton-attack.png", 13, "horizontal", 64, 64)
        self.sprites[self.TAKING_DAMAGE] = self._load_sprite_sheet("sprites/skeleton-enemy/skeleton-take-damage.png", 3, "horizontal", 64, 64)
        self.sprites[self.DIYING] = self._load_sprite_sheet("sprites/skeleton-enemy/skeleton-death.png", 13, "horizontal", 64, 64)


    def take_damage(self):
        self.health -= 30
        self.vulnerable = False
        self.status = self.TAKING_DAMAGE
        self.hit_tick = pygame.time.get_ticks()


    def is_vulnerable(self):
        return self.vulnerable
    

    def is_attacking(self):
        return self.status == self.ATTACKING


    def is_alive(self):
        return self.health > 0
    

    def is_taking_damage(self):
        return not self.is_vulnerable()


    def cooldowns(self):
        current_tick = pygame.time.get_ticks()
        if not self.is_vulnerable():
            if current_tick - self.hit_tick > self.enemy_cooldowns["HIT_COOLDOWN"]:
                self.vulnerable = True


    def can_move(self):
        return self.distance_player < 1000 and self.status not in (self.ATTACKING, self.DIYING)


    def move(self):
        self.status = self.WALKING
        self.hitbox.x += self.speed * self.facing[0]


    def set_animation_speed(self):
        if self.status == self.ATTACKING:
            self.animation_speed = self.ATTACK_ANIMATION_SPEED
        else:
            self.animation_speed = self.ANIMATION_SPEED


    def attack(self):
        self.status = self.ATTACKING
        self.animation_speed = self.ATTACK_ANIMATION_SPEED


    def can_attack(self):
        return self.distance_player <= 130 and self.status not in (self.TAKING_DAMAGE, self.DIYING)


    def die(self):
        self.status = self.DIYING


    def handle_logic(self):
        # check if is alive
        if not self.is_alive():
            # kill enemy if is not alive
            self.die()
            # check if animation is finished
            if self.current_frame == len(self.sprites[self.DIYING])-1:
                # eliminate enemy sprite
                self.kill()
        # check if is attacking
        elif self.is_attacking() and self.current_frame < len(self.sprites[self.ATTACKING])-1:
            # make sure to finish attack animation 
            self.attack()
        else:
            # setting "default" status
            self.status = self.IDLE

        # check if can attack
        if self.can_attack():
            # attack
            self.attack()
        # check if can move
        elif self.can_move():
            # move
            self.move()
            # check if is taking damage
            if self.is_taking_damage():
                self.status = self.TAKING_DAMAGE
                self.speed = 1
            else:
                self.speed = 2
        

    def create_attack_hitboxes(self):
        if self.status == self.ATTACKING:
            if self.facing[0] == 1:
                if self.current_frame == 4:
                    self.attack_hitbox = pygame.Rect(self.rect.left + 13*self.scale, self.rect.top + 8*self.scale, 51*self.scale, 28*self.scale)
                elif self.current_frame == 8:
                    self.attack_hitbox = pygame.Rect(self.rect.left + 2*self.scale, self.rect.top + 16*self.scale, 62*self.scale, 24*self.scale)
                else:
                    self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            elif self.facing[0] == -1:
                if self.current_frame == 4:
                    self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.top + 8*self.scale, 51*self.scale, 28*self.scale)
                elif self.current_frame == 8:
                    self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.top + 16*self.scale, 62*self.scale, 24*self.scale)
                else:
                    self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        else:
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)


    def update(self, events, dt):
        self.dt = dt
        self.events = events
        self.create_attack_hitboxes()
        self.cooldowns()
        self.handle_logic()
        self.set_animation_speed()