from PIL import Image
import numpy as np

class Map:
    def __init__(self):
        pass

    def transform_map(self):
        # Carregue a imagem
        imagem = Image.open('sprites\man-sprites.png')

        # Converta a imagem para escala de cinza (opcional, depende do uso)
        imagem = imagem.convert('L')

        # Converta a imagem em um array numpy
        matriz = np.array(imagem)

        for i in matriz:
            for j in i:
                print(j, end=" ")


m = Map()
m.transform_map()