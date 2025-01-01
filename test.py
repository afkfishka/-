import pygame
import sys


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

class Achivements(pygame.sprite.Sprite):         # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/menu_achievements1.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (1160, 30)  # Позиционирование спрайта в центре экрана


class Settings(pygame.sprite.Sprite):         # Кнопка достижений
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/menu_settings1.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (1100, 30)  # Позиционирование спрайта в центре экрана


class Lobby(pygame.sprite.Sprite):  # Лобби
    def __init__(self):
        pygame.init()
        self.screen_size = (1200, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Тайны подземелий")

        self.BLACK = (0, 0, 0)

        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.coin_image = pygame.image.load('images/menu_coin.png')
        self.scaled_coin_image = pygame.transform.scale(self.coin_image, (40, 40))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(ShopSprites())
        self.all_sprites.add(SkinsSprites())
        self.all_sprites.add(MapSprites())
        self.all_sprites.add(ArcadeSprites())
        self.all_sprites.add(Achivements())
        self.all_sprites.add(Settings())

        self.main_menu()

    def draw_text(self, text, font, surface, x, y, color):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            self.draw_text("Тайны подземелий", self.font, self.screen, self.screen_size[0] // 2, self.screen_size[1] // 4, (160, 40, 222))

            self.all_sprites.draw(self.screen)
            self.screen.blit(self.scaled_coin_image, (10, 10))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_click(pos)

            pygame.display.flip()

    def check_click(self, pos):
        for sprite in self.all_sprites:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, ShopSprites):
                    self.shop_function()
                elif isinstance(sprite, SkinsSprites):
                    self.skins_function()
                elif isinstance(sprite, MapSprites):
                    self.map_function()
                elif isinstance(sprite, ArcadeSprites):
                    self.arcade_function()
                elif isinstance(sprite, Achivements):
                    self.achivements_function()
                elif isinstance(sprite, Settings):
                    self.settings_function()

    def shop_function(self):
        print("Открыт магазин!")
        pygame.time.delay(2000)  # Имитация задержки

    def skins_function(self):
        print("Выбор скинов!")
        pygame.time.delay(2000)  # Имитация задержки

    def map_function(self):
        print("Открыта карта!")
        pygame.time.delay(2000)  # Имитация задержки

    def arcade_function(self):
        print("Запуск аркады!")
        pygame.time.delay(2000)  # Имитация задержки

    def achivements_function(self):
        print("Список достижений открыт!")
        pygame.time.delay(2000)  # Имитация задержки

    def settings_function(self):
        print("Запуск настроек!")
        pygame.time.delay(2000)  # Имитация задержки
Lobby()
