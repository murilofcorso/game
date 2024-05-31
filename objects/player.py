import pygame
from objects.character import Character
from configs import *

class Player(Character):
    IDLE = "idle"
    RUNNING = "running"
    ATTACKING = "attacking"
    CHARGING = "charging"

    ANIMATION_SPEED = 60
    ATTACK_ANIMATION_SPEED = 50

    ATTACK_RECT = (75, 37)

    def __init__(self, groups):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()

        self.scale = 4
        self.width = 32
        self.height = 48
        self.sprites = {}
        self._load_sprites()

        self.offsets = {
            self.CHARGING: (8*self.scale, 4*self.scale),
            self.ATTACKING: (4*self.scale, 0*self.scale)
        }
        self.flipped_sprite_offsets = {
            self.IDLE: 0,
            self.RUNNING: 0,
            self.ATTACKING: 64 * self.scale,
            self.CHARGING: 0
        }
        
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-19*self.scale, -16*self.scale)
        self.hitbox.bottomleft = (0, SCREEN_HEIGHT-50)

        self.facing = pygame.Vector2((1, 0))
        self.status = self.IDLE
        self.speed = 9
        self.can_move = True

        self.current_frame = 0
        self.time_since_last_frame = 0
        self.animation_speed = self.ANIMATION_SPEED


    def move(self):
        keys = pygame.key.get_pressed()
        if self.status not in self.ATTACKING:
            self.status = self.IDLE

            if self.can_move:
                if keys[pygame.K_a]:
                    self.hitbox.x -= self.speed
                    self.facing.x = -1
                    self.status = self.RUNNING
                if keys[pygame.K_d]:
                    self.hitbox.x += self.speed
                    self.facing.x = 1
                    self.status = self.RUNNING
            if keys[pygame.K_SPACE]:
                self.status = self.CHARGING
                self.can_move = False
            else:
                self.can_move = True


    def attack(self):
        self.status = self.ATTACKING
        self.animation_speed = self.ATTACK_ANIMATION_SPEED
        self.current_frame = 0


    def handle_events(self):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.status != self.ATTACKING:
                    self.attack()


    def check_cooldowns(self):
        if self.status == self.ATTACKING and self.current_frame >= len(self.sprites[self.ATTACKING]) - 1:
            self.status = self.IDLE
            self.animation_speed = self.ANIMATION_SPEED


    def create_attack_hitbox(self):
        if self.status == self.ATTACKING and self.current_frame > 4:
            if self.facing[0] == 1:
                self.attack_hitbox = pygame.Rect(self.hitbox.right, self.hitbox.top, self.ATTACK_RECT[0]*self.scale, self.ATTACK_RECT[1]*self.scale)
            elif self.facing[0] == -1:
                self.attack_hitbox = pygame.Rect(self.hitbox.left - self.ATTACK_RECT[0]*self.scale, self.hitbox.top, self.ATTACK_RECT[0]*self.scale, self.ATTACK_RECT[1]*self.scale)
        else:
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), self.attack_hitbox)


    def _load_sprites(self):
        self.sprites[self.IDLE] = self._load_sprite_sheet("sprites/blue-witch/B_witch_idle.png", 6)
        self.sprites[self.RUNNING] = self._load_sprite_sheet("sprites/blue-witch/B_witch_run.png", 8)
        self.sprites[self.ATTACKING] = self._load_sprite_sheet("sprites/blue-witch/B_witch_attack.png", 9, frame_height=46, frame_width=104)
        self.sprites[self.CHARGING] = self._load_sprite_sheet("sprites/blue-witch/B_witch_charge.png", 5, frame_height=48, frame_width=48)


    def update(self, events, dt):
        self.dt = dt
        self.events = events
        self.handle_events()
        self.move()
        self.create_attack_hitbox()
        self.check_cooldowns()
        
        

