from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока - красный:
APPLE_COLOR = (255, 0, 0)

# Основной цвет змейки - зеленый:
SNAKE_COLOR = (0, 255, 0)

# Цвет границы - светло-голубой:
BORDER_COLOR = (93, 216, 228)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    :param position: начальная позиция объекта в виде кортежа (x, y).
    """
    def __init__(self, position=(320, 240)):
        self.position = position
        self.body_color = None

    def draw(self):
        """
        Заглушка метод будет переопределенн для каждого класса.
        """
        pass


class Apple(GameObject):
    """
    Класс Apple, унаследованный от GameObject.
    Должен иметь атрибуты position, body_color, и метод randomize_position.
    """
    def __init__(self, position=(320,240)):
        super().__init__(position)
        # Тесты ждут, что будет атрибут body_color
        self.body_color = (255, 0, 0)
        self.border_color = BORDER_COLOR

    def randomize_position(self):
        """
        Устанавливает яблоку случайную позицию на поле.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.border_color, rect, 1)


class Snake(GameObject):
    """
    Класс Snake, унаследованный от GameObject.
    Должен иметь атрибуты: position, body_color, positions, direction,
    и методы: draw, get_head_position, move, reset, update_direction.
    """
    def __init__(self, start_position=(320,240)):
        super().__init__(start_position)
        self.body_color = (0, 255, 0)
        self.border_color = BORDER_COLOR
        # Список позиций сегментов
        self.positions = [start_position]
        self.direction = (1,0)
        # Атрибуты для логики
        self.next_direction = None
        self.last = None

    def draw(self):
        # Рисуем тело (все сегменты, кроме головы).
        for position in self.positions[1:]:
            body_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, body_rect)
            pygame.draw.rect(screen, self.body_color, body_rect, 2)

        # Рисуем голову (первый элемент списка).
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 2)

        # Затирание хвоста, если нужно.
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает координаты головы змейки.
        """
        return self.positions[0]

    def update_direction(self, new_direction):
        """
        Меняет направление змейки, если оно не противоположно текущему.
        """
        self.direction = new_direction

    def move(self):
        """
        Двигает змейку на одну ячейку в сторону self.direction.
        """
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        # Проверка выхода за границы - телепортация.
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        # Добавляем голову.
        self.positions.insert(0, new_head)

        # Если не растём, убираем хвост.
        self.last = self.positions.pop()

        if new_head in self.positions[1:]:
            self.show_game_over()
            self.reset()
            return

    def reset(self):
        """
        Сбрасывает параметры змейки к начальному состоянию.
        """
        self.positions = [self.position]  # Возвращаемся к позиции из GameObject
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def show_game_over(self):
        """
        Показываем сообщение если змейка съела себя.
        """
        font = pygame.font.Font(None, 50)  # Шрифт и размер
        text = font.render("Game Over!", True, (255, 0, 0))  # Красный текст
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Центр экрана
        screen.blit(text, text_rect)  # Рисуем текст
        pygame.display.flip()  # Обновляем экран
        pygame.time.delay(2000)  # Делаем паузу 2 секунды

def handle_keys(snake):
    """
    Функция для обработки нажатий клавиш и обновления направления змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """
    Основная функция игры.
    """
    pygame.init()

    # Создаем объекты змейки и яблока
    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    apple = Apple((
        randint(0, GRID_WIDTH - 1) * GRID_SIZE,
        randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    ))

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Управление и движение
        handle_keys(snake)
        snake.move()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            # Увеличиваем змейку: не убираем хвост
            snake.positions.append(snake.last)
            snake.last = None
            # Перемещаем яблоко
            apple.randomize_position()

        # Рисуем объекты
        snake.draw()
        apple.draw()

        pygame.display.flip()


# Запуск игры
if __name__ == '__main__':
    main()
