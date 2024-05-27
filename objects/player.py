import pygame

class Player(pygame.sprite.Sprite):
    IDLE = "idle"
    RUNNING = "running"
    ATTACKING = "attacking"

    ANIMATION_SPEED = 60
    ATTACK_ANIMATION_SPEED = 80

    ATTACK_RECT = (72, 37)

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.get_surface()

        self.size = (32, 48)
        self.scale = 3
        self.sprites = {}
        self._load_sprites()
        self.image = self.sprites[self.IDLE][0]
        self.rect = self.image.get_rect()

        self.facing = "right"
        self.status = self.IDLE
        self.previous_status = self.status
        self.speed = 4

        self.current_frame = 0
        self.time_since_last_frame = 0
        self.animation_speed = self.ANIMATION_SPEED


    def draw(self):
        self.time_since_last_frame += self.dt

        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame += 1
            self.time_since_last_frame = 0

        if self.current_frame >= len(self.sprites[self.status]) or self.status != self.previous_status:
            self.current_frame = 0

        self.image = self.sprites[self.status][self.current_frame]
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.screen.blit(self.image, self.rect.topleft)


    def move(self):
        keys = pygame.key.get_pressed()
        if self.status != self.ATTACKING:
            self.status = self.IDLE

            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.facing = "left"
                self.status = self.RUNNING
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.facing = "right"
                self.status = self.RUNNING


    def attack(self):
        self.status = self.ATTACKING
        self.animation_speed = self.ATTACK_ANIMATION_SPEED
        self.current_frame = 0
        if self.facing == "left":
            self.rect.left = self.rect.right - 48


    def handle_events(self):
        for event in self.events:
            print(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.attack()


    def _load_sprite_sheet(self, filepath, frame_count, frame_height=None, frame_width=None):
        spritesheet = pygame.image.load(filepath)
        sprites = []
        for i in range(frame_count):
            width = frame_width if frame_width else self.size[0]
            height = frame_height if frame_height else self.size[1]
            frame = pygame.transform.scale(
                spritesheet.subsurface(pygame.Rect(0, i * self.size[1], self.size[0], self.size[1])),
                (width * self.scale, height * self.scale)
            )
            sprites.append(frame)
        return sprites
    
    def _load_sprites(self):
        self.sprites[self.IDLE] = self._load_sprite_sheet("sprites/blue-witch/B_witch_idle.png", 6)
        self.sprites[self.RUNNING] = self._load_sprite_sheet("sprites/blue-witch/B_witch_run.png", 8)
        self.sprites[self.ATTACKING] = self._load_sprite_sheet("sprites/blue-witch/B_witch_attack.png", 9, frame_height=46, frame_width=104)


    def _load_sprites(self):
        idle_spritesheet = pygame.image.load("sprites/blue-witch/B_witch_idle.png")
        idle_sprites = []

        running_spritesheet = pygame.image.load("sprites/blue-witch/B_witch_run.png")
        running_sprites = []

        attack_spritesheet = pygame.image.load("sprites/blue-witch/B_witch_attack.png")
        attack_sprites = []
        for i in range(6):
            frame = pygame.transform.scale(idle_spritesheet.subsurface(pygame.Rect(0, i*self.size[1], self.size[0], self.size[1])), (self.size[0]*self.scale, self.size[1]*self.scale))
            idle_sprites.append(frame)
        for i in range(8):
            frame = pygame.transform.scale(running_spritesheet.subsurface(pygame.Rect(0, i*self.size[1], self.size[0], self.size[1])), (self.size[0]*self.scale, self.size[1]*self.scale))
            running_sprites.append(frame)
        for i in range(9):
            frame = pygame.transform.scale(attack_spritesheet.subsurface(pygame.Rect(0, i*46, 104, 46)), (104*self.scale, 46*self.scale))
            attack_sprites.append(frame)

        self.sprites["idle"] = idle_sprites
        self.sprites["running"] = running_sprites
        self.sprites["attacking"] = attack_sprites


    def update(self, events, dt):
        self.dt = dt
        self.events = events
        self.handle_events()
        self.move()
        self.previous_status = self.status
        if self.status == self.ATTACKING and self.current_frame >= len(self.sprites[self.ATTACKING]) - 1:
            self.status = self.IDLE
            self.animation_speed = self.ANIMATION_SPEED
        

