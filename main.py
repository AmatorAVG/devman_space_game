import random
import time

import asyncio
import curses


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


def draw(canvas):
    canvas.border()
    curses.curs_set(False)

    max_y, max_x = canvas.getmaxyx()
    stars_coordinates = {(random.randint(1, max_y-2), random.randint(1, max_x-2)) for _ in range(100)}
    coroutines = [blink(canvas, y, x, symbol=random.choice('+*.:')) for y, x in stars_coordinates]
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
