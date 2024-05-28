import pygame

class Character(pygame.sprite.Sprite):
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

        if self.current_frame >= len(self.sprites[self.status]):
            self.current_frame = 0

        self.image = self.sprites[self.status][self.current_frame]
        offsets = self.sprite_offsets[self.status]
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)
            flipped_offset = self.flipped_sprite_offsets[self.status]
            self.screen.blit(self.image, (self.rect.x - flipped_offset - offsets[0], self.rect.y - offsets[1]))
        else:
            self.screen.blit(self.image, (self.rect.x - offsets[0], self.rect.y - offsets[1]))
    

    