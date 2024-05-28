import pygame
from objects.character import Character

class Player(Character):
    IDLE = "idle"
    RUNNING = "running"
    ATTACKING = "attacking"
    CHARGING = "charging"

    ANIMATION_SPEED = 60
    ATTACK_ANIMATION_SPEED = 50

    ATTACK_RECT = (72, 37)

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.width = 32
        self.height = 48
        self.scale = 7
        self.sprites = {}
        self._load_sprites()
        self.sprite_offsets = {
            self.IDLE: (0, 0),
            self.RUNNING: (0, 0),
            self.ATTACKING: (0, 0),
            self.CHARGING: (8 * self.scale, 3 * self.scale),
        }
        self.flipped_sprite_offsets = {
            self.IDLE: 0,
            self.RUNNING: 0,
            self.ATTACKING: self.ATTACK_RECT[0] * self.scale,
            self.CHARGING: 0
        }
        
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()

        self.facing = "right"
        self.status = self.IDLE
        self.previous_status = self.status
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
                    self.rect.x -= self.speed
                    self.facing = "left"
                    self.status = self.RUNNING
                if keys[pygame.K_d]:
                    self.rect.x += self.speed
                    self.facing = "right"
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
        self.previous_status = self.status
        if self.status == self.ATTACKING and self.current_frame >= len(self.sprites[self.ATTACKING]) - 1:
            self.status = self.IDLE
            self.animation_speed = self.ANIMATION_SPEED
        

