# Импортирование необходимых библиотек
from pygame import sprite, image, Rect, Surface, Color, QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_a, K_s, \
    K_d, MOUSEBUTTONDOWN, K_1, K_2, K_3
from random import shuffle
import pygame
import pickle
import time
import os
import webbrowser

# Установка размеров окна и платформы
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) = 1200, 800
PLATFORM_WIDTH = PLATFORM_HEIGHT = 42

# Скорость передвижения и ограничение кадров
MOVE_STEP = 21
FPS_LIMIT = 120

# Цвет заднего фона
BACKGROUND_COLOR = "#00000000"

# Переменные для представления уровня
ENTITIES = sprite.Group()  # Группа всех спрайтов
PLATFORMS = []  # Список платформ
PORTALS = []  # Список координат порталов
BONUSES = []  # Список действующих бонусов

# Переменные для подсчета собранных бонусов за время игры
COUNT_XP = 0
COUNT_COIN = 0
COUNT_STAR = 0

# Сохраняемые данные
STATE = {'skin': ['man', 6],
         'coins': 0,  # Монеты
         'levels': [0] + [-1] * 9,  # Прогресс ур-й
         'music': True,  # Состояние музыки
         'sound': True,  # Состояние звуковых эффектов
         'freezing': 0,
         'shield': 0,
         'magnet': 0,
         'record': 0,
         'score': 0,
         'lang': 'ru'
         }

# Состояние покупки скинов
SKINS = {'man': True, 'spectrum': False, 'froggy': False}  # словарь скинов

# Словарь с изображениями стен
WALL_IMAGES = {
    '□': 'textures\\blocks\\wall_1.png', '▔': 'textures\\blocks\\wall_2.png', '▁': 'textures\\blocks\\wall_3.png',
    '▕': 'textures\\blocks\\wall_4.png', '▎': 'textures\\blocks\\wall_5.png', '╔': 'textures\\blocks\\wall_6.png',
    '╗': 'textures\\blocks\\wall_7.png', '╚': 'textures\\blocks\\wall_8.png', '╝': 'textures\\blocks\\wall_9.png',
    '-': 'textures\\blocks\\wall_2.png', '⊓': 'textures\\blocks\\wall_10.png', '⊏': 'textures\\blocks\\wall_11.png',
    '⊔': 'textures\\blocks\\wall_12.png', '⊐': 'textures\\blocks\\wall_13.png', '=': 'textures\\blocks\\wall_14.png',
    '║': 'textures\\blocks\\wall_15.png', '┓': 'textures\\blocks\\wall_16.png', '┛': 'textures\\blocks\\wall_17.png',
    '┗': 'textures\\blocks\\wall_18.png', '┏': 'textures\\blocks\\wall_19.png', 'q': 'textures\\blocks\\wall_20.png',
    'w': 'textures\\blocks\\wall_21.png', 'e': 'textures\\blocks\\wall_22.png', 'r': 'textures\\blocks\\wall_23.png',
    't': 'textures\\blocks\\wall_24.png', 'y': 'textures\\blocks\\wall_25.png', 'u': 'textures\\blocks\\wall_26.png',
    'i': 'textures\\blocks\\wall_27.png', 'o': 'textures\\blocks\\wall_28.png', 'p': 'textures\\blocks\\wall_29.png',
    '[': 'textures\\blocks\\wall_30.png', 'A': 'textures\\blocks\\wall_A.png', ']': 'textures\\blocks\\wall_31.png',
    '"': 'textures\\blocks\\wall_32.png', ';': 'textures\\blocks\\wall_33.png', ':': 'textures\\blocks\\wall_34.png',
    ',': 'textures\\blocks\\wall_35.png', '<': 'textures\\blocks\\wall_36.png', '/': 'textures\\blocks\\wall_37.png',
    '?': 'textures\\blocks\\wall_38.png', 'б': 'textures\\blocks\\wall_39.png', 'в': 'textures\\blocks\\wall_40.png',
    'г': 'textures\\blocks\\wall_41.png', 'ж': 'textures\\blocks\\wall_42.png', 'з': 'textures\\blocks\\wall_43.png',
    'х': 'textures\\blocks\\wall_44.png', 'ъ': 'textures\\blocks\\wall_45.png',
}

# Словарь с изображениями шипов
SPIKE_IMAGES = {
    'z': 'textures\\spike\\spike_0.png', 'x': 'textures\\spike\\spike_1.png', 'c': 'textures\\spike\\spike_2.png',
    'v': 'textures\\spike\\spike_3.png',
    'b': 'textures\\spike\\spike_4.png', 'n': 'textures\\spike\\spike_5.png', 'm': 'textures\\spike\\spike_6.png',
    ',': 'textures\\spike\\spike_7.png',
    '@': 'textures\\spike\\spike_8.png', '#': 'textures\\spike\\spike_9.png', 'д': 'textures\\spike\\spike_10.png',
    'ё': 'textures\\spike\\spike_11.png',
}

# Словарь с изображениями ловушек
TRAP_IMAGES = {
    'a': 'textures\\trap\\trap_1.png', 's': 'textures\\trap\\trap_2.png', 'd': 'textures\\trap\\trap_3.png',
    'f': 'textures\\trap\\trap_4.png', 'g': 'textures\\trap\\trap_5.png', 'h': 'textures\\trap\\trap_6.png',
    'j': 'textures\\trap\\trap_7.png', 'k': 'textures\\trap\\trap_8.png', 'l': 'textures\\trap\\trap_9.png',
    '&': 'textures\\trap\\trap_10.png', '(': 'textures\\trap\\trap_11.png', 'л': 'textures\\trap\\trap_12.png',
    'ь': 'textures\\trap\\trap_13.png', 'ю': 'textures\\trap\\trap_14.png', '#': 'textures\\trap\\trap_15.png'
}

# Словарь для изображений трамплина
TRAMPOLINE_IMAGE = {
    '↙': 'textures\\trampoline\\trampoline_1.png', '↘': 'textures\\trampoline\\trampoline_2.png',
    '↗': 'textures\\trampoline\\trampoline_3.png',
    '↖': 'textures\\trampoline\\trampoline_4.png'
}

pygame.init()  # Инициализация Pygame
pygame.mixer.init()  # Инициализация модуля для работы со звуком

# Словарь со звуковыми эффектами
SOUNDS = {
    'coin': pygame.mixer.Sound('music and sounds/coin.wav'),
    'xp': pygame.mixer.Sound('music and sounds/xp.wav'),
    'star': pygame.mixer.Sound('music and sounds/star_1.wav'),
    'death': pygame.mixer.Sound('music and sounds/death.wav'),
    'ice box': pygame.mixer.Sound('music and sounds/ice box.wav')
}

# Каналы для воспроизведения звуковых эффектов
coin_channel = pygame.mixer.Channel(0)
death_channel = pygame.mixer.Channel(1)
xp_channel = pygame.mixer.Channel(2)
star_channel = pygame.mixer.Channel(3)
ice_channel = pygame.mixer.Channel(4)

# Инициализация собственного шрифта
font_path = 'fonts/zx_spectrum_7_bold.ttf'
font_size = 80
my_font = pygame.font.Font(font_path, font_size)


class Platform(sprite.Sprite):
    """Класс для представления платформы (стен).
    При инициализации объекта принимаются необходимые координаты
    расположения на карте и имя файла для наложения текстуры."""

    def __init__(self, image_path, x, y):
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для платформы
        self.image = image.load(image_path)  # Загружаем изображение платформы


class Player(sprite.Sprite):
    """Класс для представления игрока.
    Управляет анимацией движения персонажа, обработкой ввода
    с клавиатуры и взаимодействием с платформами.

    При инициализации объекта устанавливаются начальные значения
    для направления, изображения и анимации игрока.
    Обеспечивает перемещение игрока с учётом столкновений с
    платформами и обновляет отображение анимации в зависимости от
    направления движения."""

    def __init__(self, x, y):
        super().__init__()

        # Направление взгляда персонажа (начальное вправо вниз)
        self.up = self.left = False
        self.down = self.right = True

        # Направление передвижения
        self.direction = None

        # Загружаем кадры для различных направлений
        self.frames_down_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                      f"{STATE['skin'][0]}_botleft")
        self.frames_down_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                       f"{STATE['skin'][0]}_botright")
        self.frames_left_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                      f"{STATE['skin'][0]}_leftbot")
        self.frames_left_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                    f"{STATE['skin'][0]}_lefttop")
        self.frames_right_down = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                       f"{STATE['skin'][0]}_rightbot")
        self.frames_right_up = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                     f"{STATE['skin'][0]}_righttop")
        self.frames_up_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                    f"{STATE['skin'][0]}_topleft")
        self.frames_up_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), STATE['skin'][1],
                                                     f"{STATE['skin'][0]}_topright")

        # Загружаем кадры анимации движения
        self.flight_frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 4, "man_move")
        self.frames = self.frames_down_right  # Начальные кадры - смотрим вниз вправо
        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для игрока
        self.frame_rate = 8  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

        # Переменные для щита
        self.shielded = False  # Активен ли щит
        self.shielded_start = None  # Время начала щита
        self.invulnerable = False  # Неуязвим ли игрок
        self.invulnerability_start = None  # Время начала неуязвимости

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
        if self.shielded and (time.time() - self.shielded_start >= 10):
            self.shielded = False
            print('Щит диактивирован!')

        if self.invulnerable and (time.time() - self.invulnerability_start >= 2):
            self.invulnerable = False
            print('Неуязвимость закончилась!')

        # Проверяем, движется ли игрок
        if self.direction:  # Если персонаж движется, используем анимацию
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.frame_counter = 0
                self.index = (self.index + 1) % len(self.flight_frames)
                self.image = self.flight_frames[self.index]
        else:  # Если не движится, используем основную анимацию
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

        line = Fire(self)
        ENTITIES.add(line)

        # Обновляем позицию игрока
        self.rect.x += dx
        self.rect.y += dy

        # Проверка коллизий с платформами
        for platform in platforms:
            if (isinstance(platform, Platform) or isinstance(platform, Dart)) and self.rect.colliderect(platform.rect):
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

    def activate_shield(self):
        """Активация щита."""
        self.shielded = True
        print("Щит активирован!")

    def collide_with_enemy(self):
        """Обработка столкновения с врагом."""
        if self.shielded:
            print("Вы врезались в врага, щит заблокировал атаку!")
            self.invulnerable = True
            self.invulnerability_start = time.time()  # Запоминаем время начала неуязвимости
            self.shielded = False  # Сбрасываем щит после использования
        elif not self.invulnerable:
            print("Вы погибли!")
            return True


class Fire(sprite.Sprite):
    """Класс для представления следа полета персонажа."""

    def __init__(self, hero):
        super().__init__()
        x, y = hero.rect.x, hero.rect.y
        self.direction = hero.direction
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        if self.direction in 'left right':

            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/line'), 3, "line_lr")
        elif self.direction in 'up down':

            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/line'), 3, "line_tb")

        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        self.index = 0
        self.image = self.frames[self.index]
        self.time = 0

    def update(self):
        self.time += 1
        if self.time == 5:
            self.image = self.frames[1]
        elif self.time == 10:
            self.image = self.frames[2]
        elif self.time == 15:
            self.kill()


class Coin(sprite.Sprite):
    """Класс для представления монеты.
    Загружает анимацию монеты и управляет её отображением
    на экране. Монета анимируется при обновлении объекта."""

    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/coin'), 4, "coin")
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


class XP(sprite.Sprite):
    """Класс для представления опыта.
    Загружает и отображает изображение опыта на экране."""

    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/xp'), 2, "xp")
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.frame_rate = 30
        self.frame_counter = 0

    def update(self):
        # Логика анимации монеты
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]


class Star(sprite.Sprite):
    """Класс для представления звезды.
    Загружает и отображает изображение звезды на экране."""

    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/star', 'star_0.png'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class IceBox(sprite.Sprite):
    """Класс для представления IceBox.
    Блок не имеет коллизию для персонажа, но имеет для врагов."""

    def __init__(self, x, y):
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/ice box', 'ice_box_0.png'))


class Finish(sprite.Sprite):
    """Класс для представления финиша.
    Загружает анимацию финиша и управляет его отображением.
    При достижении игроком финиша, активирует меню перехода."""

    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/exit'), 2, "exit")
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.frame_rate = 15
        self.frame_counter = 0

    def update(self):
        # Логика анимации финиша
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]


class Spike(sprite.Sprite):
    """Класс для представления колючек.
    Загружает изображение шипа в зависимости от направления и
    управляет его отображением на экране. При соприкосновении
    персонажа с колючкой герой погибает и активируется окно проигрыша. """

    def __init__(self, x, y, spike_type):
        super().__init__()
        self.image = image.load(spike_type)  # Загружаем изображение платформы
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для шипа

    def get_spike_image_path(key):
        return os.path.join(os.path.dirname(__file__), "spike", SPIKE_IMAGES[key])  # Получаем путь


class Trap(sprite.Sprite):
    """Класс для представления ловушки.
    Загружает изображение ловушки и создает механизм активации
    шипов вокруг неё, когда игрок входит в её область видимости."""

    def __init__(self, x, y, trap_type):
        super().__init__()
        self.image = image.load(trap_type)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self, hero):
        if (self.rect.x, self.rect.y + 42) == (hero.rect.x, hero.rect.y):
            thorn = Thorn(self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'down')
            ENTITIES.add(thorn)
        elif (self.rect.x, self.rect.y - 42) == (hero.rect.x, hero.rect.y):
            thorn = Thorn(self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'up')
            ENTITIES.add(thorn)
        elif (self.rect.x + 42, self.rect.y) == (hero.rect.x, hero.rect.y):
            thorn = Thorn(self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'right')
            ENTITIES.add(thorn)
        elif (self.rect.x - 42, self.rect.y) == (hero.rect.x, hero.rect.y):
            thorn = Thorn(self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'left')
            ENTITIES.add(thorn)


class Thorn(sprite.Sprite):
    """Класс для представления шипа ловушки.
    Активируется в зависимости от нахождения игрока и анимирует
    отображение шипа в течение определенного времени."""

    def __init__(self, x, y, width, height, trap_name):
        super().__init__()
        self.trap_name = trap_name
        self.thorn_timer = 0
        self.activation_timer = 0  # Таймер для активации объекта
        self.image_name = None  # Добавляем новый атрибут
        self.image = None
        self.x = x
        self.y = y

        if trap_name == 'down':
            self.y += 42
        elif trap_name == 'up':
            self.y -= 42
        elif trap_name == 'left':
            self.x -= 42
        elif trap_name == 'right':
            self.x += 42
        self.rect = Rect(self.x, self.y, width, height)

    def update(self):
        if self.thorn_timer == 0:
            self.image_name = f'thorn_{self.trap_name}_1.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/thorn', self.image_name))

        elif self.thorn_timer == 30:
            self.image_name = f'thorn_{self.trap_name}_2.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/thorn', self.image_name))

        elif self.thorn_timer == 60:
            self.image_name = f'thorn_{self.trap_name}_3.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/thorn', self.image_name))

        elif self.thorn_timer == 120:
            self.image_name = f'thorn_{self.trap_name}_2.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'textures/thorn', self.image_name))

        elif self.thorn_timer == 130:
            self.kill()
            self.thorn_timer = 0

        self.thorn_timer += 1


class Fish(sprite.Sprite):
    """Класс для представления рыбы-фугу.
    Загружает анимацию движения рыбы и управляет её отображением
    на экране, а также поддерживает механизм анимации."""

    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/fish'), 16, "fish")
        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение
        self.image_name = f'fish_{self.index}.png'
        self.rect = Rect(x, y, PLATFORM_WIDTH * 3, PLATFORM_HEIGHT * 3)
        self.frame_rate = 10  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

        self.image_name = f'fish_{self.index}.png'


class Bat(sprite.Sprite):
    """Класс для представления летучей мыши.
    Летучая мышь летает из стороны в сторону.
    Соприкосновение игрока с мышью убивает его."""

    def __init__(self, bat_type, x, y):
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        self.frames_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/bat'), 5, "bat_left")
        self.frames_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/bat'), 5,
                                                  "bat_right")
        self.frames = self.frames_right

        if bat_type == '♖':
            self.direction = 'right'
        elif bat_type == '♜':
            self.direction = 'down'

        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение

        self.frame_rate = 10  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

        self.stop = False
        self.stop_time = 0  # Время остановки

    def update(self, platforms):
        # Анимация
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

        dx = dy = 0
        if not self.stop:
            if self.direction == 'right':
                dx += 2
            elif self.direction == 'left':
                dx -= 2
            elif self.direction == 'down':
                dy += 2
            elif self.direction == 'up':
                dy -= 2

            self.rect.x += dx
            self.rect.y += dy

        # Проверка коллизий с платформами
        for platform in platforms:
            if (isinstance(platform, Platform) or isinstance(platform, IceBox)) and self.rect.colliderect(
                    platform.rect):
                if dx < 0:  # Движение влево
                    self.rect.left = platform.rect.right
                elif dx > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                elif dy < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                elif dy > 0:  # Движение вниз
                    self.rect.bottom = platform.rect.top

                # Смена направления
                if self.direction == 'right':
                    self.direction = 'left'
                    self.frames = self.frames_left
                elif self.direction == 'left':
                    self.direction = 'right'
                    self.frames = self.frames_right
                elif self.direction == 'up':
                    self.direction = 'down'
                elif self.direction == 'down':
                    self.direction = 'up'

                self.stop = True
                self.stop_time = time.time()  # Запоминаем время столкновения
                break  # Выйти из цикла после первой коллизии

        # Проверяем, нужно ли продолжить движение
        if self.stop:
            if time.time() - self.stop_time >= 0.2:
                self.stop = False  # Сбрасываем статус остановки


class Dart(sprite.Sprite):  # ⇐⇑⇒⇓
    """Класс для представления арбалета.
       Блок с некой периодичностью выпускает стрелы."""

    def __init__(self, dart_type, x, y):
        super().__init__()
        self.dart_type, self.x, self.y = dart_type, x, y
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        if dart_type == '⇐':
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 2,
                                                "dart_left")
            self.x -= 42
        elif dart_type == '⇑':
            self.y -= 42
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 2, "dart_up")
        elif dart_type == '⇒':
            self.x += 42
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 2,
                                                "dart_right")
        elif dart_type == '⇓':
            self.y += 42
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 2,
                                                "dart_down")

        self.image = self.frames[0]  # Начальное изображение
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

    def update(self):
        self.frame_counter += 1
        if self.frame_counter == 80:
            self.image = self.frames[1]  # Начальное изображение
            arrow = Arrow(self.dart_type, self.x, self.y)
            ENTITIES.add(arrow)

        elif self.frame_counter == 95:
            self.image = self.frames[0]  # Начальное изображение
            self.frame_counter = 0


class Arrow(sprite.Sprite):
    """Класс для представления стрел.
    Убивают персонажа при столкновении."""

    def __init__(self, arror_type, x, y):
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.arror_type = arror_type

        if arror_type == '⇐':
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 1,
                                                "arrow_left")
        elif arror_type == '⇑':
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 1, "arrow_up")
        elif arror_type == '⇒':
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 1,
                                                "arrow_right")
        elif arror_type == '⇓':
            self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/dart'), 1,
                                                "arrow_down")
        self.image = self.frames[0]  # Начальное изображение

    def update(self, platforms):
        dx = dy = 0
        if self.arror_type == '⇒':
            dx += 4
        elif self.arror_type == '⇐':
            dx -= 4
        elif self.arror_type == '⇑':
            dy -= 4
        elif self.arror_type == '⇓':
            dy += 4

        self.rect.x += dx
        self.rect.y += dy
        # Проверка коллизий с платформами
        for platform in platforms:
            if (isinstance(platform, Platform) or isinstance(platform, IceBox)) and self.rect.colliderect(
                    platform.rect):
                if dx < 0:  # Движение влево
                    self.rect.left = platform.rect.right
                elif dx > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                self.kill()


class Teleport(sprite.Sprite):
    """Класс для представления телепорта.
    Перемещает персонажа между двумя парами телепортов."""

    def __init__(self, x, y, portal_id):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/portal'), 11, "portal")
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.frame_rate = 10
        self.frame_counter = 0
        self.portal_id = int(portal_id)

    def update(self, hero):
        # Проверяем столкновение с персонажем
        if self.rect.colliderect(hero.rect):
            # Находим соответствующий портал
            if self.portal_id % 2 == 0:  # Если портал 0, 2, 4, 6, 8
                next_id = self.portal_id + 1
            else:  # Если портал 1, 3, 5, 7, 9
                next_id = self.portal_id - 1

            new_cord = PORTALS[next_id][1]

            dx = dy = 0
            if hero.direction == 'up':
                dy -= 42
            elif hero.direction == 'down':
                dy += 42
            elif hero.direction == 'left':
                dx -= 42
            elif hero.direction == 'right':
                dx += 42

            hero.rect.x, hero.rect.y = new_cord[0] + dx, new_cord[1] + dy

        # Анимация телепорта
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]


class Camera:
    """Класс для представления камеры.
    Управляет отображением игрового мира относительно положения персонажа."""

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)  # Устанавливаем начальные параметры камеры

    def apply(self, target):
        return target.rect.move(self.state.topleft)  # Применяем положение камеры к целевому объекту

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)  # Обновляем состояние камеры


class Trampoline(sprite.Sprite):
    """Класс для представления трамплина."""

    def __init__(self, trampoline_type, x, y):
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для трамплина
        self.image = image.load(trampoline_type)  # Загружаем изображение трамплина
        self.direction = trampoline_type

    def update(self, hero):
        if (self.rect.x, self.rect.y) == (hero.rect.x, hero.rect.y):
            if '1' in self.direction:
                if hero.direction == 'down':
                    hero.direction = 'right'
                elif hero.direction == 'left':
                    hero.direction = 'up'

            elif '2' in self.direction:
                if hero.direction == 'down':
                    hero.direction = 'left'
                elif hero.direction == 'right':
                    hero.direction = 'up'

            elif '4' in self.direction:
                if hero.direction == 'up':
                    hero.direction = 'right'
                elif hero.direction == 'left':
                    hero.direction = 'down'

            elif '3' in self.direction:
                if hero.direction == 'up':
                    hero.direction = 'left'
                elif hero.direction == 'right':
                    hero.direction = 'down'


class GameOver(pygame.sprite.Sprite):
    """Класс для представления окна смерти."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/game over.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (600, 400)  # Позиционирование спрайта в центре экрана


class Restart(pygame.sprite.Sprite):
    """Класс для представления кнопки RESTART."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/restart.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (495, 510)  # Позиционирование спрайта в центре экрана


class Music(pygame.sprite.Sprite):
    """Класс для представления кнопки MUSIC."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/settings_music.png') if STATE['music'] else pygame.image.load(
            'images/settings_music0.png')  # Загрузка изображения# Загрузка изображения
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(400, 355))  # Установка координат кнопки

    def update_image(self):
        image_path = 'images/settings_music.png' if STATE['music'] else 'images/settings_music0.png'
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(400, 355))  # Установка координат кнопки


class Volume(pygame.sprite.Sprite):
    """Класс для представления кнопки VOLUME."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/settings_volume.png') if STATE['sound'] else pygame.image.load(
            'images/settings_volume0.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(505, 355))  # Установка координат кнопки

    def update_image(self):
        image_path = 'images/settings_volume.png' if STATE['sound'] else 'images/settings_volume0.png'
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(505, 355))  # Установка координат кнопки


class Quit(pygame.sprite.Sprite):
    """Класс для представления кнопки QUIT."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/settings_quit.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(715, 355))  # Установка координат кнопки


class FPS(pygame.sprite.Sprite):
    """Класс для представления кнопки FPS."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/settings_fps.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (21 * 4, 23 * 4))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(610, 355))  # Установка координат кнопки


class Cross(pygame.sprite.Sprite):
    """Класс для представления кнопки крестика."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/cross.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (30, 30))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(805, 240))  # Установка координат кнопки


class Donate(pygame.sprite.Sprite):
    """Класс для представления кнопки DONATE."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/donate.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (200, 65))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(400, 485))  # Установка координат кнопки


class USA(pygame.sprite.Sprite):
    """Класс для представления кнопки смена языка (en)."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/usa.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (16 * 5.7, 9 * 5.7))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(710, 490))  # Установка координат кнопки


class RUS(pygame.sprite.Sprite):
    """Класс для представления кнопки смены языка (ru)."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rus.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (16 * 5.7, 9 * 5.7))  # Растяжение изображения
        self.rect = self.image.get_rect(topleft=(610, 490))  # Установка координат кнопки


class Home(pygame.sprite.Sprite):
    """Класс для представления кнопки HOME."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/home.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (710, 510)  # Позиционирование спрайта в центре экрана


class Resume(pygame.sprite.Sprite):
    """Класс для представления кнопки RESUME."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/resume.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (495, 510)  # Позиционирование спрайта в центре экрана


class Death:
    """Класс для представления окна при смерти."""

    def __init__(self, screen, start_x=None, start_y=None, name_file=None):
        self.name_file = name_file
        self.start_x = start_x
        self.start_y = start_y

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.b_font = pygame.font.Font(self.font_path, 100)
        self.font80 = pygame.font.Font(self.font_path, 80)
        self.font40 = pygame.font.Font(self.font_path, 40)
        self.m_font = pygame.font.Font(self.font_path, 30)

        self.game_over = pygame.sprite.Group()

        self.game_over.add(GameOver())
        self.game_over.add(Restart())
        self.game_over.add(Home())

        self.main_menu()

    def draw_text(self, text, font, surface, x, y, color):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    # пишем свой код
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_click(pos)
            # обновляем значения
            # self.screen.fill((0, 0, 0))

            self.game_over.draw(self.screen)
            self.draw_text("Рестарт", self.font40, self.screen, 520, 505, "black")
            self.draw_text("Меню", self.font40, self.screen, 720, 505, "black")
            self.draw_text("Game over", self.b_font, self.screen, 600, 390, "black")
            if self.name_file:
                self.draw_text(f"Уровень {str(self.name_file[6:-4])}", self.b_font, self.screen, 585, 275, "black")
            else:
                self.draw_text('Аркада', self.b_font, self.screen, 600, 275, "black")

            # рисуем
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def check_click(self, pos):
        for sprite in self.game_over:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, Restart):
                    print('restart')
                    if self.name_file:
                        map_level(self.name_file, self.start_x, self.start_y)
                    else:
                        arcade()
                elif isinstance(sprite, Home):
                    print('back to lobby')
                    activate_menu()  # Активируем меню
                    pygame.quit()  # Закрываем текущее игровое окно


class Pause:
    """Класс для представления окна при паузе."""

    def __init__(self, screen, name_file=None):
        self.screen = screen
        self.name_file = name_file

        self.clock = pygame.time.Clock()
        self.running = True

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.b_font = pygame.font.Font(self.font_path, 100)
        self.font80 = pygame.font.Font(self.font_path, 80)
        self.m_font = pygame.font.Font(self.font_path, 30)
        self.font40 = pygame.font.Font(self.font_path, 40)

        self.game_pause = pygame.sprite.Group()

        self.game_pause.add(GameOver())
        self.game_pause.add(Resume())
        self.game_pause.add(Home())

        self.main_menu()

    def draw_text(self, text, font, surface, x, y, color):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    # пишем свой код
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_click(pos)
            # обновляем значения
            # self.screen.fill((0, 0, 0))

            self.game_pause.draw(self.screen)
            self.draw_text("Далее", self.font40, self.screen, 520, 505, "black")
            self.draw_text("Меню", self.font40, self.screen, 720, 505, "black")
            self.draw_text("Pause", self.b_font, self.screen, 600, 390, "black")
            if self.name_file:
                self.draw_text(f"Уровень {str(self.name_file[6:-4])}", self.b_font, self.screen, 585, 275, "black")
            else:
                self.draw_text('Аркада', self.b_font, self.screen, 600, 275, "black")

            # рисуем
            pygame.display.flip()
            self.clock.tick(30)
        # pygame.quit()

    def check_click(self, pos):
        for sprite in self.game_pause:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, Resume):
                    print('resume')
                    self.running = False
                elif isinstance(sprite, Home):
                    print('back to lobby')
                    activate_menu()  # Активируем меню
                    pygame.quit()  # Закрываем текущее игровое окно


class Settings:
    """Класс для представления окна при открытии настроек."""

    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'

        self.font100 = pygame.font.Font(self.font_path, 100)
        self.font80 = pygame.font.Font(self.font_path, 80)
        self.font40 = pygame.font.Font(self.font_path, 40)
        self.font30 = pygame.font.Font(self.font_path, 30)

        self.settings = pygame.sprite.Group()
        self.settings.add(GameOver())
        self.settings.add(Music())
        self.settings.add(Volume())
        self.settings.add(FPS())
        self.settings.add(Quit())
        self.settings.add(Cross())
        self.settings.add(Donate())
        self.settings.add(USA())
        self.settings.add(RUS())

        self.main_menu()

    def main_menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_click(pos)
            # обновляем значения
            # self.screen.fill((0, 0, 0))

            self.settings.draw(self.screen)
            draw_text("Настройки", self.font100, self.screen, 420, 225, "black")
            # рисуем
            pygame.display.flip()
        pygame.quit()

    def check_click(self, pos):
        for sprite in self.settings:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, Music):
                    print('mus')
                    STATE['music'] = not STATE['music']
                    sprite.update_image()
                    print(STATE['music'])

                    update_background_music()

                elif isinstance(sprite, Volume):
                    print('vol')
                    STATE['sound'] = not STATE['sound']
                    sprite.update_image()
                    print(STATE['sound'])

                elif isinstance(sprite, Quit):
                    print('quit')
                    pygame.quit()
                    exit()

                elif isinstance(sprite, FPS):
                    print('fps')

                elif isinstance(sprite, Donate):
                    print('donate')
                    webbrowser.open('https://yoomoney.ru/fundraise/183N31A6QH5.250130')  # Открытие ссылки

                elif isinstance(sprite, USA):
                    STATE['lang'] = 'eng'

                elif isinstance(sprite, RUS):
                    STATE['lang'] = 'ru'

                elif isinstance(sprite, Cross):
                    print('back to lobby')
                    activate_menu()  # Активируем меню
                    pygame.quit()  # Закрываем текущее игровое окно


class PauseButton(pygame.sprite.Sprite):
    """Класс для представления кнопки паузы."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/menu_pause.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIN_WIDTH - 60, 20)


class Water(sprite.Sprite):
    """Класс для представления воды в аркаде.
    Вода равномерно поднимается и убивает персонажа при столкновении."""

    def __init__(self, level, hero):
        super().__init__()
        self.rect = Rect(PLATFORM_WIDTH * 2, hero.rect.y + 500, PLATFORM_WIDTH * 11, PLATFORM_HEIGHT * 11)
        self.image = Surface((PLATFORM_WIDTH * 11, PLATFORM_HEIGHT * 11))
        self.image.fill(Color('#66ffe3'))

    def update(self):
        self.rect.y -= 2.5


class Magnet(sprite.Sprite):
    """Класс для представления магнита (бонуса).
    Собирает все сокровища в увеличенном радиусе от персонажа."""

    def __init__(self, hero):
        super().__init__()
        self.rect = Rect(hero.rect.x - PLATFORM_WIDTH * 1.5, hero.rect.y - PLATFORM_HEIGHT * 1.5, PLATFORM_WIDTH * 4,
                         PLATFORM_HEIGHT * 4)
        self.start_time = time.time()

    def update(self, hero):  # 695
        self.rect.x = hero.rect.x - PLATFORM_WIDTH
        self.rect.y = hero.rect.y - PLATFORM_HEIGHT

        if time.time() - self.start_time >= 10:
            print('stop magnet')
            BONUSES.remove(self)
            self.kill()

        # Проверка столкновения с монетами, опытом и звездами
        collided_entities = pygame.sprite.spritecollide(self, ENTITIES, dokill=False)
        for entity in collided_entities:
            if isinstance(entity, Coin):
                print("Монета собрана магнитом!")
                coin_channel.play(SOUNDS['coin'])
                coin_channel.set_volume(0.1)
                ENTITIES.remove(entity)
            elif isinstance(entity, XP):
                print("Опыт собран магнитом!")
                xp_channel.play(SOUNDS['xp'])
                xp_channel.set_volume(0.05)
                ENTITIES.remove(entity)
            elif isinstance(entity, Star):
                print("Звезда собрана магнитом!")
                star_channel.play(SOUNDS['star'])
                star_channel.set_volume(0.1)
                ENTITIES.remove(entity)


# Функция для настройки положения камеры
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


# Функция для загрузки уровня из txt файла
def load_level_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            level = file.readlines()
        if not level:
            raise ValueError('Файл уровня пуст.')
        return [line.strip() for line in level]  # Возвращаем строки уровня без изменений
    except FileNotFoundError:
        print(f'Ошибка: Файл не найден: {filename}')
        return []
    except ValueError as e:
        print(e)
        return []


# функция для сохранения игры
def save_game(state):
    with open('savegame.pkl', 'wb') as f:
        pickle.dump(state, f)


# функция для загрузки сохраненной игры
def load_game():
    if os.path.exists('savegame.pkl'):
        with open('savegame.pkl', 'rb') as f:
            state = pickle.load(f)
        return state
    return None


# Функцию для закрытия окна игры и открытия лобби
def activate_menu():
    from lobby import Lobby
    Lobby()


# Функция для воспроизведения музыки
def set_background_music():
    if STATE.get('music', False):  # Проверка состояния музыки
        pygame.mixer.music.load('music and sounds/game.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.01)


# Функция для обновления музыки
def update_background_music():
    if STATE['music']:
        if not pygame.mixer.get_init():  # Проверка, инициализирован ли модулями звука
            pygame.mixer.init()
        pygame.mixer.music.load('music and sounds/menu.mp3')
        pygame.mixer.music.play(-1)  # Воспроизводить бесконечно
        pygame.mixer.music.set_volume(0.1)  # Установка громкости
    else:
        pygame.mixer.music.stop()  # Остановка музыки если 'music' выключен


# Функция для обнуления собранных сокровищ
def reset_bonuses():
    global COUNT_XP, COUNT_COIN, COUNT_STAR
    COUNT_XP, COUNT_COIN, COUNT_STAR = 0, 0, 0


# Функция для обнуления уровня
def reset_level():
    global ENTITIES, PLATFORMS, PORTALS
    ENTITIES.empty()  # удаляем все спрайты
    PLATFORMS.clear()  # Удаляем все платформы
    BONUSES.clear()
    PORTALS.clear()


# Функция для отрисовки текста
def draw_text(text, font, surface, x, y, color):
    textobj = font.render(text, True, color)
    textrect = Rect(x, y, 100, 100)
    surface.blit(textobj, textrect)


# Функция для инициализации уровня
def load_platform(level):
    for y, row in enumerate(level):
        for x, col in enumerate(row):
            if col in WALL_IMAGES and col != 'A':  # Создание платформы (стены)
                pf = Platform(WALL_IMAGES[col], x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(pf)
                PLATFORMS.append(pf)

            elif col == '$':  # Создание монеты
                coin = Coin(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(coin)

            elif col == '+':  # Создание опыта
                xp = XP(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(xp)

            elif col == '*':  # Создание звезды
                star = Star(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(star)

            elif col == 'F':  # Создаем финиш
                finish = Finish(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(finish)

            elif col in SPIKE_IMAGES:  # Создаем колючку
                spike = Spike(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, SPIKE_IMAGES[col])
                ENTITIES.add(spike)

            elif col in TRAP_IMAGES:  # Создаем ловушку
                trap = Trap(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, TRAP_IMAGES[col])
                ENTITIES.add(trap)

                pf = Platform(WALL_IMAGES['A'], x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                PLATFORMS.append(pf)

            elif col in TRAMPOLINE_IMAGE:  # Создает трамплин
                tramp = Trampoline(TRAMPOLINE_IMAGE[col], x * PLATFORM_WIDTH,
                                   y * PLATFORM_HEIGHT)  # Передаем тип трамплина
                ENTITIES.add(tramp)

            elif col == 'A':  # Создание рыбы-фугу
                fish = Fish(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(fish)

                pf = Platform(WALL_IMAGES['A'], x * PLATFORM_WIDTH + PLATFORM_WIDTH,
                              y * PLATFORM_HEIGHT + PLATFORM_HEIGHT)  # Создаем невидимую платформу
                ENTITIES.add(pf)
                PLATFORMS.append(pf)

            elif col in '♜♖':
                bat = Bat(col, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(bat)

            elif col in '⇑⇒⇓⇐':
                dart = Dart(col, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                PLATFORMS.append(dart)
                ENTITIES.add(dart)

            elif col == '⊞':
                ice_box = IceBox(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(ice_box)
                PLATFORMS.append(ice_box)

            elif col in '0123456789':
                teleport = Teleport(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, col)
                ENTITIES.add(teleport)
                PLATFORMS.append(teleport)
                PORTALS.append((col, (x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)))
                print((col, (x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)))
    PORTALS.sort(key=lambda x: x[0])


# Функция для обновления всех энтити
def update_entity(hero, freezing):
    hero.update(PLATFORMS)
    if not freezing:
        for entity in ENTITIES:
            if isinstance(entity, Trap) or isinstance(entity, Trampoline) or isinstance(entity, IceBox) or isinstance(
                    entity, Teleport):
                entity.update(hero)
            elif isinstance(entity, Bat) or isinstance(entity, Arrow):
                entity.update(PLATFORMS)
            elif not isinstance(entity, Player):
                entity.update()


# Функция для обновления бонусов
def update_bonuse(hero):
    for bonus in BONUSES:
        bonus.update(hero)


# Функция для проверки столкновения
def check_collided(collided_objects, hero, name_file=None):
    global COUNT_COIN, COUNT_XP, COUNT_STAR, STATE
    for obj in collided_objects:
        # Проверка столкновения игрока со смертельно опасными объектами
        if isinstance(obj, Spike) or (isinstance(obj, Thorn) and obj.image_name is not None and (
                '2' in obj.image_name or '3' in obj.image_name)) or (
                isinstance(obj, Fish) and int(obj.image_name[5:-4]) in list(range(6, 15)) or (
                isinstance(obj, Bat)) or isinstance(obj, Arrow) or isinstance(obj, Water)):
            if hero.collide_with_enemy():
                if STATE['sound']:
                    death_channel.play(SOUNDS['death'])
                    death_channel.set_volume(0.2)
                save_game(STATE)
                return True
        if isinstance(obj, Coin):
            COUNT_COIN += 1
            print(f"Монета собрана! ({COUNT_COIN})")
            if STATE['sound']:
                coin_channel.play(SOUNDS['coin'])
                coin_channel.set_volume(0.1)
            ENTITIES.remove(obj)
        elif isinstance(obj, XP):
            COUNT_XP += 1
            print(f"Опыт получен! ({COUNT_XP})")
            if STATE['sound']:
                xp_channel.play(SOUNDS['xp'])
                xp_channel.set_volume(0.05)
            ENTITIES.remove(obj)
        elif isinstance(obj, Star):
            COUNT_STAR += 1
            print(f"Звезда собрана! ({COUNT_STAR})")
            if STATE['sound']:
                star_channel.play(SOUNDS['star'])
                star_channel.set_volume(0.1)
            ENTITIES.remove(obj)
        elif isinstance(obj, IceBox):
            print('Ice Box разбит')
            if STATE['sound']:
                star_channel.play(SOUNDS['ice box'])
                star_channel.set_volume(0.05)
            ENTITIES.remove(obj)
            PLATFORMS.remove(obj)
        elif isinstance(obj, Finish):
            print("Поздравляю! Вы достигли финиша!")
            if STATE['sound']:
                SOUNDS['coin'].set_volume(0.05)
            STATE['levels'][int(name_file[6:-4]) - 1] = COUNT_STAR
            STATE['coins'] += COUNT_COIN
            print(STATE['coins'])
            print(STATE['levels'])

            save_game(STATE)
            activate_menu()  # Активируем меню
            pygame.quit()  # Закрываем текущее игровое окно

            # Основная функция игры


# Попытка загрузить сохранение
loaded_state = load_game()
if loaded_state is not None:
    STATE = loaded_state
STATE['score'] = 0


# Основной режим игры
def map_level(name_file, start_x, start_y):
    game_over_active = False
    paused = False
    freezing = False
    freezing_start = None

    # Очищаем данные перед загрузкой нового уровня
    reset_bonuses()
    reset_level()

    # Запуск музыки
    set_background_music()

    # Создаем дисплей для расположения всех объектов
    pygame.init()  # Инициализация Pygame
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна игры

    bg = Surface(DISPLAY)  # Создаем поверхность для фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон цветом

    # Создаем экземпляр игрока
    hero = Player(start_x * PLATFORM_WIDTH, start_y * PLATFORM_HEIGHT)
    ENTITIES.add(hero)  # Добавляем игрока в группу спрайтов

    # Определение уровня в виде строк
    level = load_level_from_file(os.path.join("levels", name_file))

    if not level:  # Если уровень оказался пустым
        print("Ошибка: Не удалось загрузить уровень.")
        activate_menu()  # Активируем меню
        pygame.quit()  # Закрываем текущее игровое окно

    # Заполнение платформ и объектов из level_n.txt
    load_platform(level)

    # Определяем размеры уровня
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    # Создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Создаем кнопку паузы
    pause_button = PauseButton()

    while True:
        if not game_over_active and not paused:  # Проверка состояния игры
            keys = pygame.key.get_pressed()  # Получаем состояние клавиш
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_button.rect.collidepoint(pos):
                        paused = not paused
                    print("Paused:", paused)
                elif event.type == KEYDOWN:  # Обработка нажатий клавиш
                    if event.key == K_LEFT or event.key == K_a:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'left')
                    elif event.key == K_RIGHT or event.key == K_d:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'right')
                    elif event.key == K_UP or event.key == K_w:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'up')
                    elif event.key == K_DOWN or event.key == K_s:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'down')
                    elif event.key == K_1:
                        magnet = Magnet(hero)
                        BONUSES.append(magnet)
                        print('start magnet')
                    elif event.key == K_2:
                        freezing = True
                        print('start freez')
                    elif event.key == K_3:
                        hero.shielded = True
                        hero.shielded_start = time.time()
                        print('start shield')

            if freezing:
                if not freezing_start:
                    freezing_start = time.time()
                elif time.time() - freezing_start >= 10:
                    print('stop freezing')
                    freezing = False
                    freezing_start = None

            # Обновляем все объекты и бонусы
            update_entity(hero, freezing)
            update_bonuse(hero)

            # Проверка столкновений с объектами
            collided_objects = pygame.sprite.spritecollide(hero, ENTITIES, dokill=False)
            game_over_active = check_collided(collided_objects, hero, name_file)

            # Отображение заднего фона и всех сущностей
            screen.blit(bg, (0, 0))  # Отображаем фон
            camera.update(hero)  # Обновляем камеру

            for spr in ENTITIES:
                if spr.image is not None:  # Проверка, что изображение не равно None
                    screen.blit(spr.image, camera.apply(spr))

            # Рисуем кнопку паузы
            screen.blit(pause_button.image, pause_button.rect)
            screen.blit(hero.image, camera.apply(hero))
            pygame.display.update()  # Обновляем экран
            pygame.time.Clock().tick(FPS_LIMIT)  # Ограничиваем FPS игры до 120

        elif paused:
            pygame.mixer.music.pause()
            Pause(screen, name_file)
            paused = False
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.stop()  # Останавливаем музыку
            Death(screen, start_x, start_y, name_file)


# Основная функция аркады
def arcade():
    game_over_active = False
    paused = False
    block = False
    first_movement = False
    freezing = False
    freezing_start = None

    # Очищаем данные перед загрузкой нового уровня
    reset_bonuses()
    reset_level()

    # Запуск музыки
    set_background_music()

    # Создаем дисплей для расположения всех объектов
    pygame.init()  # Инициализация Pygame
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна игры

    bg = Surface(DISPLAY)  # Создаем поверхность для фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон цветом

    # Генерируем карту из элементов
    arcades = [('arcade_1.txt', (7, 91)), ('arcade_2.txt', (7, 116)), ('arcade_3.txt', (7, 138)),
               ("arcade_4.txt", (7, 146))]
    shuffle(arcades)

    id_arcade = 0
    start_x, start_y = arcades[0][1]

    # Создаем экземпляр игрока
    hero = Player(start_x * PLATFORM_WIDTH, start_y * PLATFORM_HEIGHT)
    ENTITIES.add(hero)  # Добавляем игрока в группу спрайтов

    # Определение уровня в виде строк
    level = load_level_from_file(os.path.join("levels", arcades[0][0]))

    if not level:  # Если уровень оказался пустым
        print("Ошибка: Не удалось загрузить уровень.")
        activate_menu()  # Активируем меню
        pygame.quit()  # Закрываем текущее игровое окно

    # Заполнение платформ и объектов из level_n.txt
    load_platform(level)

    # Определяем размеры уровня
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    # Создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Создаем кнопку паузы и переменную с состоянием ее нажатия
    pause_button = PauseButton()

    water = Water(level, hero)
    ENTITIES.add(water)

    while True:
        if not game_over_active and not paused:  # Проверка состояния игры
            keys = pygame.key.get_pressed()  # Получаем состояние клавиш
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_button.rect.collidepoint(pos):
                        paused = not paused
                    print("Paused:", paused)
                elif event.type == KEYDOWN:  # Обработка нажатий клавиш
                    first_movement = True
                    if event.key == K_LEFT or event.key == K_a:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'left')
                    elif event.key == K_RIGHT or event.key == K_d:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'right')
                    elif event.key == K_UP or event.key == K_w:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'up')
                    elif event.key == K_DOWN or event.key == K_s:
                        hero.start_move(keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN], 'down')
                    elif event.key == K_1:
                        magnet = Magnet(hero)
                        BONUSES.append(magnet)
                        STATE['magnet'] -= 1
                        print('start magnet')
                    elif event.key == K_2:
                        freezing = True
                        print('start freez')
                        STATE['freezing'] -= 1
                    elif event.key == K_3:
                        hero.shielded = True
                        hero.shielded_start = time.time()
                        print('start shield')
                        STATE['shield'] -= 1

            if freezing:
                if not freezing_start:
                    freezing_start = time.time()
                elif time.time() - freezing_start >= 10:
                    print('stop freezing')
                    freezing = False
                    freezing_start = None

            # Обновляем все объекты
            update_entity(hero, freezing)
            update_bonuse(hero)

            # Проверка столкновений с объектами
            collided_objects = pygame.sprite.spritecollide(hero, ENTITIES, dokill=False)
            game_over_active = check_collided(collided_objects, hero)

            # Отображение заднего фона и всех сущностей
            screen.blit(bg, (0, 0))  # Отображаем фон
            camera.update(hero)  # Обновляем камеру

            for spr in ENTITIES:
                if spr.image is not None:  # Проверка, что изображение не равно None
                    screen.blit(spr.image, camera.apply(spr))

            # Рисуем кнопку паузы
            screen.blit(pause_button.image, pause_button.rect)
            screen.blit(hero.image, camera.apply(hero))

            # Отображение текущего счета
            draw_text(text=('Счёт: ' + str(COUNT_XP)), font=my_font, surface=screen, x=30, y=-10, color=(254, 254, 10))

            pygame.display.update()  # Обновляем экран
            pygame.time.Clock().tick(FPS_LIMIT)  # Ограничиваем FPS игры до 120

        if hero.rect.y <= 500:
            block = False
            id_arcade += 1

            if id_arcade > 3:
                shuffle(arcades)
                id_arcade = 0

            # Очищаем данные перед загрузкой нового уровня
            reset_level()

            # Определение уровня в виде строк
            level = load_level_from_file(os.path.join("levels", arcades[id_arcade][0]))

            start_x, start_y = 7, len(level) - 12

            # Создаем экземпляр игрока
            hero = Player(start_x * PLATFORM_WIDTH, start_y * PLATFORM_HEIGHT)
            hero.direction = 'up'
            ENTITIES.add(hero)  # Добавляем игрока в группу спрайтов

            if not level:  # Если уровень оказался пустым
                print("Ошибка: Не удалось загрузить уровень.")
                activate_menu()  # Активируем меню
                pygame.quit()  # Закрываем текущее игровое окно

            # Заполнение платформ и объектов из level_n.txt
            load_platform(level)

            # Определяем размеры уровня
            total_level_width = len(level[0]) * PLATFORM_WIDTH
            total_level_height = len(level) * PLATFORM_HEIGHT

            # Создаем камеру
            camera = Camera(camera_configure, total_level_width, total_level_height)

        if not hero.direction and not block:
            for i in range(2, 13):
                pf = Platform(WALL_IMAGES['□'], i * PLATFORM_WIDTH, (hero.rect.y + 300))
                ENTITIES.add(pf)
                PLATFORMS.append(pf)

                water = Water(level, hero)
                ENTITIES.add(water)

            block = True

        if paused:
            pygame.mixer.music.pause()
            Pause(screen)
            paused = False
            pygame.mixer.music.unpause()

        if game_over_active:
            STATE['score'] = COUNT_XP
            STATE['record'] = max(STATE['record'], COUNT_XP)
            game_over_active = False
            Death(screen)
            pygame.mixer.music.stop()  # Останавливаем музыку
