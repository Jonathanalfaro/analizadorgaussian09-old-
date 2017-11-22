import curses
import sys

from VResumen import VResumen



def main(stdscr):
    vPrincipal = VResumen(sys.argv[1])
    vPrincipal.muestraVentana(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)