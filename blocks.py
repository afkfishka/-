from pygame import *
PLATFORM_WIDTH = PLATFORM_HEIGHT = 14 * 3


class Platform(sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = image.load(image_path)  # Загружаем текстуру блока из переданного пути
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
