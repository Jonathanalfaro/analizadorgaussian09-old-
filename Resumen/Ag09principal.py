#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import sys
import locale
import argparse
from VResumen import VResumen
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mulliken', help='Muestra los datos de Mulliken', action="store_true")
parser.add_argument('-acm', '--atomic_charges_matrix', help='Muestra la matriz de cargas atomicas y su diagonal',
                    action="store_true")
parser.add_argument('-asd', '--atomic_spin_densities', help='Muestra la matriz de densidades atómicas y su diagonal',
                    action="store_true")
parser.add_argument('-hsd', '--hirshfeld_spin_densities', help='Muestra la matriz de Hirshfeld', action="store_true")
parser.add_argument('-a', '--ALL', help='Muestra todos los datos', action="store_true")
parser.add_argument('file', nargs=1, help="Nombre de archivo a procesar")
parser.parse_args()


def main(stdscr):
    vprincipal = VResumen(sys.argv)
    vprincipal.muestraventana(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
