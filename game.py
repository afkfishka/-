import pygame
from pygame import *
import os

# Установка размеров окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) = 1200, 800
PLATFORM_WIDTH = PLATFORM_HEIGHT = 42
MOVE_STEP = 21
FPS = 120

SELECT_LEVEL = "level_1.txt"

# Начальное положения персонажа (отсчет с 0)
START_X = 13
START_Y = 28

BACKGROUND_COLOR = "#101920"  # Цвет фона

# Получение директории для изображений
ICON_DIR = os.path.dirname(__file__)

# Словарь с изображениями стен
WALL_IMAGES = {
    '□': 'wall_1.png', '▔': 'wall_2.png', '▁': 'wall_3.png', '▕': 'wall_4.png', '▎': 'wall_5.png',
    '╔': 'wall_6.png', '╗': 'wall_7.png', '╚': 'wall_8.png', '╝': 'wall_9.png', '-': 'wall_2.png',
    '⊓': 'wall_10.png', '⊏': 'wall_11.png', '⊔': 'wall_12.png', '⊐': 'wall_13.png', '=': 'wall_14.png',
    '║': 'wall_15.png', '┓': 'wall_16.png', '┛': 'wall_17.png', '┗': 'wall_18.png', '┏': 'wall_19.png',
    'q': 'wall_20.png', 'w': 'wall_21.png', 'e': 'wall_22.png', 'r': 'wall_23.png', 't': 'wall_24.png',
    'y': 'wall_25.png', 'u': 'wall_26.png', 'i': 'wall_27.png',
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
        self.frames_down_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6,
                                                       "man_botright")
        self.frames_left_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_leftbot")
        self.frames_left_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_lefttop")
        self.frames_right_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6,
                                                       "man_rightbot")
        self.frames_right_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_righttop")
        self.frames_up_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_topleft")
        self.frames_up_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_topright")

        # Загружаем кадры анимации движения
        self.flight_frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 4, "man_move")

        self.frames = self.frames_down_right  # Начальные кадры - смотрим вниз вправо
        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для игрока
        self.frame_rate = 8  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

    def start_move(self, left, right, up, down, direction):
        # Установка направления движения на основе нажатых клавиш
        if not self.direction:
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
        # Проверяем, движется ли игрок
        if self.direction:  # Если персонаж движется, используем анимацию
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.frame_counter = 0
                self.index = (self.index + 1) % len(self.flight_frames)
                self.image = self.flight_frames[self.index]
        else:  # Если не движется, используем основную анимацию
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


# Новый класс для монет
class Coin(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'coin'), 4, "coin")
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.frame_rate = 15
        self.frame_counter = 0

    def update(self):
        # Логика анимации монеты
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]


# Новый класс для опыта
class XP(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'xp', 'xp_0.png'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# Новый класс для звезд
class Star(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'star', 'star_0.png'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# Новый класс для финиша
class Finish(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'exit'), 2, "exit")
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.frame_rate = 15
        self.frame_counter = 0

    def update(self):
        # Логика анимации объекта Finish
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]


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

    return Rect(l, t, w, h)


# Функция для загрузки анимационных кадров
def load_animation_frames(path, count, prefix):
    frames = []
    for i in range(count):
        image_path = os.path.join(path, f'{prefix}_{i}.png')  # Загружаем кадры анимации
        frames.append(image.load(image_path))
    return frames


def load_level_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            level = file.readlines()
        if not level:
            raise ValueError("Файл уровня пуст.")
        return [line.strip() for line in level]  # Возвращаем строки уровня без изменений
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {filename}")
        return []
    except ValueError as e:
        print(e)
        return []


# Основная функция игры
def main():
    pygame.init()  # Инициализация Pygame
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна игры
    pygame.display.set_caption("Тайны подземелий")  # Установка заголовка окна
    bg = Surface(DISPLAY)  # Создаем поверхность для фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон цветом

    hero = Player(START_X * PLATFORM_WIDTH, START_Y * PLATFORM_HEIGHT)  # Создаем экземпляр игрока
    entities = pygame.sprite.Group()  # Группа всех спрайтов
    platforms = []  # Список платформ

    entities.add(hero)  # Добавляем игрока в группу спрайтов

    # Определение уровня в виде строк
    level = load_level_from_file(os.path.join("levels", SELECT_LEVEL))

    if not level:
        print("Ошибка: Не удалось загрузить уровень.")
        return  # Прекращаем выполнение функции, так как уровень не загружен

    # Заполнение платформ и объектов из level_1.txt
    for y, row in enumerate(level):
        for x, col in enumerate(row):
            if col in WALL_IMAGES:
                image_path = get_wall_image_path(col)  # Пример получения изображения для стены
                pf = Platform(image_path, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)  # Создаем платформу
                entities.add(pf)  # Добавляем платформу в группу спрайтов
                platforms.append(pf)  # Добавляем платформу в список платформ
            elif col == '$':  # Монета
                coin = Coin(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                entities.add(coin)  # Добавляем монету в группу спрайтов
            elif col == '+':  # Опыт
                xp = XP(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                entities.add(xp)  # Добавляем опыт в группу спрайтов
            elif col == '*':  # Звезда
                star = Star(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                entities.add(star)  # Добавляем звезду в группу спрайтов
            elif col == 'F':  # Объект Finish
                finish = Finish(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                entities.add(finish)  # Добавляем объект Finish в группу спрайтов

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

        # Обновляем монеты и другие объекты (кроме игрока)
        for entity in entities:
            if not isinstance(entity, Player):  # Не обновляем игрока здесь
                entity.update()  # Вызываем update для монет, опыта и звезд

        # Проверка столкновений с объектами
        collided_objects = pygame.sprite.spritecollide(hero, entities, dokill=False)
        for obj in collided_objects:
            if isinstance(obj, Coin):
                print("Монета собрана!")
                entities.remove(obj)  # Удаляем монету
            elif isinstance(obj, XP):
                print("Опыт получен!")
                entities.remove(obj)  # Удаляем опыт
            elif isinstance(obj, Star):
                print("Звезда собрана!")
                entities.remove(obj)  # Удаляем звезду
            elif isinstance(obj, Finish):
                print("Поздравляю! Вы достигли финиша!")  # Сообщение о достижении финиша

        # Отображение заднего фона и всех сущностей
        screen.blit(bg, (0, 0))  # Отображаем фон
        camera.update(hero)  # Обновляем камеру
        for spr in entities:
            screen.blit(spr.image, camera.apply(spr))

        pygame.display.update()  # Обновляем экран
        pygame.time.Clock().tick(FPS)  # Ограничиваем FPS игры до 120


# Запуск основной функции
if __name__ == "__main__":
    main()
