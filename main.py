import random
import time

import asyncio
import curses

from curses_tools import draw_frame


async def blink(canvas, row, column, symbol='*'):
    while True:
        for i in range(random.randint(1, 5)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(15):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(1):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, frame_1, frame_2):
    while True:
        for frame in (frame_1, frame_2):
            draw_frame(canvas, 8, 35, frame)
            for i in range(2):
                await asyncio.sleep(0)
            draw_frame(canvas, 8, 35, frame, negative=True)


def draw(canvas):

    with open('frames/rocket_frame_1.txt', 'r', encoding='utf8') as file:
        frame_1 = file.read()
    with open('frames/rocket_frame_2.txt', 'r', encoding='utf8') as file:
        frame_2 = file.read()

    canvas.border()
    curses.curs_set(False)

    max_y, max_x = canvas.getmaxyx()
    stars_coordinates = {(random.randint(1, max_y-2), random.randint(1, max_x-2)) for _ in range(100)}
    coroutines = [blink(canvas, y, x, symbol=random.choice('+*.:')) for y, x in stars_coordinates]
    coroutines.append(fire(canvas, 20, 15, rows_speed=-0.3, columns_speed=0))
    coroutines.append(animate_spaceship(canvas, frame_1, frame_2))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(0.1)
        if len(coroutines) == 0:
            break
    time.sleep(5)
    # while True:
    #     canvas.addstr(row, column, '*', curses.A_DIM)
    #     canvas.refresh()
    #     time.sleep(2)
    #     canvas.addstr(row, column, '*')
    #     canvas.refresh()
    #     time.sleep(0.3)
    #     canvas.addstr(row, column, '*', curses.A_BOLD)
    #     canvas.refresh()
    #     time.sleep(0.5)
    #     canvas.addstr(row, column, '*')
    #     canvas.refresh()
    #     time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
