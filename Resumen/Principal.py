#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import sys
import locale
import argparse
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
from VResumen import VResumen


parser = argparse.ArgumentParser()
parser.add_argument('pclave', nargs = '+', help="Palabras claves a procesar, por ejemplo"
                                                "\nAPT_atomic_charges")
parser.add_argument('-M','-Mulliken',help='Muestra los datos de Mulliken')
parser.add_argument('file', nargs = 1, help="Nombre de archivo a procesar")

parser.parse_args()
def main(stdscr):
    vPrincipal = VResumen(sys.argv)

    vPrincipal.muestraVentana(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)