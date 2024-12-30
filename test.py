import pygame

# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen = pygame.display.set_mode((800, 600))


# Определение класса спрайта
class ShopSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/shop.png')  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника для позиционирования
        self.rect.center = (400, 300)  # Позиционирование спрайта в центре экрана


# Создание группы спрайтов
all_sprites = pygame.sprite.Group()
shop_sprite = ShopSprite()
all_sprites.add(shop_sprite)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка всех спрайтов на экране
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
