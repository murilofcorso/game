import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.get_surface()

        self.size = (32, 48)
        self.scale = 3
        self.sprites = {}
        self._load_sprites()
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()

        self.facing = "right"
        self.status = "idle"
        self.speed = 4

        self.current_frame = 0
        self.time_since_last_frame = 0
        self.animation_speed = 120


    def draw(self, dt):
        self.time_since_last_frame += dt
        if (self.time_since_last_frame >= self.animation_speed):
            self.current_frame = (self.current_frame + 1)
            self.time_since_last_frame = 0
        if self.current_frame >= len(self.sprites[self.status]):
            self.current_frame = 0
        
        if self.facing == "left":
            self.image = pygame.transform.flip(self.sprites[self.status][self.current_frame], True, False)
        else:
            self.image = self.sprites[self.status][self.current_frame]
        self.screen.blit(self.image, self.rect.topleft)


    def move(self):
        # Getting all pressed keys
        keys = pygame.key.get_pressed()  
        # Movement keys
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing = "left"
            self.status = "running"
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing = "right"
            self.status = "running"
        if not any(list(keys)):
            self.status = "idle"
        if keys[pygame.K_SPACE]:
            pass


    def _load_sprites(self):
        idle_spritesheet = pygame.image.load("sprites/blue-witch/B_witch_idle.png")
        idle_sprites = []

        running_spritesheet = pygame.image.load("sprites/blue-witch/B_witch_run.png")
        running_sprites = []
        for i in range(6):
            frame = pygame.transform.scale(idle_spritesheet.subsurface(pygame.Rect(0, i*self.size[1], self.size[0], self.size[1])), (self.size[0]*self.scale, self.size[1]*self.scale))
            idle_sprites.append(frame)
        for i in range(8):
            frame = pygame.transform.scale(running_spritesheet.subsurface(pygame.Rect(0, i*self.size[1], self.size[0], self.size[1])), (self.size[0]*self.scale, self.size[1]*self.scale))
            running_sprites.append(frame)

        self.sprites["idle"] = idle_sprites
        self.sprites["running"] = running_sprites


    def update(self):
        self.move()
        

