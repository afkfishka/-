import pygame
import os

from blocks import *


# Объявляем переменные
DISPLAY = WIN_WIDTH, WIN_HEIGHT = 1200, 800
PLATFORM_WIDTH = PLATFORM_HEIGHT = 42
BACKGROUND_COLOR = "#101920"

WALL_IMAGES = {
    '1': os.path.join(os.path.dirname(__file__), "blocks/wall_1.png"),
    '2': os.path.join(os.path.dirname(__file__), "blocks/wall_2.png"),
    '3': os.path.join(os.path.dirname(__file__), "blocks/wall_3.png"),
    '4': os.path.join(os.path.dirname(__file__), "blocks/wall_4.png"),
    '5': os.path.join(os.path.dirname(__file__), "blocks/wall_5.png"),
    '6': os.path.join(os.path.dirname(__file__), "blocks/wall_6.png"),
    '7': os.path.join(os.path.dirname(__file__), "blocks/wall_7.png"),
    '8': os.path.join(os.path.dirname(__file__), "blocks/wall_8.png"),
    '9': os.path.join(os.path.dirname(__file__), "blocks/wall_9.png"),
    '-': os.path.join(os.path.dirname(__file__), "blocks/wall_2.png"),
}


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окно
    pygame.display.set_caption("Super Mario Boy")  # Заголовок окна
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон

    entities = pygame.sprite.Group()  # Группа всех объектов
    platforms = []  # Платформы, в которые будем врезаться

    level = [
        "63333333333333333333333333337",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000000000000000005",
        "40000000000000630000037000005",
        "40000000000000400000005000005",
        "40000000000000400000005000005",
        "40000000000000400000005000005",
        "40000000000000400000005000005",
        "4000000000000092-----28000005",
        "406370-----000000000000000005",
        "40405000000000000000000000005",
        "40928000000000000000000000005",
        "40000000000000000000000000005",
        "92-------------------------28",
    ]

    timer = pygame.time.Clock()
    x = y = 0  # Начальные координаты
    for row in level:  # Итерируем строки уровня
        for col in row:  # Итерируем символы в строке
            if col != "0":  # Если символ не '0', создаем платформу
                image_path = WALL_IMAGES.get(col)  # Получаем путь к изображению в зависимости от колонки
                if image_path:  # Проверяем, что путь действителен
                    platform = Platform(image_path, x, y)  # Создаем платформу с нужной текстурой
                    entities.add(platform)  # Добавляем платформу в группу объектов
                    platforms.append(platform)

            x += PLATFORM_WIDTH  # Увеличиваем x на ширину платформы
        y += PLATFORM_HEIGHT  # Переходим к следующей строке
        x = 0  # Сбрасываем x для новой строки

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Ширина уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # Высота уровня
    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.blit(bg, (0, 0))  # Отрисовываем фон

        for i in entities:  # Отображаем все объекты на экране
            screen.blit(i.image, camera.apply(i))

        pygame.display.update()  # Обновляем экран
        timer.tick(60)


if __name__ == "__main__":
    main()
