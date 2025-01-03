import pygame
from pygame import *
import os

# Установка размеров окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) = 1200, 800
PLATFORM_WIDTH = PLATFORM_HEIGHT = 42
MOVE_STEP = 42
FPS = 60

# Начальное положения персонажа (отсчет с 0)
START_X = 11
START_Y = 15

BACKGROUND_COLOR = "#101920"  # Цвет фона

# Получение директории для изображений
ICON_DIR = os.path.dirname(__file__)

# Словарь с изображениями стен
WALL_IMAGES = {
    '1': 'wall_1.png', '2': 'wall_2.png', '3': 'wall_3.png', '4': 'wall_4.png',
    '5': 'wall_5.png', '6': 'wall_6.png', '7': 'wall_7.png', '8': 'wall_8.png',
    '9': 'wall_9.png', '-': 'wall_2.png', 'z': 'wall_10.png', 'x': 'wall_11.png',
    'c': 'wall_12.png', 'q': 'wall_13.png', 'w': 'wall_14.png', 'e': 'wall_15.png',
    'r': 'wall_16.png', 't': 'wall_17.png', 'y': 'wall_18.png', 'u': 'wall_19.png',
    'p': 'wall_20.png', 'a': 'wall_21.png', 's': 'wall_22.png'
}


# Класс для представления платформ
class Platform(sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = image.load(image_path)  # Загружаем изображение платформы
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для платформы


# Класс для представления игрока
class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Направление взгляда персонажа (начальное вправо вниз)
        self.up = self.left = False
        self.down = self.right = True
        self.direction = None

        # Загружаем кадры для различных направлений
        self.frames_down_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_botleft")
        self.frames_down_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6,"man_botright")
        self.frames_left_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_leftbot")
        self.frames_left_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_lefttop")
        self.frames_right_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6,"man_rightbot")
        self.frames_right_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_righttop")
        self.frames_up_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_topleft")
        self.frames_up_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_topright")

        self.frames = self.frames_down_right  # Начальные кадры - смотрим вниз вправо
        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для игрока
        self.frame_rate = 8  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

    def start_move(self, left, right, up, down, direction):
        # Установка направления движения на основе нажатых клавиш
        self.direction = direction
        if left:
            self.left = True
            self.right = False
        elif right:
            self.right = True
            self.left = False
        elif up:
            self.up = True
            self.down = False
        elif down:
            self.down = True
            self.up = False

    def update(self, platforms):
        # Основная логика анимации
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

        # Двигаемся в текущее направление, если оно задано
        if self.direction:
            moved = self.move(platforms)
            if not moved:
                self.direction = None  # Останавливаем движение, если столкновение

    def move(self, platforms):
        # Переменные для изменения позиции
        dx, dy = 0, 0

        if self.direction == 'left':
            dx = -MOVE_STEP
            if self.down:
                self.frames = self.frames_left_down
            elif self.up:
                self.frames = self.frames_left_up

        elif self.direction == 'right':
            dx = MOVE_STEP
            if self.down:
                self.frames = self.frames_right_down
            elif self.up:
                self.frames = self.frames_right_up

        elif self.direction == 'up':
            dy = -MOVE_STEP
            if self.left:
                self.frames = self.frames_up_left
            elif self.right:
                self.frames = self.frames_up_right

        elif self.direction == 'down':
            dy = MOVE_STEP
            if self.left:
                self.frames = self.frames_down_left
            elif self.right:
                self.frames = self.frames_down_right

        # Обновляем позицию игрока
        self.rect.x += dx
        self.rect.y += dy

        # Проверка коллизий с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx < 0:  # Движение влево
                    self.rect.left = platform.rect.right
                elif dx > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                if dy < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                elif dy > 0:  # Движение вниз
                    self.rect.bottom = platform.rect.top
                return False  # Столкновение произошло

        return True  # Перемещение прошло успешно


# Класс для представления камеры
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)  # Устанавливаем начальные параметры камеры

    def apply(self, target):
        return target.rect.move(self.state.topleft)  # Применяем положение камеры к целевому объекту

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)  # Обновляем состояние камеры


# Функция для получения пути к изображению стены
def get_wall_image_path(key):
    return os.path.join(os.path.dirname(__file__), "blocks", WALL_IMAGES[key])


# Функция для конфигурирования камеры
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH // 2, -t + WIN_HEIGHT // 2  # Центрируем камеру на игроке

    # Ограничиваем движение камеры по x
    l = max(-(camera.width - WIN_WIDTH), l)  # Правая граница
    l = min(0, l)  # Левая граница

    # Ограничиваем движение камеры по y
    t = max(-(camera.height - WIN_HEIGHT), t)  # Нижняя граница
    t = min(0, t)  # Верхняя граница

    return Rect(l, t, w, h)


# Функция для загрузки анимационных кадров
def load_animation_frames(path, count, prefix):
    frames = []
    for i in range(count):
        image_path = os.path.join(path, f'{prefix}_{i}.png')  # Загружаем кадры анимации
        frames.append(image.load(image_path))
    return frames


# Основная функция игры
def main():
    pygame.init()  # Инициализация Pygame
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна игры
    pygame.display.set_caption("Тайны подземелий")  # Установка заголовка окна
    bg = Surface(DISPLAY)  # Создаем поверхность для фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон цветом

    hero = Player(START_X * 42, START_Y * 42)  # Создаем экземпляр игрока
    entities = pygame.sprite.Group()  # Группа всех спрайтов
    platforms = []  # Список платформ

    entities.add(hero)  # Добавляем игрока в группу спрайтов

    # Определение уровня в виде строк
    level = [
        "00000000063700000",
        "00000000040500000",
        "00000000040500000",
        "00000000040500000",
        "00000000040500000",
        "000000633r0500000",
        "00000040000500000",
        "000000400w2800000",
        "000000400e7000000",
        "00000040005000000",
        "00000092q05000000",
        "00000000405000000",
        "00000000405000000",
        "00000063r0e370000",
        "00000040000050000",
        "0000004000u050000",
        "0000004000p050000",
        "0000004000p050000",
        "000633txy2s050000",
        "00040000504050000",
        "00040wq0e3r050000",
        "00040540000050000",
        "633r0etxxxyca3337",
        "4000000000er00005",
        "40000w22q00000005",
        "400005009cxxz0005",
        "40000500040000005",
        "92--2800040000005",
        "00000000040000005",
        "00000000092----28",
    ]

    x = y = 0  # Начальные координаты для размещения платформ
    for row in level:
        for col in row:
            if col != "0":  # Если символ не '0', значит это стена
                image_path = get_wall_image_path(col)  # Получаем путь к изображению стены
                pf = Platform(image_path, x, y)  # Создаем платформу
                entities.add(pf)  # Добавляем платформу в группу спрайтов
                platforms.append(pf)  # Добавляем платформу в список платформ

            x += PLATFORM_WIDTH  # Обновляем координату x площадки
        y += PLATFORM_HEIGHT  # Обновляем координату y площадки
        x = 0  # Сбрасываем x для следующей строки

    # Определяем размеры уровня
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT
    camera = Camera(camera_configure, total_level_width, total_level_height)  # Создаем камеру

    while True:
        keys = pygame.key.get_pressed()  # Получаем состояние клавиш
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:  # Обработка нажатий клавиш
                if event.key == K_LEFT:
                    hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'left')
                elif event.key == K_RIGHT:
                    hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'right')
                elif event.key == K_UP:
                    hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'up')
                elif event.key == K_DOWN:
                    hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'down')

        # Обновляем игрока
        hero.update(platforms)

        screen.blit(bg, (0, 0))  # Отображаем фон
        camera.update(hero)  # Обновляем камеру
        for spr in entities:
            screen.blit(spr.image, camera.apply(spr))

        pygame.display.update()  # Обновляем экран
        pygame.time.Clock().tick(FPS)  # Ограничиваем FPS игры до 60


# Запуск основной функции
if __name__ == "__main__":
    main()
