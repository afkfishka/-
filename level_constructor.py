import pygame
import os
import re
from pygame import KEYDOWN, K_ESCAPE

screen_size = width, height = 1920, 1080
cell_size = 30


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['0'] * width for _ in range(height)]

        self.cell_size = cell_size
        self.colors = {
            '0': '#000000',  # пустота
            '-': '#d44042',  # стена
            '#': '#43f6cb',  # шипы
            '@': '#000000',  # трап
            '^': '#000000',  # трамплин
            '+': '#000000',  # xp
            '$': '#000000',  # монета
            '*': '#000000',  # звезда
            'F': '#000000',  # финиш
            'S': '#000000'  # старт
        }

        # self.left_color_order = ['-', '#', '@', '^', '0']  # Порядок для левой кнопки
        self.left_color_order = ['-', '#', '0']
        self.right_color_order = ['+', '$', '*', 'F', 'S']  # Порядок для правой кнопки

        self.offset_x = 0
        self.offset_y = 0

    def set_color_left(self, x, y, flag=False):  # обработка при нажатии левой кнопки мыши
        """Если кликаем по полю, то определяем какой там сейчас символ
        и заменяем его на следующий символ из списка left_color_order"""

        if 0 <= x < self.width * self.cell_size and 0 <= y < self.height * self.cell_size:
            grid_x, grid_y = (x - self.offset_x) // self.cell_size, (y - self.offset_y) // self.cell_size
            current_symbol = self.board[grid_y][grid_x]
            current_index = self.left_color_order.index(current_symbol)

            if flag:  # если кнопка зажата >0.5сек, то режим рисования только стен
                new_index = 0
            else:
                new_index = (current_index + 1) % len(self.left_color_order)

            self.board[grid_y][grid_x] = self.left_color_order[new_index]

    # def set_color_right(self, x, y):  # обработка при нажатии правой кнопки мыши
    #     if 0 <= x < self.width * self.cell_size and 0 <= y < self.height * self.cell_size:
    #         grid_x, grid_y = (x - self.offset_x) // self.cell_size, (y - self.offset_y) // self.cell_size
    #         current_symbol = self.board[grid_y][grid_x]
    #         if current_symbol in self.right_color_order:
    #             current_index = self.right_color_order.index(current_symbol)
    #             new_index = (current_index + 1) % len(self.right_color_order)
    #             self.board[grid_y][grid_x] = self.right_color_order[new_index]

    def get_borders(self):
        """Находит границы ненулевой части матрицы"""
        top, bottom, left, right = None, None, None, None
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != '0':
                    if top is None:
                        top = y
                    bottom = y
                    if left is None or x < left:
                        left = x
                    if right is None or x > right:
                        right = x
        if top is not None and bottom is not None and left is not None and right is not None:
            return top, bottom, left, right
        return None

    def calculate_next_level_number(self):
        """Вычисляет следующий номер уровня на основе существующих файлов"""
        max_level = -1
        pattern = r"level_(\d+)\.txt"
        for filename in os.listdir('.'):
            match = re.match(pattern, filename)
            if match:
                level_number = int(match.group(1))
                max_level = max(max_level, level_number)
        return max_level

    def corner_cells(self, x, y):  # расставить угловые клетки на поле
        if self.board[y][x] == '0':  # Проверка, является ли текущая клетка '-'
            return

        up, down, left, right = False, False, False, False
        for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < self.height and 0 <= nx < self.width:
                if self.board[ny][nx] != '0':
                    if dx == -1:
                        left = True
                    if dx == 1:
                        right = True
                    if dy == 1:
                        down = True
                    if dy == -1:
                        up = True

        if down and up and left and right:
            self.board[y][x] = '1'

        elif down and right:
            self.board[y][x] = '6'
            self.board[y][x + 1] = '3'
            self.board[y + 1][x] = '4'

        elif down and left:
            self.board[y][x] = '7'
            self.board[y][x - 1] = '3'
            self.board[y + 1][x] = '5'

        elif up and left:
            self.board[y][x] = '8'
            self.board[y][x - 1] = '2'
            self.board[y - 1][x] = '5'

        elif up and right:
            self.board[y][x] = '9'
            self.board[y][x + 1] = '2'
            self.board[y - 1][x] = '4'

        elif up and down:
            if self.board[y + 1][x] in '469' or self.board[y - 1][x] in '469':
                self.board[y][x] = '4'
            else:
                self.board[y][x] = '5'

        elif left and right:
            if self.board[y][x + 1] in '367' or self.board[y][x - 1] in '367':
                self.board[y][x] = '3'

    def save_level(self):
        borders = self.get_borders()  # Получаем границы ненулевой части матрицы
        if borders:  # Если границы найдены
            top, bottom, left, right = borders
            level_file = f"level_{self.calculate_next_level_number() + 1}.txt"

            for row in range(top, bottom + 1):
                for col in range(left, right + 1):
                    if self.board[row][col] == '-':
                        self.corner_cells(col, row)

            with open(level_file, "w") as file:
                file.write("level = [\n")
                for row in range(top, bottom + 1):
                    new_line = []
                    for col in range(left, right + 1):
                        new_line.append(self.board[row][col])  # Оставляем другие символы без изменений

                    line = ''.join(new_line)  # Собираем строку из измененных символов
                    file.write(f'    "{line}",\n')  # Записываем строку в формате с кавычками
                file.write("]\n")

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                symbol = self.board[j][i]  # Получаем символ
                color = pygame.Color(self.colors[symbol])  # Находим соответствующий цвет по символу
                pygame.draw.rect(screen, color,
                                 (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                  self.cell_size, self.cell_size))

                # Отрисовка рамки
                pygame.draw.rect(screen, (255, 255, 255),
                                 (i * self.cell_size + self.offset_x, j * self.cell_size + self.offset_y,
                                  self.cell_size, self.cell_size), 1)

        pygame.display.flip()


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
            if event.button == 1:
                mouse_button_down = True
                press_start_time = pygame.time.get_ticks()
                x, y = event.pos
                board.set_color_left(x, y)

            if event.button == 3:
                x, y = event.pos
                # board.set_color_right(x, y)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False

    if mouse_button_down and pygame.mouse.get_pressed()[0]:
        current_time = pygame.time.get_ticks()
        if current_time - press_start_time >= 500:
            x, y = pygame.mouse.get_pos()
            board.set_color_left(x, y, flag=True)

    # screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
