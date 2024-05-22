import pygame
from assets.sprites.sprite import Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.get_surface()

        self.size = (32, 48)
        self.scale = 3
        self.image = Sprite(self.size).get_sprite("assets/sprites/blue-witch/B_witch_idle.png", (0, 0), self.scale)
        self.rect = self.image.get_rect()

        self.facing = "right"
        self.status = "idle"
        self.speed = 3


    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)



    def move(self):
        # Getting all pressed keys
        keys = pygame.key.get_pressed()  

        # Movement keys
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing = "left"
            self.status = "moving_left"
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing = "right"
            self.status = "moving_right"
        # if keys[pygame.K_w]:
        #     self.rect.y -= self.speed
        #     self.facing = "up"
        #     self.status = "moving_up"
        # if keys[pygame.K_s]:
        #     self.rect.y += self.speed
        #     self.facing = "down"
        #     self.status = "moving_down" 
        if not any(list(keys)):
            self.status = f"idle_{self.facing}"
            

        # Dash keys
        if keys[pygame.K_SPACE]:
            pass


    def update(self):
        self.move()
        

