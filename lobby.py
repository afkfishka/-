import pygame
import sys
import os


class ShopSprites(pygame.sprite.Sprite):         # Кнопка магазина
    def __init__(self):
        super().__init__()
        # Магазин
        self.image = pygame.image.load('images/shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (355, 750)  # Позиционирование спрайта в центре экрана



class SkinsSprites(pygame.sprite.Sprite):         # Кнопка скинов
    def __init__(self):
        super().__init__()
        # Скины
        self.image = pygame.image.load('images/skin.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (460, 750)  # Позиционирование спрайта в центре экрана



class MapSprites(pygame.sprite.Sprite):         # Кнопка карты
    def __init__(self):
        super().__init__()
        # Скины
        self.image = pygame.image.load('images/map.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (665, 750)  # Позиционирование спрайта в центре экрана


class ArcadeSprites(pygame.sprite.Sprite):         # Кнопка аркады
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/arcade.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (870, 750)  # Позиционирование спрайта в центре экрана




class Lobby(pygame.sprite.Sprite):          # Лобби

    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Установка размера экрана
        self.screen_size = (1200, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Тайны подземелий")

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Загрузка шрифта
        self.font_path = 'fonts/zx_spectrum_7_bold.ttf'
        self.font_size = 60  # Размер шрифта
        self.font = pygame.font.Font(self.font_path, self.font_size)

        # Загрузка монеты
        self.coin_image = pygame.image.load('images/coin.png')

        # Создание группы спрайтов
        self.all_sprites = pygame.sprite.Group()

        self.all_sprites.add(ShopSprites())
        self.all_sprites.add(SkinsSprites())
        self.all_sprites.add(MapSprites())
        self.all_sprites.add(ArcadeSprites())


        self.main_menu()



    def draw_text(self, text, font, surface, x, y, color):   # Написание текста
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            self.draw_text("Тайны подземелий", self.font, self.screen, self.screen_size[0] // 2, self.screen_size[1] // 4, (147, 27, 222))
            self.all_sprites.draw(self.screen)



            # Создание текста


            self.screen.blit(self.coin_image, (0, 0))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.start_game()
                    elif event.key == pygame.K_2:
                        self.settings()
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    def start_game(self):
        # Здесь будет код для начала игры
        print("Игра начата!")
        pygame.time.delay(2000)  # Имитация задержки; замените реальной логикой игры

    def settings(self):
        # Здесь будет код для настроек
        print("Настройки игры")
        pygame.time.delay(2000)  # Имитация задержки; замените реальной логикой настроек


Lobby()