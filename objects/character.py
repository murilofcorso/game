import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.last_status = None

    def _load_sprite_sheet(self, filepath, frame_count, direction="vertical", frame_height=None, frame_width=None):
        spritesheet = pygame.image.load(filepath)
        sprites = []
        if direction == "vertical":    
            for i in range(frame_count):
                width = frame_width if frame_width else self.width
                height = frame_height if frame_height else self.height

                frame = pygame.transform.scale(spritesheet.subsurface(pygame.Rect(0, i*height, width, height)), (width*self.scale, height*self.scale))
                sprites.append(frame)
        elif direction == "horizontal":
            for i in range(frame_count):
                width = frame_width if frame_width else self.width
                height = frame_height if frame_height else self.height

                frame = pygame.transform.scale(spritesheet.subsurface(pygame.Rect(i*width, 0, width, height)), (width*self.scale, height*self.scale))
                sprites.append(frame)
        return sprites
    

    def draw(self):
        self.time_since_last_frame += self.dt

        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame += 1
            self.time_since_last_frame = 0

        if self.current_frame >= len(self.sprites[self.status]) or self.last_status != self.status:
            self.current_frame = 0

        self.image = self.sprites[self.status][self.current_frame]
        self.rect.center = self.hitbox.center
        offset_x = self.offsets[self.status][0] if self.status in self.offsets.keys() else 0 
        offset_y = self.offsets[self.status][1] if self.status in self.offsets.keys() else 0 
        if self.facing.x == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            flipped_offset = self.flipped_sprite_offsets[self.status]
            position = (self.rect.x - flipped_offset - offset_x, self.rect.y - offset_y)
            self.screen.blit(self.image, position)
        else:
            position = (self.rect.x - offset_x, self.rect.y - offset_y)
            self.screen.blit(self.image, position)
        
        self.last_status = self.status
    