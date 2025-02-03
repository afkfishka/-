import pygame
import sys
import game
import os

flag_shop = False  # флаг для отрисовки магазина
flag_skins = False  # флаг для отрисовки меню скинов
flag_map = True  # флаг для отрисовки карты уровней
flag_arcade = False  # флаг для отрисовки аркады


class Load_image(pygame.sprite.Sprite): # Загрузка изображения
    def __init__(self, image_path, position):
        super().__init__()
        # Загрузка изображения
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)  # Установить позицию спрайта


class Load_lock(pygame.sprite.Sprite):   # Загрузка изображения с трансформированием
    def __init__(self, image_path, position, scalled):
        super().__init__()
        # Загрузка изображения
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scalled)  # Масштабируем изображение до 40x40
        self.rect = self.image.get_rect(topleft=position)  # Установить позицию спрайта


# уровни все


def load_animation_frames(path, count, prefix):      # Анимация фреймов
    frames = []
    for i in range(count):
        image_path = os.path.join(path, f'{prefix}_{i}.png')  # Загружаем кадры анимации
        frames.append(pygame.image.load(image_path))
    return frames


class ShopSprites(pygame.sprite.Sprite):  # Спрайты магазина
    def __init__(self):
        super().__init__()
        if game.STATE['lang'] == 'ru':
            self.image = pygame.image.load('images/shop.png')  # Загрузка изображения
        elif game.STATE['lang'] == 'eng':
            self.image = pygame.image.load('images/shop_eng.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (292, 750)  # Позиционирование спрайта


class SkinsSprites(pygame.sprite.Sprite):  # Спрайты скинов
    def __init__(self):
        super().__init__()
        if game.STATE['lang'] == 'ru':
            self.image = pygame.image.load('images/skin.png')  # Загрузка изображения
        elif game.STATE['lang'] == 'eng':
            self.image = pygame.image.load('images/skin_eng.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (497, 750)  # Позиционирование спрайта


class MapSprites(pygame.sprite.Sprite):  # Спрайты карты
    def __init__(self):
        super().__init__()
        if game.STATE['lang'] == 'ru':
            self.image = pygame.image.load('images/map.png')  # Загрузка изображения
        elif game.STATE['lang'] == 'eng':
            self.image = pygame.image.load('images/map_eng.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (702, 750)  # Позиционирование спрайта


class ArcadeSprites(pygame.sprite.Sprite):  # Спрайты аркады
    def __init__(self):
        super().__init__()
        if game.STATE['lang'] == 'ru':
            self.image = pygame.image.load('images/arcade.png')  # Загрузка изображения
        elif game.STATE['lang'] == 'eng':
            self.image = pygame.image.load('images/arcade_eng.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (907, 750)  # Позиционирование спрайта




class Pink_line(pygame.sprite.Sprite):  # Розовая линия
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/pink_line.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (900, 450)  # Позиционирование спрайта в центре экрана


class Pink_line2(pygame.sprite.Sprite):  # Розовая линия
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/pink_line.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (300, 450)  # Позиционирование спрайта в центре экрана


class ArcadeDoor(pygame.sprite.Sprite):  # Врата для аркады
    def __init__(self):
        x, y = (445, 350)
        a = 5
        width, height = (62 * a, 34 * a)
        super().__init__()
        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'textures/arcade'), 4,
                                            "arcade_animate")
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


class Shop_skin_1(pygame.sprite.Sprite):  # картинки магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (175, 200)  # Позиционирование спрайта


class Shop_skin_2(pygame.sprite.Sprite):  # картинки магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (475, 200)  # Позиционирование спрайта


class Shop_skin_3(pygame.sprite.Sprite):  # картинки магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (775, 200)  # Позиционирование спрайта


class Shop_skin_11(pygame.sprite.Sprite):
    '''Анимированный скин в магазине'''
    def __init__(self):
        super().__init__()

        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "man_botright")
        self.index = 0
        self.image = self.frames[self.index]
        self.frame_rate = 15
        self.frame_counter = 0

        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (236, 286)  # Позиционирование спрайта

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.image = pygame.transform.scale(self.image, (128, 128))


class Shop_skin_22(pygame.sprite.Sprite):
    '''Анимированный скин в магазине'''
    def __init__(self):
        super().__init__()

        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 6, "spectrum_botright")
        self.index = 0
        self.image = self.frames[self.index]
        self.frame_rate = 15
        self.frame_counter = 0

        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (540, 286)  # Позиционирование спрайта

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.image = pygame.transform.scale(self.image, (128, 128))


class Shop_skin_33(pygame.sprite.Sprite):
    '''Анимированный скин в магазине'''
    def __init__(self):
        super().__init__()

        self.frames = load_animation_frames(os.path.join(os.path.dirname(__file__), 'man'), 5, "froggy_botright")
        self.index = 0
        self.image = self.frames[self.index]
        self.frame_rate = 20
        self.frame_counter = 0

        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (836, 286)  # Позиционирование спрайта


    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.image = pygame.transform.scale(self.image, (128, 128))


class Shop_spell_1(pygame.sprite.Sprite):  # Картинка магазина скинов
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (175, 200)  # Позиционирование спрайта


class Shop_spell_2(pygame.sprite.Sprite):   # Картинка магазина скинов
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (475, 200)  # Позиционирование спрайта


class Shop_spell_3(pygame.sprite.Sprite):   # Картинка магазина скинов
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/layout_shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.topleft = (775, 200)  # Позиционирование спрайта


class Shop_spell_button_1(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (200, 625)  # Позиционирование спрайта


class Shop_spell_button_2(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (500, 625)  # Позиционирование спрайта


class Shop_spell_button_3(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (800, 625)  # Позиционирование спрайта


class Shop_skin_button_1(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (200, 625)  # Позиционирование спрайта


class Shop_skin_button_2(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (500, 625)  # Позиционирование спрайта


class Shop_skin_button_3(pygame.sprite.Sprite):  # Кнопка магазина
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/zxc.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.bottomleft = (800, 625)  # Позиционирование спрайта


class Settings(pygame.sprite.Sprite):  # Кнопка настроек
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/menu_settings1.png')  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (40, 40))  # Масштабируем изображение до 40x40
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (1170, 30)  # Позиционирование спрайта в центре экрана


class Arcade_right(pygame.sprite.Sprite):  # картинка для аркады
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rignt.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (775, 245)  # Позиционирование спрайта


class Arcade_left(pygame.sprite.Sprite): # картинка для аркады
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/left.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (400, 245)  # Позиционирование спрайта


class Arcade_button(pygame.sprite.Sprite):  # картинка для аркады
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/play_in_arcade.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (600, 600)  # Позиционирование спрайта


class draw_lvl(pygame.sprite.Sprite):     # Рисуем уровень
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10))  # Заполняем красным цветом
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class Lvl1(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][0] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(120, 270))  # Устанавливаем позицию


class Lvl2(pygame.sprite.Sprite):   # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][0] > 0 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(120, 430))  # Устанавливаем позицию


class Lvl3(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][1] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(330, 430))  # Устанавливаем позицию


class Lvl4(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][2] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(330, 270))  # Устанавливаем позицию


class Lvl5(pygame.sprite.Sprite):   # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][3] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(540, 270))  # Устанавливаем позицию


class Lvl6(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][4] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(540, 430))  # Устанавливаем позицию


class Lvl7(pygame.sprite.Sprite): # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][5] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(750, 430))  # Устанавливаем позицию


class Lvl8(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][6] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(750, 270))  # Устанавливаем позицию


class Lvl9(pygame.sprite.Sprite):  # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][7] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(960, 270))  # Устанавливаем позицию


class Lvl10(pygame.sprite.Sprite): # Отрисовка уровня
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((120, 100))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if game.STATE['levels'][8] != -1 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=(960, 430))  # Устанавливаем позицию


class draw_vertikall_line(pygame.sprite.Sprite):   # Отрисовка линий уровней
    def __init__(self, position, id=None):
        super().__init__()
        self.image = pygame.Surface((20, 60))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if id == 1 and game.STATE['levels'][0] > 0 or id == 2 and \
                                                       game.STATE['levels'][
                                                           2] > 0 or id == 3 and game.STATE['levels'][
                                                           4] > 0 or id == 4 and game.STATE['levels'][
                                                           6] > 0 or id == 5 and game.STATE['levels'][
                                                           8] > 0 else self.image.fill(pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class draw_gorizontall_line(pygame.sprite.Sprite): # Отрисовка линий уровней
    def __init__(self, position, id=None):
        super().__init__()
        self.image = pygame.Surface((90, 20))  # Создаем поверхность
        self.image.fill(pygame.Color(254, 254, 10)) if id == 1 and game.STATE['levels'][1] > 0 or id == 2 and \
                                                       game.STATE['levels'][
                                                           3] > 0 or id == 3 and game.STATE['levels'][
                                                           5] > 0 or id == 4 and game.STATE['levels'][
                                                           7] > 0 else self.image.fill(
            pygame.Color(214, 0, 254))
        self.rect = self.image.get_rect(topleft=position)  # Устанавливаем позицию


class Lobby(pygame.sprite.Sprite):  # Лобби
    def __init__(self):
        pygame.init()
        self.screen_size = (1200, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Тайны подземелий")
        print(game.STATE)
        # Воспроизведение фоновой музыки

        self.BLACK = (0, 0, 0)

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.b_font = pygame.font.Font(self.font_path, 100)
        self.font_70 = pygame.font.Font(self.font_path, 70)
        self.font_30 = pygame.font.Font(self.font_path, 30)
        self.font_50 = pygame.font.Font(self.font_path, 50)

        self.coin_image = pygame.image.load('images/menu_coin.png')
        self.scaled_coin_image = pygame.transform.scale(self.coin_image, (40, 40))

        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.arcade_sprites = pygame.sprite.Group()
        self.shop_skins_sprites = pygame.sprite.Group()
        self.shop_spell_sprites = pygame.sprite.Group()

        self.all_sprites.add(ShopSprites())
        self.all_sprites.add(SkinsSprites())
        self.all_sprites.add(MapSprites())
        self.all_sprites.add(ArcadeSprites())
        self.all_sprites.add(Settings())

        self.image_path_stars_0 = 'textures/star/stars_0.png'
        self.image_path_stars_1 = 'textures/star/stars_1.png'
        self.image_path_stars_2 = 'textures/star/stars_2.png'
        self.image_path_stars_3 = 'textures/star/stars_3.png'

        # Позиции для звезд
        self.pos_lvl_1 = (120, 270 + 90)
        self.pos_lvl_2 = (120, 430 + 90)
        self.pos_lvl_3 = (330, 430 + 90)
        self.pos_lvl_4 = (330, 270 + 90)
        self.pos_lvl_5 = (540, 270 + 90)
        self.pos_lvl_6 = (540, 430 + 90)
        self.pos_lvl_7 = (750, 430 + 90)
        self.pos_lvl_8 = (750, 270 + 90)
        self.pos_lvl_9 = (960, 270 + 90)
        self.pos_lvl_10 = (960, 430 + 90)

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

        self.shop_skins_sprites.add(Shop_skin_1())
        self.shop_skins_sprites.add(Shop_skin_2())
        self.shop_skins_sprites.add(Shop_skin_3())
        self.shop_skin_11 = Shop_skin_11()
        self.shop_skin_22 = Shop_skin_22()
        self.shop_skin_33 = Shop_skin_33()
        self.shop_skins_sprites.add(self.shop_skin_11)
        self.shop_skins_sprites.add(self.shop_skin_22)
        self.shop_skins_sprites.add(self.shop_skin_33)
        self.shop_skins_sprites.add(Shop_skin_button_1())
        self.shop_skins_sprites.add(Shop_skin_button_2())
        self.shop_skins_sprites.add(Shop_skin_button_3())

        self.shop_spell_sprites.add(Shop_spell_1())
        self.shop_spell_sprites.add(Shop_spell_2())
        self.shop_spell_sprites.add(Shop_spell_3())
        self.shop_spell_sprites.add(Shop_spell_button_1())
        self.shop_spell_sprites.add(Shop_spell_button_2())
        self.shop_spell_sprites.add(Shop_spell_button_3())
        self.shop_spell_sprites.add(Load_lock('images/bonus_shield.png', (236, 286), (128, 128)))
        self.shop_spell_sprites.add(Load_lock('images/bonus_magnet.png', (536, 286), (128, 128)))
        self.shop_spell_sprites.add(Load_lock('images/bonus_freezing.png', (836, 286), (128, 128)))


        self.map_sprites.add(draw_vertikall_line((170, 370), 1))
        self.map_sprites.add(draw_vertikall_line((380, 370), 2))
        self.map_sprites.add(draw_vertikall_line((590, 370), 3))
        self.map_sprites.add(draw_vertikall_line((800, 370), 4))
        self.map_sprites.add(draw_vertikall_line((1010, 370), 5))

        self.map_sprites.add(draw_gorizontall_line((240, 470), 1))
        self.map_sprites.add(draw_gorizontall_line((450, 310), 2))
        self.map_sprites.add(draw_gorizontall_line((660, 470), 3))
        self.map_sprites.add(draw_gorizontall_line((870, 310), 4))

        # ОТОБРАЖЕНИЕ звезд для 1 уровня (или замочка)
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_1)) if game.STATE['levels'][
                                                                                         0] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_1)) if game.STATE['levels'][
                                                                                         0] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_1)) if game.STATE['levels'][
                                                                                         0] == 3 else None

        # ОТОБРАЖЕНИЕ звезд для 2 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_2)) if game.STATE['levels'][
                                                                                         1] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_2)) if game.STATE['levels'][
                                                                                         1] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_2)) if game.STATE['levels'][
                                                                                         1] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_2)) if game.STATE['levels'][
                                                                                         1] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_2[0] + 30, self.pos_lvl_2[1] - 70), (60, 60))) if \
            game.STATE['levels'][0] == 0 else None

        # ОТОБРАЖЕНИЕ звезд для 3 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_3)) if game.STATE['levels'][
                                                                                         2] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_3)) if game.STATE['levels'][
                                                                                         2] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_3)) if game.STATE['levels'][
                                                                                         2] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_3)) if game.STATE['levels'][
                                                                                         2] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_3[0] + 30, self.pos_lvl_3[1] - 70), (60, 60))) if \
            game.STATE['levels'][1] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 4 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_4)) if game.STATE['levels'][
                                                                                         3] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_4)) if game.STATE['levels'][
                                                                                         3] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_4)) if game.STATE['levels'][
                                                                                         3] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_4)) if game.STATE['levels'][
                                                                                         3] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_4[0] + 30, self.pos_lvl_4[1] - 70), (60, 60))) if \
            game.STATE['levels'][2] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 5 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_5)) if game.STATE['levels'][
                                                                                         4] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_5)) if game.STATE['levels'][
                                                                                         4] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_5)) if game.STATE['levels'][
                                                                                         4] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_5)) if game.STATE['levels'][
                                                                                         4] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_5[0] + 30, self.pos_lvl_5[1] - 70), (60, 60))) if \
            game.STATE['levels'][3] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 6 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_6)) if game.STATE['levels'][
                                                                                         5] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_6)) if game.STATE['levels'][
                                                                                         5] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_6)) if game.STATE['levels'][
                                                                                         5] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_6)) if game.STATE['levels'][
                                                                                         5] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_6[0] + 30, self.pos_lvl_6[1] - 70), (60, 60))) if \
            game.STATE['levels'][4] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 7 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_7)) if game.STATE['levels'][
                                                                                         6] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_7)) if game.STATE['levels'][
                                                                                         6] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_7)) if game.STATE['levels'][
                                                                                         6] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_7)) if game.STATE['levels'][
                                                                                         6] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_7[0] + 30, self.pos_lvl_7[1] - 70), (60, 60))) if \
            game.STATE['levels'][5] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 8 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_8)) if game.STATE['levels'][
                                                                                         7] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_8)) if game.STATE['levels'][
                                                                                         7] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_8)) if game.STATE['levels'][
                                                                                         7] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_8)) if game.STATE['levels'][
                                                                                         7] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_8[0] + 30, self.pos_lvl_8[1] - 70), (60, 60))) if \
            game.STATE['levels'][6] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 9 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_9)) if game.STATE['levels'][
                                                                                         8] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_9)) if game.STATE['levels'][
                                                                                         8] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_9)) if game.STATE['levels'][
                                                                                         8] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_9)) if game.STATE['levels'][
                                                                                         8] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_9[0] + 30, self.pos_lvl_9[1] - 70), (60, 60))) if \
            game.STATE['levels'][7] == -1 else None

        # ОТОБРАЖЕНИЕ звезд для 10 уровня
        self.map_sprites.add(Load_image(self.image_path_stars_0, self.pos_lvl_10)) if game.STATE['levels'][
                                                                                          9] == 0 else None
        self.map_sprites.add(Load_image(self.image_path_stars_1, self.pos_lvl_10)) if game.STATE['levels'][
                                                                                          9] == 1 else None
        self.map_sprites.add(Load_image(self.image_path_stars_2, self.pos_lvl_10)) if game.STATE['levels'][
                                                                                          9] == 2 else None
        self.map_sprites.add(Load_image(self.image_path_stars_3, self.pos_lvl_10)) if game.STATE['levels'][
                                                                                          9] == 3 else None
        self.map_sprites.add(
            Load_lock('images/lock.png', (self.pos_lvl_10[0] + 30, self.pos_lvl_10[1] - 70), (60, 60))) if \
            game.STATE['levels'][8] == -1 else None

        print(game.STATE['levels'])

        self.arcade_sprites.add(Arcade_right())
        self.arcade_sprites.add(Arcade_left())
        self.arcade_sprites.add(ArcadeDoor())
        self.arcade_sprites.add(Pink_line())
        self.arcade_sprites.add(Pink_line2())
        self.arcade_sprites.add(Arcade_button())

        game.update_background_music()
        self.main_menu()

    def draw_text(self, text, font, surface, x, y, color):       # Отрисовка текста
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):       # Запуск лобби
        while True:
            self.screen.fill(self.BLACK)
            if game.STATE['lang'] == 'ru':
                self.draw_text("Тайны подземелий", self.font, self.screen, self.screen_size[0] // 2,
                               self.screen_size[1] // 6, (160, 40, 222))
            else:
                self.draw_text("Secrets of the dungeons", self.font, self.screen, self.screen_size[0] // 2,
                               self.screen_size[1] // 6, (160, 40, 222))


            self.all_sprites.draw(self.screen)
            self.screen.blit(self.scaled_coin_image, (10, 10))
            self.draw_text(str(game.STATE['coins']), self.font, self.screen, 80, 24, (254, 254, 10))  # Счетчик монет

            if flag_skins:
                self.shop_skins_sprites.draw(self.screen)

                # Отображение статусов скинов
                # Обычный
                self.draw_text("Обычный", self.font, self.screen, 300, 240, 'black')
                if game.SKINS['man']:
                    if game.STATE['skin'][0] == 'man':
                        self.draw_text("ВЫБРАН", self.font, self.screen, 300, 590, 'black')
                    else:
                        self.draw_text("ИМЕЕТСЯ", self.font, self.screen, 300, 590, 'black')
                else:
                    self.draw_text("КУПИТЬ", self.font, self.screen, 300, 590, 'black')

                # Спектра
                self.draw_text("Спектра", self.font, self.screen, 600, 240, 'black')
                if game.SKINS['spectrum']:
                    if game.STATE['skin'][0] == 'spectrum':
                        self.draw_text("ВЫБРАН", self.font, self.screen, 600, 590, 'black')
                    else:
                        self.draw_text("ИМЕЕТСЯ", self.font, self.screen, 600, 590, 'black')
                else:
                    self.draw_text("КУПИТЬ", self.font, self.screen, 600, 590, 'black')

                # Джабба
                self.draw_text("Джабба", self.font, self.screen, 900, 240, 'black')
                if game.SKINS['froggy']:
                    if game.STATE['skin'][0] == 'froggy':
                        self.draw_text("ВЫБРАН", self.font, self.screen, 900, 590, 'black')
                    else:
                        self.draw_text("ИМЕЕТСЯ", self.font, self.screen, 900, 590, 'black')
                else:
                    self.draw_text("КУПИТЬ", self.font, self.screen, 900, 590, 'black')

                self.draw_text("Обычный", self.font, self.screen, 300, 240, 'black')
                self.draw_text("Спектра", self.font, self.screen, 600, 240, 'black')
                self.draw_text("Джабба", self.font, self.screen, 900, 240, 'black')

                self.draw_text("Типичный иска-", self.font_30, self.screen, 300, 450, 'black')
                self.draw_text("тель приключений", self.font_30, self.screen, 300, 470,'black')

                self.draw_text("Великий воин", self.font_30, self.screen, 600, 450, 'black')
                self.draw_text("из тени", self.font_30, self.screen, 600, 470, 'black')

                self.draw_text("Джабба Хат с", self.font_30, self.screen, 900, 450, 'black')
                self.draw_text("планеты Татуин", self.font_30, self.screen, 900, 470, 'black')

                self.draw_text("Бесплатно", self.font_50, self.screen, 300, 535, 'black')
                self.draw_text("50$", self.font, self.screen, 600, 535, 'black')
                self.draw_text("70$", self.font, self.screen, 900, 535, 'black')

                self.shop_skin_11.update()
                self.shop_skin_22.update()
                self.shop_skin_33.update()


            if flag_shop:        # Отрисовка спрайтов магазина
                self.shop_spell_sprites.draw(self.screen)

                self.draw_text("Купить", self.font, self.screen, 300, 590, 'black')
                self.draw_text("Купить", self.font, self.screen, 600, 590, 'black')
                self.draw_text("Купить", self.font, self.screen, 900, 590, 'black')

                self.draw_text("Щит", self.font, self.screen, 300, 240, 'black')
                self.draw_text("Магнит", self.font, self.screen, 600, 240, 'black')
                self.draw_text("Мороз", self.font, self.screen, 900, 240, 'black')

                self.draw_text("Дарует временную", self.font_30, self.screen, 300, 450, 'black')
                self.draw_text("защиту от ловушек", self.font_30, self.screen, 300, 470,'black')

                self.draw_text("Притягивает сокро-", self.font_30, self.screen, 600, 450, 'black')
                self.draw_text("вища поблизости", self.font_30, self.screen, 600, 470, 'black')

                self.draw_text("Замораживает всё", self.font_30, self.screen, 900, 450, 'black')
                self.draw_text("вокруг", self.font_30, self.screen, 900, 470, 'black')

                self.draw_text("15$", self.font, self.screen, 300, 535, 'black')
                self.draw_text("10$", self.font, self.screen, 600, 535, 'black')
                self.draw_text("20$", self.font, self.screen, 900, 535, 'black')


            if flag_map:  # Отрисовка спрайтов карты уровней
                self.map_sprites.draw(self.screen)
                self.draw_text("1", self.b_font, self.screen, 180, 310, (0, 0, 0))
                self.draw_text("2", self.b_font, self.screen, 180, 470, (0, 0, 0)) if game.STATE['levels'][
                                                                                          0] > 0 else None
                self.draw_text("3", self.b_font, self.screen, 390, 470, (0, 0, 0)) if game.STATE['levels'][
                                                                                          1] > 0 else None
                self.draw_text("4", self.b_font, self.screen, 390, 310, (0, 0, 0)) if game.STATE['levels'][
                                                                                          2] > 0 else None
                self.draw_text("5", self.b_font, self.screen, 600, 310, (0, 0, 0)) if game.STATE['levels'][
                                                                                          3] > 0 else None
                self.draw_text("6", self.b_font, self.screen, 600, 470, (0, 0, 0)) if game.STATE['levels'][
                                                                                          4] > 0 else None
                self.draw_text("7", self.b_font, self.screen, 810, 470, (0, 0, 0)) if game.STATE['levels'][
                                                                                          5] > 0 else None
                self.draw_text("8", self.b_font, self.screen, 810, 310, (0, 0, 0)) if game.STATE['levels'][
                                                                                          6] > 0 else None
                self.draw_text("9", self.b_font, self.screen, 1020, 310, (0, 0, 0)) if game.STATE['levels'][
                                                                                           7] > 0 else None
                self.draw_text("10", self.b_font, self.screen, 1020, 470, (0, 0, 0)) if game.STATE['levels'][
                                                                                            8] > 0 else None

            if flag_arcade:  # Отрисовка спрайтов аркады
                self.arcade_sprites.draw(self.screen)

                self.draw_text("Аркада", self.b_font, self.screen, self.screen_size[0] // 2,
                               self.screen_size[1] // 10 * 3, "Yellow")
                self.draw_text("Играть", self.b_font, self.screen, self.screen_size[0] // 2,
                               587, "black")
                self.arcade_sprites.update()

                self.draw_text('Очки', self.font_70, self.screen, 300, 400, (212, 0, 254))
                self.draw_text(str(game.STATE['score']), self.font_70, self.screen, 300, 480, (212, 0, 254))

                self.draw_text('Рекорд', self.font_70, self.screen, 900, 400, (212, 0, 254))
                self.draw_text(str(game.STATE['record']), self.font_70, self.screen, 900, 480, (212, 0, 254))

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
                    self.click_shop_spell(pos)
                    self.click_shop_skin(pos)

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
                elif isinstance(sprite, Settings):
                    game.Settings(self.screen)

    def click_arcade(self, pos):
        for sprite in self.arcade_sprites:
            if sprite.rect.collidepoint(pos) and flag_arcade:
                if isinstance(sprite, Arcade_button):
                    game.arcade()

    def click_lvl_map(self, pos):
        for sprite in self.map_sprites:
            if sprite.rect.collidepoint(pos) and flag_map:
                if isinstance(sprite, Lvl1):
                    game.map_level("level_1.txt", 13, 28)
                elif isinstance(sprite, Lvl2) and game.STATE['levels'][0] > 0:
                    game.map_level("level_2.txt", 12, 4)
                elif isinstance(sprite, Lvl3) and game.STATE['levels'][1] > 0:
                    game.map_level("level_3.txt", 17, 25)
                elif isinstance(sprite, Lvl4) and game.STATE['levels'][2] > 0:
                    game.map_level("level_4.txt", 11, 4)
                elif isinstance(sprite, Lvl5) and game.STATE['levels'][3] > 0:
                    game.map_level("level_5.txt", 13, 27)
                elif isinstance(sprite, Lvl6) and game.STATE['levels'][4] > 0:
                    game.map_level("level_6.txt", 15, 26)
                elif isinstance(sprite, Lvl7) and game.STATE['levels'][5] > 0:
                    game.map_level("level_7.txt", 31, 30)
                elif isinstance(sprite, Lvl8) and game.STATE['levels'][6] > 0:
                    game.map_level("level_8.txt", 5, 37)
                elif isinstance(sprite, Lvl9) and game.STATE['levels'][7] > 0:
                    game.map_level("level_9.txt", 6, 4)
                elif isinstance(sprite, Lvl10) and game.STATE['levels'][8] > 0:
                    game.map_level("level_10.txt", 22, 16)

    def click_shop_spell(self, pos):
        for sprite in self.shop_spell_sprites:
            if sprite.rect.collidepoint(pos) and flag_shop:
                if isinstance(sprite, Shop_spell_button_1):
                    if game.STATE['coins'] >= 15:
                        print('способность 1 куплена')
                        game.STATE['shield'] += 1
                        game.STATE['coins'] -= 15
                        game.save_game(game.STATE)
                elif isinstance(sprite, Shop_spell_button_2):
                    if game.STATE['coins'] >= 10:
                        print('способность 2 куплена')
                        game.STATE['magnet'] += 1
                        game.STATE['coins'] -= 10
                        game.save_game(game.STATE)
                elif isinstance(sprite, Shop_spell_button_3):
                    if game.STATE['coins'] >= 20:
                        print('способность 3 куплена')
                        game.STATE['freezing'] += 1
                        game.STATE['coins'] -= 20
                        game.save_game(game.STATE)

    def click_shop_skin(self, pos):
        for sprite in self.shop_skins_sprites:
            if sprite.rect.collidepoint(pos) and flag_skins:
                if isinstance(sprite, Shop_skin_button_1):
                    game.SKINS['man'] = True
                    game.STATE['skin'] = ['man', 6]
                    game.save_game(game.STATE)
                elif isinstance(sprite, Shop_skin_button_2):
                    if game.STATE['coins'] >= 50 and not game.SKINS['spectrum']:
                        game.SKINS['spectrum'] = True
                        game.STATE['skin'] = ['spectrum', 6]
                        game.STATE['coins'] -= 50
                        game.save_game(game.STATE)
                elif isinstance(sprite, Shop_skin_button_3):
                    if game.STATE['coins'] >= 70 and not game.SKINS['froggy']:
                        game.SKINS['froggy'] = True
                        game.STATE['skin'] = ['froggy', 5]
                        game.STATE['coins'] -= 70
                        game.save_game(game.STATE)


Lobby()
