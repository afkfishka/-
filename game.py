# Импортирование необходимых библиотек
from pygame import sprite, image, Rect, Surface, Color, QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN
import pygame
import pickle
import os

# Установка размеров окна и платформы
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) = 1200, 800
PLATFORM_WIDTH = PLATFORM_HEIGHT = 42

# Скорость передвижения и ограничение кадров
MOVE_STEP = 21
FPS = 120

# Цвет заднего фона
BACKGROUND_COLOR = "#00000000"

# Переменные для представления уровня
ENTITIES = sprite.Group()  # Группа всех спрайтов
PLATFORMS = []  # Список платформ

# Сохраняемые данные
STATE = {'coins': 0,  # Монеты
         'levels': [0] + [-1] * 9,  # Прогресс ур-й
         'music': None,  # Состояние музыки
         'sound': None}  # Состояние звуковых эффектов

# Словарь с изображениями стен
WALL_IMAGES = {
    '□': 'wall_1.png', '▔': 'wall_2.png', '▁': 'wall_3.png', '▕': 'wall_4.png', '▎': 'wall_5.png',
    '╔': 'wall_6.png', '╗': 'wall_7.png', '╚': 'wall_8.png', '╝': 'wall_9.png', '-': 'wall_2.png',
    '⊓': 'wall_10.png', '⊏': 'wall_11.png', '⊔': 'wall_12.png', '⊐': 'wall_13.png', '=': 'wall_14.png',
    '║': 'wall_15.png', '┓': 'wall_16.png', '┛': 'wall_17.png', '┗': 'wall_18.png', '┏': 'wall_19.png',
    'q': 'wall_20.png', 'w': 'wall_21.png', 'e': 'wall_22.png', 'r': 'wall_23.png', 't': 'wall_24.png',
    'y': 'wall_25.png', 'u': 'wall_26.png', 'i': 'wall_27.png', 'o': 'wall_28.png', 'p': 'wall_29.png',
    '[': 'wall_30.png', 'A': 'wall_A.png', ']': 'wall_31.png', '"': 'wall_32.png'
}

# Словарь с изображениями шипов
SPIKE_IMAGES = {
    'z': 'spike_0.png', 'x': 'spike_1.png', 'c': 'spike_2.png', 'v': 'spike_3.png',
    'b': 'spike_4.png', 'n': 'spike_5.png', 'm': 'spike_6.png', ',': 'spike_7.png',
}

# Словарь с изображениями ловушек
TRAP_IMAGES = {
    'a': 'trap_1.png', 's': 'trap_2.png', 'd': 'trap_3.png',
    'f': 'trap_4.png', 'g': 'trap_5.png', 'h': 'trap_6.png',
    'j': 'trap_7.png', 'k': 'trap_8.png', 'l': 'trap_9.png',
}

# Словарь для изображений трамплина
TRAMPOLINE_IMAGE = {
    '↙': 'trampoline_1.png', '↘': 'trampoline_2.png', '↗': 'trampoline_3.png', '↖': 'trampoline_4.png'
}

pygame.init()  # Инициализация Pygame
pygame.mixer.init()  # Инициализация модуля для работы со звуком

# Словарь со звуковыми эффектами
SOUNDS = {
    'coin': pygame.mixer.Sound('music and sounds/coin.wav'),
    'xp': pygame.mixer.Sound('music and sounds/xp.wav'),
    'star': pygame.mixer.Sound('music and sounds/star_1.wav'),
    'death': pygame.mixer.Sound('music and sounds/death.wav'),
}

coin_channel = pygame.mixer.Channel(0)
death_channel = pygame.mixer.Channel(1)
xp_channel = pygame.mixer.Channel(2)
star_channel = pygame.mixer.Channel(3)


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

        # Обновляем позицию игрока
        self.rect.x += dx
        self.rect.y += dy

        # Проверка коллизий с платформами
        for platform in platforms:
            if isinstance(platform, Platform) and self.rect.colliderect(platform.rect):
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


class Coin(sprite.Sprite):
    """Класс для представления монеты.
    Загружает анимацию монеты и управляет её отображением
    на экране. Монета анимируется при обновлении объекта."""

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


class XP(sprite.Sprite):
    """Класс для представления опыта.
    Загружает и отображает изображение опыта на экране."""

    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'xp', 'xp_0.png'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Star(sprite.Sprite):
    """Класс для представления звезды.
    Загружает и отображает изображение звезды на экране."""

    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'star', 'star_0.png'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Finish(sprite.Sprite):
    """Класс для представления финиша.
    Загружает анимацию финиша и управляет его отображением.
    При достижении игроком финиша, активирует меню перехода."""

    def __init__(self, x, y):
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'exit'), 2, "exit")
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
        self.image = image.load(Spike.get_spike_image_path(spike_type))  # Исправлено: добавлено 'Spike.'
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Определяем прямоугольник для шипа

    def get_spike_image_path(key):
        return os.path.join(os.path.dirname(__file__), "spike", SPIKE_IMAGES[key])  # Получаем путь


class Trap(sprite.Sprite):
    """Класс для представления ловушки.
    Загружает изображение ловушки и создает механизм активации
    шипов вокруг неё, когда игрок входит в её область видимости."""

    def __init__(self, x, y, trap_type):
        super().__init__()
        self.image = image.load(os.path.join(os.path.dirname(__file__), 'trap', TRAP_IMAGES[trap_type]))
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
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'thorn', self.image_name))

        elif self.thorn_timer == 30:
            self.image_name = f'thorn_{self.trap_name}_2.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'thorn', self.image_name))

        elif self.thorn_timer == 60:
            self.image_name = f'thorn_{self.trap_name}_3.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'thorn', self.image_name))

        elif self.thorn_timer == 120:
            self.image_name = f'thorn_{self.trap_name}_2.png'  # Устанавливаем имя
            self.image = image.load(os.path.join(os.path.dirname(__file__), 'thorn', self.image_name))

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
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'fish'), 16, "fish")
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
    def __init__(self, bat_type, x, y):  # ♖♜
        super().__init__()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        self.frames_left = load_animation_frames(os.path.join(os.path.dirname(__file__), 'bat'), 5, "bat_left")
        self.frames_right = load_animation_frames(os.path.join(os.path.dirname(__file__), 'bat'), 5, "bat_right")
        self.frames = self.frames_right

        if bat_type == '♖':
            self.direction = 'right'
        elif bat_type == '♜':
            self.direction = 'down'

        self.index = 0  # Индекс текущего кадра
        self.image = self.frames[self.index]  # Начальное изображение

        self.frame_rate = 10  # Частота смены кадров
        self.frame_counter = 0  # Счетчик кадров для управления анимацией

    def update(self, platforms):
        # Анимация
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

        dx = dy = 0
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
            if isinstance(platform, Platform) and self.rect.colliderect(platform.rect):
                if dx < 0:  # Движение влево
                    self.rect.left = platform.rect.right
                elif dx > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
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
        self.image = image.load(self.get_trampoline_image_path(trampoline_type))  # Загружаем изображение трамплина
        self.direction = trampoline_type

    def update(self, hero):
        if (self.rect.x, self.rect.y) == (hero.rect.x, hero.rect.y):
            if self.direction == '↙':
                if hero.direction == 'down':
                    hero.direction = 'right'
                elif hero.direction == 'left':
                    hero.direction = 'up'

            elif self.direction == '↘':
                if hero.direction == 'down':
                    hero.direction = 'left'
                elif hero.direction == 'right':
                    hero.direction = 'up'

            elif self.direction == '↖':
                if hero.direction == 'up':
                    hero.direction = 'right'
                elif hero.direction == 'left':
                    hero.direction = 'down'

            elif self.direction == '↗':
                if hero.direction == 'up':
                    hero.direction = 'left'
                elif hero.direction == 'right':
                    hero.direction = 'down'

    def get_trampoline_image_path(self, key):
        return os.path.join(os.path.dirname(__file__), 'trampoline', TRAMPOLINE_IMAGE[key])


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/game over.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (600, 400)  # Позиционирование спрайта в центре экрана


class Restart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/restart.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (517, 488)  # Позиционирование спрайта в центре экрана


class Home(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/home.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (684, 488)  # Позиционирование спрайта в центре экрана


class Death:
    def __init__(self, screen, name_file, start_x, start_y):
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
            self.draw_text("Рестарт", self.m_font, self.screen, 532, 487, "black")
            self.draw_text("Меню", self.m_font, self.screen, 697, 487, "black")
            self.draw_text("Game over", self.font80, self.screen, 600, 390, "black")
            self.draw_text("Уровень", self.font, self.screen, 570, 305, "black")
            self.draw_text(str(self.name_file[6:-4]), self.font, self.screen, 680, 305, "black")

            # рисуем
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def check_click(self, pos):
        for sprite in self.game_over:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, Restart):
                    print('restart')
                    main(self.name_file, self.start_x, self.start_y)
                elif isinstance(sprite, Home):
                    print('back to lobby')
                    activate_menu()  # Активируем меню
                    pygame.quit()  # Закрываем текущее игровое окно


# Функция для получения пути к изображению платформы (стены)
def get_wall_image_path(key):
    return os.path.join(os.path.dirname(__file__), "blocks", WALL_IMAGES[key])


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
    with open('savegame.pkl', 'rb') as f:
        state = pickle.load(f)
    return state


# Функцию для закрытия окна игры и открытия лобби
def activate_menu():
    from lobby import Lobby
    Lobby()


# Основная функция игры
def main(name_file, start_x, start_y):
    game_over_active = False

    # Очищаем данные перед загрузкой нового уровня
    ENTITIES.empty()  # удаляем все спрайты
    PLATFORMS.clear()  # Удаляем все платформы

    count_star = 0  # Обнуляем звезды, собранные за уровень
    count_coin = 0  # Обнуляем монеты, собранные за уровень

    # Создаем дисплей для расположения всех объектов
    pygame.init()  # Инициализация Pygame
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна игры
    pygame.display.set_caption("Тайны подземелий")  # Установка заголовка окна

    bg = Surface(DISPLAY)  # Создаем поверхность для фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон цветом

    # Запуск музыки
    pygame.mixer.music.stop()  # Останавливаем музыку из меню
    pygame.mixer.music.load('music and sounds/game.mp3')  # Загружаем музыку для воспроизведения во время игры
    pygame.mixer.music.play(-1)  # Воспроизводить бесконечно
    pygame.mixer.music.set_volume(0.01)  # Установка громкости на 1%

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
    for y, row in enumerate(level):
        for x, col in enumerate(row):
            if col in WALL_IMAGES and col != 'A':  # Создание платформы (стены)
                image_path = get_wall_image_path(col)  # Получаем изображение для стены
                pf = Platform(image_path, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
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
                spike = Spike(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, col)
                ENTITIES.add(spike)

            elif col in TRAP_IMAGES:  # Создаем ловушку
                trap = Trap(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, col)
                ENTITIES.add(trap)

                image_path = get_wall_image_path('A')  # Создаем невидимую платформу
                pf = Platform(image_path, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                PLATFORMS.append(pf)

            elif col in TRAMPOLINE_IMAGE:  # Создает трамплин
                tramp = Trampoline(col, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)  # Передаем тип трамплина
                ENTITIES.add(tramp)

            elif col == 'A':  # Создание рыбы-фугу
                fish = Fish(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(fish)

                image_path = get_wall_image_path(col)
                pf = Platform(image_path, x * PLATFORM_WIDTH + PLATFORM_WIDTH,
                              y * PLATFORM_HEIGHT + PLATFORM_HEIGHT)  # Создаем невидимую платформу
                ENTITIES.add(pf)
                PLATFORMS.append(pf)

            elif col in '♜♖':
                bat = Bat(col, x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT)
                ENTITIES.add(bat)

    # Определяем размеры уровня
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    # Создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:
        if not game_over_active:
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

            # Обновляем все объекты
            if not game_over_active:
                hero.update(PLATFORMS)
                for entity in ENTITIES:
                    if isinstance(entity, Trap) or isinstance(entity, Trampoline):
                        entity.update(hero)
                    elif isinstance(entity, Bat):
                        entity.update(PLATFORMS)
                    elif not isinstance(entity, Player):
                        entity.update()

                # Проверка столкновений с объектами
                collided_objects = pygame.sprite.spritecollide(hero, ENTITIES, dokill=False)
                for obj in collided_objects:
                    # Проверка столкновения игрока со смертельно опасными объектами
                    if isinstance(obj, Spike) or (
                            isinstance(obj, Thorn) and obj.image_name is not None and (
                            '2' in obj.image_name or '3' in obj.image_name)) or (
                            isinstance(obj, Fish) and int(obj.image_name[5:-4]) in list(range(6, 15)) or (
                            isinstance(obj, Bat))):
                        print("Вы погибли!")
                        death_channel.play(SOUNDS['death'])
                        death_channel.set_volume(0.2)

                        game_over_active = True
                        break

                    if isinstance(obj, Coin):
                        print("Монета собрана!")
                        coin_channel.play(SOUNDS['coin'])
                        coin_channel.set_volume(0.1)
                        count_coin += 1
                        ENTITIES.remove(obj)

                    elif isinstance(obj, XP):
                        print("Опыт получен!")
                        xp_channel.play(SOUNDS['xp'])
                        xp_channel.set_volume(0.05)
                        ENTITIES.remove(obj)

                    elif isinstance(obj, Star):
                        print("Звезда собрана!")
                        star_channel.play(SOUNDS['star'])
                        star_channel.set_volume(0.1)
                        ENTITIES.remove(obj)
                        count_star += 1

                    elif isinstance(obj, Finish):
                        print("Поздравляю! Вы достигли финиша!")

                        STATE['levels'][int(name_file[-5]) - 1] = count_star
                        STATE['coins'] += count_coin
                        SOUNDS['coin'].set_volume(0.05)
                        save_game(STATE)

                        activate_menu()  # Активируем меню
                        pygame.quit()  # Закрываем текущее игровое окно

                # Отображение заднего фона и всех сущностей
                screen.blit(bg, (0, 0))  # Отображаем фон
                camera.update(hero)  # Обновляем камеру

                for spr in ENTITIES:
                    if spr.image is not None:  # Проверка, что изображение не равно None
                        screen.blit(spr.image, camera.apply(spr))

                pygame.display.update()  # Обновляем экран
                pygame.time.Clock().tick(FPS)  # Ограничиваем FPS игры до 120

        else:
            pygame.mixer.music.stop()  # Останавливаем музыку
            Death(screen, name_file, start_x, start_y)