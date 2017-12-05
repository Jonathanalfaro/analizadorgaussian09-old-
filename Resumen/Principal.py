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
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
parser.parse_args()
def main(stdscr):
    vPrincipal = VResumen(sys.argv)

    vPrincipal.muestraVentana(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)