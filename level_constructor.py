import pygame
import os
import re
from pygame import KEYDOWN, K_ESCAPE

# Размеры окна
screen_size = width, height = 325, 1000
cell_size = 25

# Определение пути к изображениям
image_paths = {
    '-': 'blocks/wall_1.png',
    'c': 'spike/spike_2.png',
    'a': 'trap/trap_1.png',
    '↙': 'trampoline/trampoline_1.png',
    'A': 'fish/fish_icon.png',
    '♜': 'bat/bat_left_0.png',
    '⇑': 'dart/dart_left_0.png',
    '+': 'xp/xp_0.png',
    '$': 'coin/coin_0.png',
    '*': 'star/star_0.png',
    '⊞': 'ice box/ice_box_0.png',
    'F': 'exit/exit_0.png',
    ' ': None  # Для пустоты будет черный квадрат с белой рамкой
}


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[' '] * width for _ in range(height)]
        self.cell_size = cell_size
        self.offset_x = 0
        self.offset_y = 0

        # Загрузка изображений
        self.images = {}
        for symbol, path in image_paths.items():
            if path:
                img = pygame.image.load(path).convert_alpha()
                # Изменение размера изображения до квадрата cell_size
                self.images[symbol] = pygame.transform.scale(img, (cell_size, cell_size))
            else:
                self.images[symbol] = None  # Пустое поле

        # Порядок символов для левой и правой кнопок
        self.left_color_order = ['-', 'c', 'a', '↙', 'A', '♜', '⇑', ' ']
        self.right_color_order = ['+', '$', '*', '⊞', 'F', ' ']

    def set_color_left(self, x, y, flag=False):
        """Обработка при нажатии левой кнопки мыши."""
        if 0 <= x < self.width * self.cell_size and 0 <= y < self.height * self.cell_size:
            grid_x, grid_y = (x - self.offset_x) // self.cell_size, (y - self.offset_y) // self.cell_size
            current_symbol = self.board[grid_y][grid_x]

            if current_symbol in self.left_color_order:
                current_index = self.left_color_order.index(current_symbol)
            else:
                current_index = -1

            if flag:
                new_index = 0  # Режим рисования стен
            else:
                new_index = (current_index + 1) % len(self.left_color_order)

            self.board[grid_y][grid_x] = self.left_color_order[new_index]

    def set_color_right(self, x, y, flag=False):
        """Обработка при нажатии правой кнопки мыши."""
        if 0 <= x < self.width * self.cell_size and 0 <= y < self.height * self.cell_size:
            grid_x, grid_y = (x - self.offset_x) // self.cell_size, (y - self.offset_y) // self.cell_size
            current_symbol = self.board[grid_y][grid_x]

            if current_symbol in self.right_color_order:
                current_index = self.right_color_order.index(current_symbol)
            else:
                current_index = -1

            if flag:
                new_index = 0  # Режим рисования стен
            else:
                new_index = (current_index + 1) % len(self.right_color_order)

            self.board[grid_y][grid_x] = self.right_color_order[new_index]

    def remove_color(self, x, y):
        """Удаляет цвет на выбранной клетке."""
        if 0 <= x < self.width * self.cell_size and 0 <= y < self.height * self.cell_size:
            grid_x, grid_y = (x - self.offset_x) // self.cell_size, (y - self.offset_y) // self.cell_size
            self.board[grid_y][grid_x] = ' '

    def render(self, screen):
        """Отрисовка борда."""
        for i in range(self.width):
            for j in range(self.height):
                symbol = self.board[j][i]  # Получаем символ

                if symbol in self.images:
                    image = self.images[symbol]
                    if image:
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                          self.cell_size, self.cell_size))
                        # Рассчитываем координаты для отрисовки изображения, чтобы оно было по центру ячейки
                        pos_x = i * self.cell_size + self.offset_x + (self.cell_size - image.get_width()) // 2
                        pos_y = j * self.cell_size + self.offset_y + (self.cell_size - image.get_height()) // 2
                        screen.blit(image, (pos_x, pos_y))  # Отрисовка изображения
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                          self.cell_size, self.cell_size), 1)  # Белая рамка
                    else:
                        # Отрисовка черного квадрата в случае пустоты
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                          self.cell_size, self.cell_size))
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                          self.cell_size, self.cell_size), 1)  # Белая рамка

        pygame.display.flip()

    def calculate_next_level_number(self):
        """Определяет номер следующего уровня для сохранения."""
        max_level = -1
        pattern = r"level_(\d+)\.txt"
        for filename in os.listdir('.'):
            match = re.match(pattern, filename)
            if match:
                level_number = int(match.group(1))
                max_level = max(max_level, level_number)
        return max_level

    def save_level(self):
        """Сохраняет уровень в файл."""
        borders = self.get_borders()  # Получаем границы ненулевой части матрицы
        if borders:  # Если границы найдены
            top, bottom, left, right = borders
            level_file = f"level_{self.calculate_next_level_number() + 1}.txt"

            with open(level_file, "w", encoding='utf-8') as file:
                for row in range(top, bottom + 1):
                    new_line = ''.join(self.board[row][left:right + 1])
                    file.write(f'|{new_line}\n')  # Записываем строку в формате с кавычками

    def get_borders(self):
        """Находит границы ненулевой части матрицы."""
        top, bottom, left, right = None, None, None, None
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != ' ':
                    if top is None:
                        top = y
                    bottom = y
                    if left is None or x < left:
                        left = x
                    if right is None or x > right:
                        right = x
        return (top, bottom, left, right) if all(v is not None for v in [top, bottom, left, right]) else None


# Инициализация Pygame и создание окна
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
board = Board(width // cell_size, height // cell_size)

mouse_button_down = False
press_start_time = 0

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                board.save_level()
                print(f"Уровень {board.calculate_next_level_number()} сохранен.")
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:  # Левая кнопка
                mouse_button_down = True
                press_start_time = pygame.time.get_ticks()
                board.set_color_left(x, y)

            elif event.button == 2:  # Средняя (колесико)
                mouse_button_down = True
                press_start_time = pygame.time.get_ticks()
                board.remove_color(x, y)

            elif event.button == 3:  # Правая кнопка
                mouse_button_down = True
                press_start_time = pygame.time.get_ticks()
                board.set_color_right(x, y)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False

    if mouse_button_down:
        x, y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        if current_time - press_start_time >= 500:
            if pygame.mouse.get_pressed()[0]:  # Лёвая кнопка
                board.set_color_left(x, y, True)
            if pygame.mouse.get_pressed()[1]:  # Средняя кнопка
                board.remove_color(x, y)
            if pygame.mouse.get_pressed()[2]:  # Правая кнопка
                board.set_color_right(x, y, True)

    # Рендеринг доски
    board.render(screen)
    clock.tick(60)  # Ограничение до 60 FPS
