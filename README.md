# The Snake game

Classic snake game implemented in Python using the Pygame library.

## About


https://github.com/user-attachments/assets/9ba0c491-ca34-422e-a0f6-6edc3472bd85


In the game you control a snake, which must eat apples that appear on the
screen. With each apple eaten, the snake grows in length. The game ends when
the snake collides with itself.

## Features

- **Control**: Use the arrow keys (Up, Down, Left, Right) to change the snake's
  direction.
- **Sound effects**: When the snake collides with itself, the game ends and the
  sound effect plays if the `game_over.wav` file is present in the project
  directory.
- **Game mechanics**: The snake can move through the screen boundaries,
  appearing on the opposite side.
- **OOP**: Code is written using object-oriented programming principles.

## System requirements

- Python 3.12+
- Pygame 2.5.2+

## Installation and running

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jurassicon/the_snake
   cd the_snake
   ```

2. **Install requirements**:
   A virtual environment is required to avoid dependency conflicts with other
   projects.
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the game**:
   ```bash
   python the_snake.py
   ```

## Project structure

- `the_snake.py` - Main game logic and rendering is located here.
- `game_over.wav` - Sound file, played on the game over screen.
- `requirements.txt` - List of required libraries for the project to work.
- `tests/` - Directory with tests for checking the code structure and
  main logic.

## Development

For checking the code quality, `flake8` is used and `pytest` for testing.

For running tests:

```bash
pytest
```

For checking code style:

```bash
flake8 .
```

## Author

Iurii Cherkasov

- **[Telegram](https://t.me/iurii_cherkasov)**
