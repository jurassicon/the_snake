
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока - красный.
APPLE_COLOR = (255, 0, 0)

# Основной цвет змейки - зеленый.
SNAKE_COLOR = (0, 255, 0)

# Цвет границы - светло-голубой.
BORDER_COLOR = (93, 216, 228)

# Скорость движения змейки.
SPEED = 15

# Настройка игрового окна.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')

# Настройка времени.
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    Position: начальная позиция объекта в виде кортежа (x, y).
    """

    def __init__(self, position=SCREEN_CENTER):
        self.position = position
        self.body_color = None
        self.border_color = None

    def draw(self):
        """Заглушка метод будет переопределенн для каждого класса."""
        raise (NotImplementedError
               ('Draw() должен быть переопределенн в дочернем классе.'))

    def draw_cell(self, position, color=None, border_color=None):
        """
        Отрисовывает клетку на экране.

        Position: Кортеж (x, y), координаты клетки.
        Color: Цвет заливки клетки. Если нет, используется
        self.body_color.
        Border_color: Цвет границы клетки. Если нет, используется
        self.border_color.
        """
        if color is None:
            color = self.body_color  # Если цвет не задан,
            # используем цвет объекта.
        if border_color is None:
            border_color = self.border_color  # Если цвет границы нет,
            # используем цвет границы объекта.

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))  # Создаём
        # прямоугольник с позицией и размером.
        pg.draw.rect(screen, color, rect)  # Рисуем заливку клетки.
        pg.draw.rect(screen, border_color, rect, 1)  # Рисуем границу
        # клетки.


class Apple(GameObject):
    """
    Класс Apple, унаследованный от GameObject.
    Должен иметь атрибуты position, body_color,
    и метод randomize_position.
    """

    def __init__(
            self,
            position=SCREEN_CENTER,
            body_color=None,
            border_color=None,
            occupied_positions=None
    ):
        super().__init__(position)
        self.body_color = body_color if body_color is not None else APPLE_COLOR
        self.border_color = border_color if border_color is not None \
            else BORDER_COLOR
        self.reset()
        self.randomize_position(occupied_positions)

    def reset(self):
        """Сбрасывает параметры объекта к начальному состоянию."""
        self.positions = [self.position]
        self.next_direction = None
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def randomize_position(self, occupied_positions=None):
        """
        Устанавливает яблоку случайную позицию на поле, избегая занятых клеток.

        Occupied_positions: Набор координат, которые уже заняты
        (например, телом змейки).
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if (occupied_positions is None or new_position not in
                    occupied_positions):
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """
    Класс Snake, унаследованный от GameObject.
    Должен иметь атрибуты: position, body_color, positions, direction,
    и методы: draw, get_head_position, move, reset, update_direction.
    """

    def __init__(self, start_position=SCREEN_CENTER):
        super().__init__(start_position)
        self.body_color = SNAKE_COLOR
        self.border_color = BORDER_COLOR

        # Список позиций сегментов.
        self.positions = [start_position]
        self.direction = RIGHT

        # Атрибуты для логики.
        self.last = None

    def draw(self):
        """Отрисовывает тело змейки.

        Рисует все сегменты змейки, кроме головы, используя цвет тела.
        Затем отдельно рисует голову с обводкой.
        """
        # Рисуем тело змейки
        for position in self.positions[1:]:
            self.draw_cell(position)  # Тело змейки.

        # Рисуем голову (первый элемент списка).
        self.draw_cell(self.positions[0], border_color=BORDER_COLOR)

        # Затирание хвоста, если нужно.
        if self.last is not None:
            self.draw_cell(self.last, color=BOARD_BACKGROUND_COLOR,
                           border_color=BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Меняет направление змейки, если оно не противоположно текущему."""
        self.direction = new_direction

    def move(self):
        """Двигает змейку на одну ячейку в сторону self.direction."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Добавляем голову.
        self.positions.insert(0, new_head)

        # Если не растём, убираем хвост.
        self.last = self.positions.pop()

    def reset(self):
        """Сбрасывает параметры змейки к начальному состоянию."""
        self.positions = [self.position]  # Возвращаемся к позиции
        # из GameObject.
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    @staticmethod
    def show_game_over():
        """Показываем сообщение если змейка съела себя."""
        font = pg.font.Font(None, 50)  # Шрифт и размер.
        text = font.render('Game Over!', True, (255, 0, 0))  # Красный текст.
        text_rect = text.get_rect(center=SCREEN_CENTER)  # Центрируем текст.
        screen.blit(text, text_rect)  # Рисуем текст.
        pg.display.flip()  # Обновляем экран.
        pg.time.delay(2000)  # Делаем паузу 2 секунды.

    def grow(self):
        """Увеличивает длину змейки за счёт последнего сохранённого сегмента
        (self.last).
        """
        if self.last is not None:
            self.positions.append(self.last)
            self.last = None


def handle_keys(snake):
    """Функция для обработки нажатий клавиш и обновления направления змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    pg.init()

    # Создаём змейку.
    snake = Snake(SCREEN_CENTER)

    # Создаём яблоко с учётом занятых позиций.
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Управление и движение.
        handle_keys(snake)
        snake.move()
        # Проверяем, не врезалась ли змейка в себя.
        if snake.get_head_position() in snake.positions[1:]:
            snake.show_game_over()  # Вызываем Game Over.
            snake.reset()
            continue  # Или просто return, если хотим сразу выйти из цикла,
            # в зависимости от логики.

        # Проверяем, съела ли змейка яблоко.
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(occupied_positions=snake.positions)
            # Перемещаем яблоко.

        # Отрисовка объектов.
        snake.draw()
        apple.draw()

        # Обновление экрана.
        pg.display.flip()


# Запуск игры.
if __name__ == '__main__':
    main()
