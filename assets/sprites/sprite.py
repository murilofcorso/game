from PIL import Image
import numpy as np
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, size):
        self.size = size
        self.image = None
        self.rect = None
   

    def get_sprite(self, sheetpath, position, transform=1):
        sheet = self.remove_background(sheetpath, [(55, 55, 80), (57, 57, 83), (56, 56, 81), (56, 56, 80), (57, 57, 82), (56, 56, 82), (55, 55, 81), (57, 57, 83)])
        self.image = pygame.surface.Surface(self.size, pygame.SRCALPHA)
        rect = self.image.get_rect()
        rect.topleft = (position[0] * self.size[0], position[1] * self.size[1])
        self.image.blit(sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (rect.width * transform, rect.height * transform))
        self.rect = self.image.get_rect()
        return self.image
    

    def remove_background(self, sheetpath, background_colors):
        imagem = Image.open(sheetpath)

        # Converte a imagem para RGBA (caso não esteja)
        imagem = imagem.convert('RGBA')
        dados = np.array(imagem)

        for background_color in background_colors:
            # Cria uma máscara para os pixels que correspondem à cor a ser removida
            mascara = np.all(dados[:, :, :3] == background_color, axis=-1)

            # Substitui os pixels da cor a ser removida pela cor substituta
            dados[mascara] = (255, 255, 255, 255)

        # Cria uma nova imagem a partir dos dados modificados
        imagem_limpa = Image.fromarray(dados, 'RGBA')

        image_str = imagem_limpa.tobytes("raw", "RGBA")

        # Convert the string data to a Pygame surface
        size = imagem_limpa.size
        pygame_image = pygame.image.fromstring(image_str, size, "RGBA")

        return pygame_image

