import curses
import sys

from Resumen.VResumen import VValidar
from VLector import VLector


def main(stdscr):
    if len(sys.argv) == 3:
        vPrincipal = VLector(sys.argv)
    else:
        vPrincipal = VValidar(sys.argv)
    vPrincipal.muestraVentana(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

