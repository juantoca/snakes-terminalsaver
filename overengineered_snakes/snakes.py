#! /usr/bin/env python

import shutil
import random
import curses
from backend import Handler
from overengineered_snakes.cli.parse_args import options
from overengineered_snakes.configs.config import Config
from overengineered_snakes.renderers.curses import CursesRenderer


def main(stdscr, config: Config):  # The root method, do not annoy him
    size = shutil.get_terminal_size()  # Gets terminal size so curses won't complain
    colors = []
    for i in range(0, curses.COLORS):  # Curses shit
        colors.append(i)
    mapa = Handler(size[1], size[0]-1, colors, clean=config.clear,
                   percentage=config.percentage,
                   max_length=config.max_length, headlimit=config.limit,
                   random_weight=config.random_weighted, crazy_behaviour=config.crazy,
                   body_char=config.body, head_char=config.head)
    renderer = CursesRenderer()
    # We init the game class, just read
    if config.seed is not False:  # We try to set the seed of the random module based on the config
        random.seed(a=config.seed)
    else:
        random.seed(a=random.randint(0, 100))
    if config.justCalculating is not True:  # Graphic Mode
        import time
        while True:
            tmpsize = shutil.get_terminal_size()
            tiempo = time.time()
            status = mapa.run(gen=True)
            try:
                renderer.render(mapa)
            except KeyboardInterrupt:
                exit()
            if config.filled and status["filled"] and status["snakes"] == 0:
                time.sleep(config.timeout)
                raise curses.error
            if tmpsize != size:  # If the window has been resized, relaunch the app
                raise curses.error
            tiempo = time.time() - tiempo
            try:
                time.sleep(1 / config.fps - tiempo)
            except KeyboardInterrupt:
                exit()
            except:
                pass
    else:  # Verbose Mode
        returneo = None
        for x in range(0, config.cicles):
            returneo = mapa.run(gen=True)
        stdscr.addstr(str(returneo))
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    while True:
        config: Config = options()
        try:
            curses.wrapper(main, config)
        except KeyboardInterrupt:
            exit()
        except curses.error:
            pass
