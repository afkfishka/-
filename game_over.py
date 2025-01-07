import pygame

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

class Death():
    def __init__(self):
        pygame.init()
        size = [1200, 800]
        self.screen = pygame.display.set_mode(size)
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
            self.screen.fill((0, 0, 0))

            self.game_over.draw(self.screen)
            self.draw_text("Рестарт", self.m_font, self.screen, 532, 487, "black")
            self.draw_text("Меню", self.m_font, self.screen, 697, 487, "black")
            self.draw_text("Game over", self.font80, self.screen, 600, 390, "black")
            self.draw_text("Уровень", self.font, self.screen, 570, 305, "black")
            self.draw_text("1", self.font, self.screen, 680, 305, "black")

            # рисуем
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def check_click(self, pos):
        for sprite in self.game_over:
            if sprite.rect.collidepoint(pos):
                if isinstance(sprite, Restart):
                    print('restart')
                elif isinstance(sprite, Home):
                    print('back to lobby')

Death()