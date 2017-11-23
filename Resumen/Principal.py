import curses
import sys
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
from VResumen import VResumen



def main(stdscr):
    vPrincipal = VResumen(sys.argv[1])
    vPrincipal.muestraVentana(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)