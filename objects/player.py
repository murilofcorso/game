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
        self.ultimo_status = self.status
        self.speed = 4

        self.current_frame = 0
        self.time_since_last_frame = 0
        self.animation_speed = 60
        self.attack_animation_speed = 30


    def draw(self):
        self.time_since_last_frame += self.dt

        # Setting spritesheet animation speed
        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame += 1
            self.time_since_last_frame = 0

        # Restarting spritesheet loop
        if (self.current_frame >= len(self.sprites[self.status])) or (self.status != self.ultimo_status):
            self.current_frame = 0

        # Fliping player according to "self.facing"
        if self.facing == "left":
            self.image = pygame.transform.flip(self.sprites[self.status][self.current_frame], True, False)
        else:
            self.image = self.sprites[self.status][self.current_frame]

        # Placing player image on screen
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


    def attack(self):
        print("atacking")


    def handle_events(self):
        for event in self.events:
            print(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.attack()


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
        self.dt =  dt
        self.events = events
        self.draw()
        self.handle_events()
        self.move()
        self.ultimo_status = self.status
        

