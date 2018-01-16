#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import sys
import locale
import argparse
import re
from Ag09principal import *
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


#Clase VResumen. Es la ventana que muestra al usuario el resumen del LOG
class VResumen:

    def __init__(self, parametrosentrada):
        self.ruta1 = parametrosentrada[len(parametrosentrada)-1]
        self.paramentrosresumen = parametrosentrada
        self.contenidoArchivo = NResumen.obtencontenidolog(self.ruta1)
        self.posypad1 = 0
        self.posypad2 = 0
        self.posxpad1 = 0
        self.posxpad2 = 0
        self.pad1yi = 2
        self.pad1xi = 0
        self.pad2xi = 0
        self.pad2yi = 0
        self.posycursor = 2
        self.posxcursor = 0
        self.padactivo = 1
        self.padBuscar = curses.newpad(1, 1000)
        self.tamypad1 = 32700
        self.tamypad2 = self.tamypad1
        self.pad1 = curses.newpad(self.tamypad1 + 1, 1000)
        self.contenidoPad = NResumen.hazresumen(self.contenidoArchivo, self.paramentrosresumen)
        self.pondatospad(self.contenidoPad)
        self.barraAyuda = "Presiona 'q' para salir"
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def pondatospad(self, contenido):
        y = 0
        for linea in contenido:
            self.pad1.addstr(y, 1, str(linea))
            y = y + 1

    def muestraventana(self, stdscr):
        k = 1
        stdscr.timeout(10)
        stdscr.keypad(True)
        while k != ord('q'):
            maxy, maxx = stdscr.getmaxyx()
            self.pad1xf = int(maxx - 1)
            self.pad1yf = maxy-2
            stdscr.attron(curses.color_pair(1))
            if len(self.ruta1) <= maxx:
                stdscr.addstr(1, 0, self.ruta1)
                stdscr.addstr(1, len(self.ruta1), " " * (self.pad1xf - len(self.ruta1)))
            else:
                ruta = self.ruta1[0:maxx]
                stdscr.addstr(1, 0, ruta)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(maxy-1, 0, self.barraAyuda)
            stdscr.attroff(curses.color_pair(2))
            if k == ord('1'):
                self.posycursor = self.pad1yi
                self.posxcursor = self.pad1xi
                self.padactivo = 1
            if k == curses.KEY_DOWN:
                self.posycursor = self.posycursor + 1
            if k == curses.KEY_UP:
                self.posycursor = self.posycursor - 1
            if k == curses.KEY_LEFT:
                self.posxcursor = self.posxcursor - 1
                if self.posxcursor <= 0:
                    self.posxpad1 = self.posxpad1 - 1
            if k == curses.KEY_RIGHT:
                self.posxcursor = self.posxcursor + 1
                if self.posxcursor >= maxx - 1:
                    self.posxpad1 = self.posxpad1 + 1
            if self.padactivo == 1:
                self.posycursor = max(self.pad1yi, self.posycursor)
                self.posycursor = min(self.pad1yf, self.posycursor)
                if self.posycursor > self.pad1yf - 1 and k != -1:
                    self.posypad1 = min(self.posypad1 + 1, self.tamypad1)
                if self.posycursor <= self.pad1yi + 1 and k != -1:
                    self.posypad1 = max(0, self.posypad1 - 1)
            self.posxcursor = max(0, self.posxcursor)
            self.posxcursor = min(maxx - 1, self.posxcursor)
            stdscr.move(self.posycursor, self.posxcursor)
            self.pad1.refresh(self.posypad1, self.posxpad1, self.pad1yi, self.pad1xi, self.pad1yf, self.pad1xf)
            k = stdscr.getch()

    @staticmethod
    def dialogobuscar(stdscr, padbuscar):
        stdscr.timeout(-1)
        y, x = stdscr.getmaxyx()
        curses.echo()
        padbuscar.addstr(0, 0, 'Palabra a buscar: ')
        padbuscar.refresh(0, 0, 0, 0, 1, x - 2)
        palabra = stdscr.getstr(0, 20, 100)
        curses.noecho()
        stdscr.timeout(10)
        return palabra


class NResumen:

    @staticmethod
    def obtencontenidolog(ruta):
        contenido = []
        contenidolog = DResumen.abrearchivo(ruta)
        for linea in contenidolog:
            lineaaux = linea.replace('\r', '')
            contenido.append(lineaaux)

        return contenido

    @staticmethod
    def hazresumen(contenidolog, parametros):
        terminacion = True
        r = NResumen.buscapalabra('natoms=', contenidolog)
        if r != -1:
            natomos = int(contenidolog[r].split()[1])
        else:
            n = NResumen.obtendatosmulliken(105, contenidolog)
            natomos = len(n)
        resumen = []
        matriz = []
        r = NResumen.buscapalabra(' #', contenidolog)
        comin = contenidolog[r]
        datosini = NResumen.obtendatosiniciales(contenidolog, r)
        for elemento in datosini:
            resumen.append(elemento)

        resumen.append('')
        r = NResumen.buscapalabra('termination', contenidolog)
        if r == -1:
            resumen.append('Error, no se encontraron datos de la terminación')
        else:

            if 'Normal' in contenidolog[r]:
                resumen.append('Terminación normal')
            else:
                terminacion = False
            resumen.append('')
            if 'opt' in comin:
                resumen.append('Datos de convergencia')
                r = NResumen.buscapalabra('converged\?', contenidolog)
                if r != -1:
                    datosconv = NResumen.obtendatosconvergencia(r, contenidolog)
                    for elemento in datosconv:
                        resumen.append(elemento)
                        resumen.append(elemento)
        resumen.append(' ')
        resumen.append('Numero de átomos: ' + str(natomos))
        resumen.append(' ')
        r = NResumen.buscapalabra('multiplicity', contenidolog)
        if r == -1:
            resumen.append('Error, no hay datos de carga y multiplicidad ')
        else:
            aux = contenidolog[r].split()
            resumen.append('Carga: ' + aux[2] + ' Multiplicidad: ' + aux[5])
            resumen.append(' ')
        r = NResumen.buscapalabra('HF=', contenidolog)
        if r == -1:
            resumen.append('Error, no hay datos HF')
        else:
            hf = ''
            index = contenidolog[r].index('HF=')
            for i in range(index + 4, len(contenidolog[r])):
                if contenidolog[r][i] == '\\' or contenidolog[r][i] == '|':
                    break
                hf = hf + contenidolog[r][i]
            resumen.append('Valor HF ' + hf)
            resumen.append(' ')
        r = NResumen.buscapalabra('pressure', contenidolog)
        if r == -1:
            resumen.append('Error, No se encontraron resultados para temperatura y presión')
        else:
            aux = contenidolog[r].split()
            resumen.append("Temperatura: " + aux[1] + ' ' + aux[2] + ' Presión: ' + aux[4] + ' ' + aux[5])
            resumen.append(' ')
        r = NResumen.buscapalabra('Zero-point correction', contenidolog)
        if r != -1:
            for i in range(r, len(contenidolog) - 1):
                resumen.append(contenidolog[i])
                if 'Vibrational' in contenidolog[i]:
                    break
        resumen.append('')
        if 'freq' in comin:
            r = NResumen.buscapalabra('imaginary frequencies \(', contenidolog)
            if r == -1:
                resumen.append('No hay frecuencias negativas')
                resumen.append(' ')
            else:
                fneg = NResumen.obtenfrequenciasnegativas(contenidolog, r)
                resumen.append('Hay ' + str(len(fneg)) + ' frecuencias negativas')
                for elemento in fneg:
                    resumen.append(elemento)
                resumen.append(' ')
        # A partir de aqui se mostrarán solo si la palabra se pasó como parámetro en la ejecucion del programa
        for elemento in parametros:
            if '--ALL' in parametros or '-a' in parametros:
                NResumen.opcmulliken(resumen, contenidolog)
                NResumen.opcacm(resumen, contenidolog, natomos)
                NResumen.opcasd(resumen, contenidolog, matriz, natomos)
                NResumen.opchsd(resumen, contenidolog, [], natomos)
                break
            if elemento == '--mulliken' or elemento == '-m':
                NResumen.opcmulliken(resumen, contenidolog)
            if elemento == '--atomic_charges_matrix' or elemento == '-acm':
                NResumen.opcacm(resumen, contenidolog, natomos)
            if elemento == '--atomic_spin_densities' or elemento == '-asd':
                NResumen.opcasd(resumen, contenidolog, matriz, natomos)
            if elemento == '--hirshfeld spin densities' or elemento == '-hsd':
                NResumen.opchsd(resumen, contenidolog, [], natomos)
        if not terminacion:
            resumen = []
            resumen.append('Terminación Erronea')
            for i in range(len(contenidolog)-1, 0, -1):
                if '        ' in contenidolog[i]:
                    for j in range(i+1, len(contenidolog)-1, 1):
                        resumen.append(contenidolog[j])
                    break
        return resumen

    @staticmethod
    def buscapalabraold(palabra, contenido):
        nl = 0
        pos = -1
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:
            res = expreg.search(linea)
            if res is None:
                pass
            else:
                pos = nl
                if palabra == ' #':
                    break
            nl = nl + 1
        return pos

    # Codigo redundante, optimizar !!!!!!!!!!!!!
    @staticmethod
    def buscapalabra(palabra, contenido):
        pos = -1
        nl = 0
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        if palabra == ' #':
            for linea in contenido:
                res = expreg.search(linea)
                if res is None:
                    pass
                else:
                    pos = nl
                    if palabra == ' #':
                        break
                nl = nl + 1
            return pos
        for i in range(len(contenido) - 1, 0, -1):
            res = expreg.search(contenido[i])
            if res is None:
                pass
            else:
                pos = i
                break
        return pos

    @staticmethod
    def obtendatosiniciales(contenido, posicioninicio):
        c1 = 0
        c2 = 0
        datosi = []
        for i in range(posicioninicio, 0, -1):
            if '***' in contenido[i]:
                c1 = c1 + 1
                if c1 == 2:
                    break
        for j in range(i, len(contenido), 1):
            datosi.append(contenido[j])
            if '-----' in contenido[j]:
                c2 = c2 + 1
                if c2 == 2:
                    break

        return datosi

    @staticmethod
    def obtenfrequenciasnegativas(contenido, posicioninicio):
        fneg = []
        expreg = re.compile(r'(Frequencies)\s+(-){2}\s+-?')
        for i in range(posicioninicio + 1, len(contenido) - 1):
            linea = contenido[i]
            if expreg.search(linea) is not None:
                aux = linea.split()
                for elemento in aux:
                    try:
                        f = float(elemento)
                        if f < 0.0:
                            fneg.append(str(f))
                        else:
                            return fneg
                    except:
                        pass
        return fneg

    @staticmethod
    def obtendatosconvergencia(lineainicio, contenido):
        datosconv = []
        for i in range(lineainicio, lineainicio + 5):
            datosconv.append(contenido[i])
        return datosconv

    # Modificar para que busque en al expresion regular 3 o mas flotantes y una letra al final

    @staticmethod
    def obtendatosmulliken(lineainicio, contenido):
        datos = []
        vaux = 0

        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+-?\d+.?\d+\s+[A-Z]?$')
        for i in range(lineainicio + 1, len(contenido) - 1):
            if expreg.search(contenido[i]) is not None and vaux < 2:
                cad = contenido[i].split()
                datos.append(cad[len(cad) - 1] + '\n')
                vaux = 1
            else:
                if vaux == 1:
                    break
                pass
        return datos

    @staticmethod
    def obtenmatriz(pos, contenido, na):
        matriz = []
        for i in range(na):
            matriz.append([0] * na)
        ultimapos = 0
        natomos = 0
        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+(-?\d+\.?\d+\s*)+$')
        for linea in contenido[pos + 2:]:
            if expreg.search(linea) is not None:
                aux = linea.split()[2:]
                ind = ultimapos
                for elemento in aux:
                    matriz[natomos][ind] = elemento
                    ind = (ind + 1) % na
                natomos = (natomos + 1) % na
            else:
                ultimapos = ultimapos + 6
                if ultimapos >= na:
                    break
        return matriz

    @staticmethod
    def buscarlinea(palabra, contenido):
        nl = 0
        posiciones = []
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:
            res = expreg.search(linea)
            if res is None:
                pass
            else:
                posiciones.append(nl)
            nl = nl + 1
        return posiciones

    @staticmethod
    def opcacm(resumen, contenidolog, natomos):
        r = NResumen.buscapalabra('Condensed to atoms', contenidolog)
        if r == -1 or 'Mulliken atomic charges:' in contenidolog[r + 1]:
            resumen.append('No hay datos de la matriz ')
        else:
            matriz = NResumen.obtenmatriz(r, contenidolog, natomos)
            """resumen.append('Atomic Charges Matrix')
            resumen.append(' ')
            for linea in matriz:
                caux = ''
                for elemento in linea:
                    caux += str(elemento) + '\t'
                resumen.append(caux)"""
            diagonal = ''
            resumen.append('Valores de la diagonal de Atomic Charges Matrix: ')
            for i in range(len(matriz)):
                diagonal = diagonal + str(matriz[i][i]) + ' '
                resumen.append(matriz[i][i])
            resumen.append(' ')
        resumen.append(' ')

    @staticmethod
    def opcasd(resumen, contenidolog, matriz, natomos):
        r = NResumen.buscapalabra('Atomic-Atomic Spin Densities.', contenidolog)
        diagonal = ''
        for i in range(len(matriz)):
            diagonal = diagonal + str(matriz[i][i]) + ' '
            resumen.append(matriz[i][i])
        resumen.append(' ')
        if r == -1:
            resumen.append('No hay datos de la matriz de densidades de spin')
        else:
            matriz2 = NResumen.obtenmatriz(r, contenidolog, natomos)
            """resumen.append('Atomic Spin Densities Matrix\n\n')
            resumen.append(' ')
            for linea in matriz2:
                caux = ''
                for elemento in linea:
                    caux += str(elemento) + '\t'
                resumen.append(caux)"""
            resumen.append(' ')
            diagonal = ''
            resumen.append('Valores de la diagonal de Atomic-Atomic Spin Densities: ')
            for i in range(len(matriz2)):
                diagonal = diagonal + str(matriz2[i][i]) + ' '
                resumen.append(matriz2[i][i])
            resumen.append(' ')

    @staticmethod
    def opchsd(resumen, contenidolog, matriz, natomos):
        r = NResumen.buscapalabra('Hirshfeld spin densities, ', contenidolog)
        if r == -1:
            resumen.append('No hay datos de la matriz Hirshfeld spin densities')
        else:
            resumen.append(' Hirshfeld spin densities:\n\n')
            resumen.append('')
            resumen.append('Átomo\tSpin Densities\tCharges')
            resumen.append('')
            for i in range(r + 2, r + natomos + 2, 1):
                resumen.append('\t'.join(contenidolog[i].split()[1:4]))
            resumen.append(' ')

    @staticmethod
    def opcapt(resumen, contenidolog):
        r = NResumen.buscapalabra('APT atomic charges:', contenidolog)
        aptch = []
        if r == -1:
            resumen.append('Error, no se encontraron datos')
        else:
            aptch = NResumen.obtendatosmulliken(r, contenidolog)
        r = NResumen.buscapalabra('APT Atomic charges with hydrogens summed', contenidolog)
        aths = []
        if r == -1:
            resumen.append('Error, no se encontraron datos')
            resumen.append('')
        else:
            aths = NResumen.obtendatosmulliken(r, contenidolog)
            resumen.append('APT atomic charges \t APT atomic charges hydrogens summed')
        for i in range(len(aptch)):
            resumen.append(str(float(aptch[i])) + '\t\t\t' + str(aths[i]))

    @staticmethod
    def opcmulliken(resumen, contenidolog):
        resumen.append('')
        r = NResumen.buscapalabra('Mulliken atomic charges:', contenidolog)
        aptch = []
        if not r == -1:
            aptch = NResumen.obtendatosmulliken(r, contenidolog)
            resumen.append('Mulliken atomic charges ')
            resumen.append('')
            for i in range(len(aptch)):
                resumen.append(str(float(aptch[i])))
        r = NResumen.buscapalabra('^ Mulliken atomic spin', contenidolog)
        aths = []
        if not r == -1:
            aths = NResumen.obtendatosmulliken(r, contenidolog)
            resumen.append('Mulliken atomic spin densities')
            for i in range (len(aths)):
                resumen.append(str(aths[i]))
        resumen.append('')

class DResumen:


    @staticmethod
    def abrearchivo(ruta):
        archivo = open(ruta)
        contenido = archivo.readlines()
        archivo.close()
        return contenido