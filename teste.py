from PIL import Image
import numpy as np
import pygame

imagem = Image.open("assets\sprites\sprites.png")

# Converte a imagem para RGBA (caso não esteja)
imagem = imagem.convert('RGBA')
dados = np.array(imagem)

for background_color in [(55, 55, 80), (57, 57, 83), (56, 56, 81), (56, 56, 80), (57, 57, 82), (56, 56, 82), (55, 55, 81), (57, 57, 83), (58, 58, 83)]:
    # Cria uma máscara para os pixels que correspondem à cor a ser removida
    mascara = np.all(dados[:, :, :3] == background_color, axis=-1)

    # Substitui os pixels da cor a ser removida pela cor substituta
    dados[mascara] = (255, 255, 255, 0)

# Cria uma nova imagem a partir dos dados modificados
imagem_limpa = Image.fromarray(dados, 'RGBA')

image_str = imagem_limpa.tobytes("raw", "RGBA")

# Convert the string data to a Pygame surface
size = imagem_limpa.size
pygame_image = pygame.image.fromstring(image_str, size, "RGBA")

pygame.image.save(pygame_image, "sprites-noback.png")