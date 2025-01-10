import pygame
import sys
import game
import os

STATE = game.load_game()

flag_shop = False  # флаг для отрисовки магазина
flag_skins = False  # флаг для отрисовки меню скинов
flag_map = True  # флаг для отрисовки карты уровней
flag_arcade = False  # флаг для отрисовки аркады


# уровни все


def load_animation_frames(path, count, prefix):
    frames = []
    for i in range(count):
        image_path = os.path.join(path, f'{prefix}_{i}.png')  # Загружаем кадры анимации
        frames.append(pygame.image.load(image_path))
    return frames


class ShopSprites(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (292, 750)  # Позиционирование спрайта


class SkinsSprites(pygame.sprite.Sprite):  # Кнопка скинов
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/skin.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (497, 750)  # Позиционирование спрайта


class MapSprites(pygame.sprite.Sprite):  # Кнопка карты
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/map.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (702, 750)  # Позиционирование спрайта


class ArcadeSprites(pygame.sprite.Sprite):  # Кнопка аркады
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/arcade.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (907, 750)  # Позиционирование спрайта


class Achivements(pygame.sprite.Sprite):  # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/menu_achievements1.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (40, 40))  # Масштабируем изображение до 40x40
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (1160, 30)  # Позиционирование спрайта в центре экрана


class Pink_line(pygame.sprite.Sprite):  # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/pink_line.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (900, 450)  # Позиционирование спрайта в центре экрана

class Pink_line2(pygame.sprite.Sprite):  # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/pink_line.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (300, 450)  # Позиционирование спрайта в центре экрана




class ArcadeDoor(pygame.sprite.Sprite):
    def __init__(self):
        x, y = (445, 350)
        a = 5
        width, height = (62 * a, 34 * a)
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'arcade'), 4, "arcade_animate")
        self.index = 0
        self.image = pygame.transform.scale(self.frames[self.index], (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.frame_rate = 60
        self.frame_counter = 0

    def update(self):
        # Логика анимации аркады
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.index], (self.rect.width, self.rect.height))


class Settings(pygame.sprite.Sprite):  # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/menu_settings1.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (40, 40))  # Масштабируем изображение до 40x40
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (1100, 30)  # Позиционирование спрайта в центре экрана

class Arcade_right(pygame.sprite.Sprite):  # Кнопка карты
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rignt.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (775, 245)  # Позиционирование спрайта




class Arcade_left(pygame.sprite.Sprite):  # Кнопка карты
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/left.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (400, 245)  # Позиционирование спрайта


class Arcade_button(pygame.sprite.Sprite):  # Кнопка карты
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/play_in_arcade.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (600, 600)  # Позиционирование спрайта


class draw_lvl(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class Lvl1(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(120, 270))  # Устанавливаем позицию


class Lvl2(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(120, 430))  # Устанавливаем позицию


class Lvl3(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(330, 430))  # Устанавливаем позицию


class Lvl4(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(330, 270))  # Устанавливаем позицию


class Lvl5(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(540, 270))  # Устанавливаем позицию


class Lvl6(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(540, 430))  # Устанавливаем позицию


class Lvl7(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(750, 430))  # Устанавливаем позицию


class Lvl8(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(750, 270))  # Устанавливаем позицию


class Lvl9(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(960, 270))  # Устанавливаем позицию


class Lvl10(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=(960, 430))  # Устанавливаем позицию


class draw_vertikall_line(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 60))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class draw_gorizontall_line(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((90, 20))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class Lobby(pygame.sprite.Sprite):  # Лобби
    def __init__(self):
        pygame.init()
        self.screen_size = (1200, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Тайны подземелий")

        # Воспроизведение фоновой музыки
        pygame.mixer.init()
        pygame.mixer.music.load('music and sounds/menu.mp3')
        pygame.mixer.music.play(-1)  # Воспроизводить бесконечно
        pygame.mixer.music.set_volume(0.1)  # Установка громкости на 2%

        self.BLACK = (0, 0, 0)

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.b_font = pygame.font.Font(self.font_path, 100)

        self.coin_image = pygame.image.load('images/menu_coin.png')
        self.scaled_coin_image = pygame.transform.scale(self.coin_image, (40, 40))

        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.arcade_sprites = pygame.sprite.Group()

        self.all_sprites.add(ShopSprites())
        self.all_sprites.add(SkinsSprites())
        self.all_sprites.add(MapSprites())
        self.all_sprites.add(ArcadeSprites())
        self.all_sprites.add(Achivements())
        self.all_sprites.add(Settings())

        self.map_sprites.add(Lvl1())
        self.map_sprites.add(Lvl2())
        self.map_sprites.add(Lvl3())
        self.map_sprites.add(Lvl4())
        self.map_sprites.add(Lvl5())
        self.map_sprites.add(Lvl6())
        self.map_sprites.add(Lvl7())
        self.map_sprites.add(Lvl8())
        self.map_sprites.add(Lvl9())
        self.map_sprites.add(Lvl10())

        self.map_sprites.add(draw_vertikall_line((170, 370)))
        self.map_sprites.add(draw_vertikall_line((380, 370)))
        self.map_sprites.add(draw_vertikall_line((590, 370)))
        self.map_sprites.add(draw_vertikall_line((800, 370)))
        self.map_sprites.add(draw_vertikall_line((1010, 370)))

        self.map_sprites.add(draw_gorizontall_line((240, 470)))
        self.map_sprites.add(draw_gorizontall_line((450, 310)))
        self.map_sprites.add(draw_gorizontall_line((660, 470)))
        self.map_sprites.add(draw_gorizontall_line((870, 310)))

        self.arcade_sprites.add(Arcade_right())
        self.arcade_sprites.add(Arcade_left())
        self.arcade_sprites.add(ArcadeDoor())
        self.arcade_sprites.add(Pink_line())
        self.arcade_sprites.add(Pink_line2())
        self.arcade_sprites.add(Arcade_button())

        self.main_menu()

    def draw_text(self, text, font, surface, x, y, color):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            self.draw_text("Тайны подземелий", self.font, self.screen, self.screen_size[0] // 2,
                           self.screen_size[1] // 6, (160, 40, 222))

            self.all_sprites.draw(self.screen)
            self.screen.blit(self.scaled_coin_image, (10, 10))

            if flag_map:  # отображение карты уровней
                self.map_sprites.draw(self.screen)
                self.draw_text("1", self.b_font, self.screen, 180, 310, (0, 0, 0))  # 6 4
                self.draw_text("2", self.b_font, self.screen, 180, 470, (0, 0, 0))
                self.draw_text("3", self.b_font, self.screen, 390, 470, (0, 0, 0))
                self.draw_text("4", self.b_font, self.screen, 390, 310, (0, 0, 0))
                self.draw_text("5", self.b_font, self.screen, 600, 310, (0, 0, 0))
                self.draw_text("6", self.b_font, self.screen, 600, 470, (0, 0, 0))
                self.draw_text("7", self.b_font, self.screen, 810, 470, (0, 0, 0))
                self.draw_text("8", self.b_font, self.screen, 810, 310, (0, 0, 0))
                self.draw_text("9", self.b_font, self.screen, 1020, 310, (0, 0, 0))
                self.draw_text("10", self.b_font, self.screen, 1020, 470, (0, 0, 0))

            if flag_arcade:
                self.arcade_sprites.draw(self.screen)

                self.draw_text("Аркада", self.b_font, self.screen, self.screen_size[0] // 2,
                               self.screen_size[1] // 10 * 3, "Yellow")
                self.draw_text("Играть", self.b_font, self.screen, self.screen_size[0] // 2,
                               587, "black")
                self.arcade_sprites.update()



            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_click(pos)
                    self.click_lvl_map(pos)
                    self.click_arcade(pos)

            pygame.display.flip()

    def check_click(self, pos):  # нажатие на кнопки меню
        global flag_shop  # флаг для отрисовки магазина
        global flag_skins  # флаг для отрисовки меню скинов
        global flag_map  # флаг для отрисовки карты уровней
        global flag_arcade  # флаг для отрисовки аркады
        for sprite in self.all_sprites:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, ShopSprites):
                    flag_shop = True  # флаг для отрисовки магазина
                    flag_skins = False  # флаг для отрисовки меню скинов
                    flag_map = False  # флаг для отрисовки карты уровней
                    flag_arcade = False  # флаг для отрисовки аркады
                elif isinstance(sprite, SkinsSprites):
                    flag_shop = False  # флаг для отрисовки магазина
                    flag_skins = True  # флаг для отрисовки меню скинов
                    flag_map = False  # флаг для отрисовки карты уровней
                    flag_arcade = False  # флаг для отрисовки аркады
                elif isinstance(sprite, MapSprites):
                    flag_shop = False  # флаг для отрисовки магазина
                    flag_skins = False  # флаг для отрисовки меню скинов
                    flag_map = True  # флаг для отрисовки карты уровней
                    flag_arcade = False  # флаг для отрисовки аркады

                elif isinstance(sprite, ArcadeSprites):
                    flag_shop = False  # флаг для отрисовки магазина
                    flag_skins = False  # флаг для отрисовки меню скинов
                    flag_map = False  # флаг для отрисовки карты уровней
                    flag_arcade = True  # флаг для отрисовки аркады
                elif isinstance(sprite, Achivements):
                    pass
                elif isinstance(sprite, Settings):
                    pass



    def click_arcade(self, pos):
        for sprite in self.arcade_sprites:
            if sprite.rect.collidepoint(pos) and flag_arcade:
                if isinstance(sprite, Arcade_button):
                    print('это сообщение находится в 403 строчке!!!!!!!!!!')

    def click_lvl_map(self, pos):
        for sprite in self.map_sprites:
            if sprite.rect.collidepoint(pos) and flag_map:
                if isinstance(sprite, Lvl1):
                    game.level("level_1.txt", 13, 28)
                elif isinstance(sprite, Lvl2):
                    game.level("level_2.txt", 12, 4)
                elif isinstance(sprite, Lvl3):
                    game.level("level_3.txt", 17, 25)
                elif isinstance(sprite, Lvl4):
                    game.level("level_4.txt", 11, 4)
                elif isinstance(sprite, Lvl5):
                    game.level("level_5.txt", 13, 27)
                elif isinstance(sprite, Lvl6):
                    game.level("level_6.txt", 15, 26)
                elif isinstance(sprite, Lvl7):
                    game.level("level_7.txt", 4, 8)
                elif isinstance(sprite, Lvl8):
                    print('8')
                elif isinstance(sprite, Lvl9):
                    game.level("arcade_1.txt", 7, 91)
                elif isinstance(sprite, Lvl10):
                    game.level("arcade_2.txt", 7, 116)


def achivements_function(self):
    print("Список достижений открыт!")
    pygame.time.delay(2000)  # Имитация задержки


def settings_function(self):
    print("Запуск настроек!")
    pygame.time.delay(2000)  # Имитация задержки


Lobby()
