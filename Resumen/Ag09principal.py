#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import curses
    import random
    import sys
    import locale
    import argparse
    import re
    import csv
    from Ag09principal import *
except ImportError as ie:
    print '{0} install first'.format(ie)
    exit(0)

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
parser = argparse.ArgumentParser()
parser.add_argument('-hf', help='Muestra el valor de la energía de Hirshfeld', action="store_true")
parser.add_argument('-m', '--mulliken', help='Muestra las cargas atómicas de Mulliken', action="store_true")
parser.add_argument('-apt', '--APT_atomic', help='Muestra atomic polar tensor charges (APT)', action="store_true")
parser.add_argument('-tq', '--thermochemical', help='Muestra los datos termoquímicos como dipolo, temperatura, presión, etc', action="store_true")
parser.add_argument('-acm', '--atomic_charges_matrix', help='Muestra la diagonal de la matriz de cargas atómicas',
                    action="store_true")
parser.add_argument('-asd', '--atomic_spin_densities', help='Muestra la diagonal de matriz de densidades atómicas',
                    action="store_true")
parser.add_argument('-hsd', '--hirshfeld_spin_densities', help='Muestra las densidades de spin y las cargas de la matriz de Hirshfeld', action="store_true")
parser.add_argument('-nao', nargs = '?' , action='store', dest='Atomo', default = 'N' ,help='Muestra Natural atomic orbital occupancies')
parser.add_argument('-mep', help='Muestra molecular electrostatic potential', action = "store_true")
parser.add_argument('-a', '--ALL', help='Muestra todos los datos', action="store_true")
parser.add_argument('-e', '--exporta', help='Exporta los datos a un archivo separado por comas (CSV)', action="store_true")
parser.add_argument('-t', '--texto', help='Muestra los resultados directamente en la terminal', action="store_true")
parser.add_argument('-d', '--debug', help='No imprime nada', action="store_true")
parser.add_argument('file', nargs='+', help="Nombre de archivo a procesar")
args = parser.parse_args()

''' Método principal, manda a llamar a la ventana principal segun el modo
    Si es modo curses abre la ventana interactiva, si es modo terminal
    pone todo en la terminal.

    :param stdscr: estandar screen de curses

'''


def main(stdscr):
    vprincipal = VResumenCur(sys.argv)
    vprincipal.muestraventana(stdscr)


if __name__ == "__main__":
    modo = 'curses'
    for elemento in sys.argv:
        if elemento == '-t' or elemento == '--texto':
            modo = 'term'
            break
    if modo == 'term':
        for archivo in args.file:
            vprincipal = VResumenTer(sys.argv, archivo)

    else:
        curses.wrapper(main)


# Clase VResumen. Es la ventana que muestra al usuario el resumen del LOG
class VResumenCur:
    ''' Clase de vista para curses
        :param parametrosentrada: La lista de los parametros ingresados
        en la terminal para ejecutar el programa.(Argumentos, ruta)

    '''

    def __init__(self, parametrosentrada):
        ''' Constructor para la clase VResumenCur.

        Inicializa el objeto y pone los datos del log en el pad de curses
        que es donde se muestra el resumen

        :param parametrosentrada:


        '''
        self.contenidoPad = []
        self.ruta1 = parametrosentrada[len(parametrosentrada) - 1]
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
        try:
            if 'Error' in self.contenidoArchivo[0] or 'no es' in self.contenidoArchivo:
                self.contenidoPad.append(self.contenidoArchivo[0])
            else:
                self.contenidoPad = NResumen.hazresumen(self.contenidoArchivo, self.paramentrosresumen, self.ruta1)
        except:
            self.contenidoPad.append('No es un archivo válido')
        self.tamypad1 = len(self.contenidoPad)
        self.tamxpad1 = 1000
        self.pad1 = curses.newpad(self.tamypad1 + 1, 1000)
        self.pondatospad(self.contenidoPad)
        self.barraAyuda = "Presiona 'q' para salir 'e' para exportar"
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def pondatospad(self, contenido):

        ''' Método que se encarga de llenar el pad.

        :param contenido: Lo que se va a poner en el pad


        '''
        y = 0
        for linea in contenido:
            self.pad1.addstr(y, 1, str(linea))
            y = y + 1

    def muestraventana(self, stdscr):
        ''' Se encarga de mostrar la ventana y actualizarla.

        Actualiza lo mostrado en el modo curses segun la tecla presionada

        :param stdscr:


        '''
        k = 1
        stdscr.timeout(10)
        stdscr.keypad(True)
        self.posycursor = 0
        self.posxcursor = 0
        while k != ord('q'):
            maxy, maxx = stdscr.getmaxyx()
            self.pad1xf = int(maxx - 1)
            self.pad1yf = maxy - 2
            stdscr.attron(curses.color_pair(1))
            if len(self.ruta1) <= maxx:
                stdscr.addstr(1, 0, self.ruta1)
                stdscr.addstr(1, len(self.ruta1), " " * (self.pad1xf - len(self.ruta1)))
            else:
                ruta = self.ruta1[0:maxx]
                stdscr.addstr(1, 0, ruta)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(maxy - 1, 0, self.barraAyuda)
            stdscr.attroff(curses.color_pair(2))

            if k == ord('e'):
                status = -1
                mensaje = ''
                ruta = self.dialogoexportar(stdscr, self.padBuscar, self.contenidoPad)

            if k == curses.KEY_DOWN:
                self.posycursor = self.posycursor + 1
            if k == curses.KEY_UP:
                self.posycursor = self.posycursor - 1
            if k == curses.KEY_LEFT:
                self.posxcursor = self.posxcursor - 1
            if k == curses.KEY_RIGHT:
                self.posxcursor = self.posxcursor + 1

            if self.posycursor > self.pad1yf:
                self.posypad1 = min(self.posypad1 + 1, self.tamypad1 - (self.pad1yf - self.pad1yi))
            if self.posycursor < self.pad1yi:
                self.posypad1 = max(0, self.posypad1 - 1)

            if self.posxcursor > self.pad1xf:
                self.posxpad1 = min(self.posxpad1 + 1, self.tamxpad1)
            if self.posxcursor <= self.pad1xi + 1:
                self.posxpad1 = max(0, self.posxpad1 - 1)

            self.posycursor = max(self.pad1yi, self.posycursor)
            self.posycursor = min(self.pad1yf, self.posycursor)
            self.posxcursor = max(0, self.posxcursor)
            self.posxcursor = min(maxx - 1, self.posxcursor)
            stdscr.move(self.posycursor, self.posxcursor)
            if k == curses.KEY_RESIZE:
                self.posypad1 = min(self.pad1yf - self.pad1yi, self.posypad1)
            self.pad1.refresh(self.posypad1, self.posxpad1, self.pad1yi, self.pad1xi
                              , self.pad1yf, self.pad1xf)
            k = stdscr.getch()

    @staticmethod
    def dialogobuscar(stdscr, padbuscar):

        ''' Sirve para mostrar la entrada de busqueda un patrón en el resumen.

        :param stdscr:
        :param padbuscar: pad donde se ingresa la palabra para buscar en el resumen
        :return: palabra: devuelve la palabra ingresada por el usuario

        '''

        stdscr.timeout(-1)
        y, x = stdscr.getmaxyx()
        curses.echo()
        padbuscar.addstr(0, 0, 'Palabra a buscar: ')
        padbuscar.refresh(0, 0, 0, 0, 1, x - 2)
        palabra = stdscr.getstr(0, 20, 100)
        curses.noecho()
        stdscr.timeout(10)

        return palabra

    @staticmethod
    def dialogoexportar(stdscr, padbuscar, contenidopad):

        ''' Sirve para mostrar la entrada de busqueda un patrón en el resumen.

        :param stdscr:
        :param padbuscar: pad donde se ingresa la palabra para buscar en el resumen
        :return: palabra: devuelve la palabra ingresada por el usuario

        '''

        stdscr.timeout(-1)
        y, x = stdscr.getmaxyx()
        curses.echo()
        padbuscar = curses.newpad(1, 1000)
        padbuscar.addstr(0, 0, 'Ruta y nombre del archivo: ')
        padbuscar.refresh(0, 0, 0, 0, 1, x - 2)
        ruta = stdscr.getstr(0, 30, 100)
        curses.noecho()
        stdscr.timeout(10)
        status, mensaje = NResumen.exporta(contenidopad, ruta)
        mensaje = str(mensaje)
        padbuscar.addstr(0, 0, mensaje)
        padbuscar.refresh(0, 0, 0, 0, 1, x - 2)
        padbuscar = curses.newpad(1, 1000)


class NResumen:
    ''' Clase lógica NResumen, sirve para hacer el resumen.



    '''

    @staticmethod
    def obtencontenidolog(ruta):
        ''' Obtiene el contenido del log del cual se va a hacer el resumen.

        Obtiene el texto del archivo .log o .out llamando a un objeto de la
        clase DResumen.

        :param ruta: la ruta del archivo a abrir
        :return: contenido: El texto del archivo .log o .out

        '''
        contenido = []
        contenidolog = DResumen.abrearchivo(ruta)
        for linea in contenidolog:
            lineaaux = linea.replace('\r', '')
            contenido.append(lineaaux)
        return contenido

    @staticmethod
    def hazresumen(contenidolog, parametros, ruta):
        ''' Hace el resumen, método principal de este trabajo.

        Sirve para hacer el resumen del contenido del log, usa expresiones regulares
        para reconocer patrones, se pueden agregar nuevas palabras y buscar otros
        patrones

        :param contenidolog: El contenido del archivo .log o .out
        :param parametros: Parámetros ingresados en la linea de comandos
        :param ruta: La ruta del archivo procesado, sirve para agregarlo a la pantalla
        :return: El resumen obtenido para mostrarse en modo curses o en modo terminal

        '''
        cargamult = []
        r = 0
        i = 0
        varexportar = []
        resumen = []
        comin = ''
        for linea in contenidolog:
            if 'Gaussian(R)' in linea:
                r = NResumen.buscapalabra(' #', contenidolog)
                if r == -1:
                    return ['El archivo ' + ruta + ' no es un archivo de salida de Gaussian válido']
                else:
                    break
            i = i+1
        if i == len(contenidolog):
            return ['El archivo ' + ruta + ' no es un archivo de salida de Gaussian válido']

        resumen.append(ruta)
        varexportar.append([ruta])
        resumen.append('*********************************************************************')
        resumen.append('Analizador  Gaussian09')
        resumen.append('Ag09 v0.9')
        resumen.append('*********************************************************************')
        matriz = []
        r = NResumen.buscapalabra(' #', contenidolog)
        #if r == -1:
            #return ['El archivo ' + ruta + ' no es un archivo de salida de Gaussian válido']
        comin = contenidolog[r]
        datosini = NResumen.obtendatosiniciales(contenidolog, r)
        for elemento in datosini:
            resumen.append(' '.join(elemento.split()))

        resumen.append('')
        r = NResumen.buscapalabra('termination', contenidolog)
        if r == -1:
            resumen.append('')
        else:
            if 'Normal' in contenidolog[r]:
                resumen.append('Terminación normal')
            else:

                resumen = []
                resumen.append(ruta)
                resumen.append('Terminación Erronea')
                for i in range(len(contenidolog) - 1, 0, -1):
                    if '        ' in contenidolog[i]:
                        for j in range(i + 1, len(contenidolog) - 1, 1):
                            resumen.append(contenidolog[j])
                        break
                return resumen
            resumen.append('')
            if 'opt' in comin:
                resumen.append('*** DATOS DE CONVERGENCIA ***\n')
                r = NResumen.buscapalabra('converged\?', contenidolog)
                if r != -1:
                    datosconv = NResumen.obtendatosconvergencia(r, contenidolog)
                    for elemento in datosconv:
                        resumen.append(elemento.replace('\n',''))
                resumen.append('')
                numpasos = 0
                paso = 0
                # for k in range(len(contenidolog -1, 0, -1)):

                r = NResumen.buscapalabra('Stationary', contenidolog)
                if r != -1:
                    for i in range(r, 0, -1):
                        if 'Converged?' in contenidolog[i]:
                            paso = paso + 1
                    for i in range(0, len(contenidolog), 1):
                        if 'Converged?' in contenidolog[i]:
                            numpasos = numpasos + 1
                    resumen.append('Stationary point found en el paso ' + str(paso) + ' de ' + str(numpasos))
        r = NResumen.buscapalabra('natoms=', contenidolog)
        if r != -1:
            natomos = int(contenidolog[r].split()[1])
        else:
            n = NResumen.obtendatosaptmulliken(105, contenidolog)
            natomos = len(n)


        resumen.append(' ')
        resumen.append('Numero de átomos: ' + str(natomos))
        resumen.append(' ')
        r = NResumen.buscapalabra('multiplicity', contenidolog)
        if r == -1:
            resumen.append('')
        else:
            aux = contenidolog[r].split()
            cargamult.append('Carga: ' + aux[2] + ' Multiplicidad: ' + aux[5])
            resumen.append('Carga: ' + aux[2] + ' Multiplicidad: ' + aux[5])
            resumen.append(' ')
            varexportar.append(cargamult)

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
        if 'nmr=' in comin:
            NResumen.opcnics(resumen, contenidolog, ruta, varexportar)

        # A partir de aqui se mostrarán solo si la palabra se pasó como parámetro en la ejecucion del programa
        for elemento in parametros:
            if '--ALL' in parametros or '-a' in parametros:
                hf = NResumen.opchf(contenidolog)
                if hf:
                    resumen.append('Valor HF: ' + hf + ' Hartrees ')
                    resumen.append(' ')
                    varexportar.append(['Valor_HF: '+  hf])
                tq = NResumen.opctq(resumen, contenidolog, natomos)
                if tq:
                    resumen.append('Dipolo ' + tq)
                    resumen.append(' ')
                    varexportar.append(['Dipolo: '+ tq])

                NResumen.opcmulliken(resumen, contenidolog, varexportar)
                NResumen.opcapt(resumen, contenidolog, varexportar)
                NResumen.opcacm(resumen, contenidolog, natomos, varexportar)
                NResumen.opcasd(resumen, contenidolog, natomos, varexportar)
                NResumen.opchsd(resumen, contenidolog, natomos, varexportar)
                NResumen.opcnao(resumen,contenidolog,varexportar)
                NResumen.opcmep(resumen,contenidolog,varexportar)

                break

            if elemento == '-hf':
                hf = NResumen.opchf(contenidolog)
                if hf:
                    resumen.append('Valor HF: ' + hf + ' Hartrees ')
                    resumen.append(' ')
                    varexportar.append(hf)
            if elemento == '-tq':
                tq = NResumen.opctq(resumen, contenidolog, natomos)
                if tq:
                    resumen.append('Dipolo ' + tq)
                    resumen.append(' ')
                    varexportar.append(tq)
            if elemento == '-apt':
                NResumen.opcapt(resumen, contenidolog,varexportar)
            if elemento == '--mulliken' or elemento == '-m':
                NResumen.opcmulliken(resumen, contenidolog, varexportar)
            if elemento == '--atomic_charges_matrix' or elemento == '-acm':
                NResumen.opcacm(resumen, contenidolog, natomos, varexportar)
            if elemento == '--atomic_spin_densities' or elemento == '-asd':
                NResumen.opcasd(resumen, contenidolog, natomos, varexportar)
            if elemento == '--hirshfeld spin densities' or elemento == '-hsd':
                NResumen.opchsd(resumen, contenidolog, natomos, varexportar)
            if elemento == '-nao':
                NResumen.opcnao(resumen, contenidolog,varexportar)
            if elemento == '-mep':
                NResumen.opcmep(resumen, contenidolog, varexportar)

        mensaje = ''
        if '-e' in parametros and '-t' in parametros:
            rutacsv = raw_input('Escriba el nombre del archivo y la ruta: ')
            if rutacsv[len(rutacsv) - 1] is '/':
                mensaje = ' {0} no es un nombre de archivo válido'.format(rutacsv)
            else:
                c, mensaje = NResumen.exporta(varexportar,rutacsv)
        resumen.append(mensaje)
        return resumen

    @staticmethod
    def exporta(datosarchivo, ruta):
        ''' Exporta el resumen en formato csv.

        Exporta el resumen(o lo que tenga el parametro resumen) a un archivo .csv
        cuyo nombre sera igual al del log del que se genera

        :param datosarchivo: Los datos que se van a exportar al csv
        :param ruta: ruta del .log o .out, sirve para generar el nombre del archivo csv

        '''
        datos = []
        for dato in datosarchivo:
            for elemento in dato:
                datos.append(elemento)
        status, mensaje = DResumen.guardaarchivo(ruta, datos)
        print datos
        print datosarchivo
        return status, mensaje

    # Codigo redundante, optimizar !!!!!!!!!!!!!
    @staticmethod
    def buscapalabra(palabra, contenido):
        ''' Busca una palabra en el contenido del log.

        Busca los patrones en el contenido de los logs, regresa el número de la
        linea en donde encontró la coincidencia. La búsqueda se hace de manera inversa.

        :param palabra: la palabra a buscar
        :param contenido: El texto donde se va a buscar
        :return: pos: El número de linea donde se encontro la coincidencia, si no se
        encontro se regresa -1

        '''
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
        ''' Obtiene los datos contenidos en las primeras lineas del log.

        Sirve para obtener los primeros datos del log, entre ellos se encuentran
        la cantidad de memoria, el número de procesadores, el comando inicial, etc.

        :param contenido: el contenido del log
        :param posicioninicio: Desde cual linea se inicia a buscar los datos
        :return: datosi: Los datos iniciales que incluyen la cantidad de memoria utilizada,
        el número de procesadores, el comando inicial,etc

        '''
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
        ''' Obtiene  una lista con las frecuencias negativas

        Obtiene las frecuencias negativas, si es que las hay, sólo en caso de que el comando inicial contenga
        la palabra freq

        :param contenido: contenido del log
        :param posicioninicio: Numero de linea del log desde el cuál se va a empezar a buscar las
        frecuencias
        :return: fneg: Lista que contiene las frecuencias negativas, si no las hay esta es vacia

        '''
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
        ''' Obtiene los datos de convergencia.

        Obtiene los datos de convergencia del contenido del log solo en caso de que el
        comando inicial contenga la palabra opt

        :param lineainicio: Numero de linea del log desde el cuál se va a empezar a buscar los
        datos de convergencia
        :param contenido: contenido del log
        :return: datosconv: Datos de convergencia, nunca vacío

        '''
        datosconv = []
        for i in range(lineainicio, lineainicio + 5):
            datosconv.append(contenido[i])
        return datosconv

    # Modificar para que busque en al expresion regular 3 o mas flotantes y una letra al final

    @staticmethod
    def obtendatosaptmulliken(lineainicio, contenido):
        ''' Obtiene los vectores APT o de Mulliken

        Obtiene los vectores APT atomic charges, Mulliken atomic charges, etc.

        :param lineainicio: Linea desde la cual empezara a extraer los datos
        :param contenido: contenido del log
        :return: datos: El vector APT o Mulliken

        '''

        datos = []
        vaux = 0

        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+-?\d+.?\d+\s+[A-Z]?$')
        for i in range(lineainicio + 2, len(contenido) - 1, 1):
            if expreg.search(contenido[i]) is not None:
                cad = contenido[i].split()
                datos.append(cad[1:])
            else:
                break
        #datos.append(str(len(datos)))
        return datos

    @staticmethod
    def obtenmatriz(pos, contenido, na):
        ''' Obtiene la matriz Atomic Charges Matrix o Atomic spin densities

        Obtiene la matriz Atomic Charges Matrix o Atomic spin densities si es que existen
        para despues extraer de ellas la diagonal correspondiente

        :param pos: Linea de inicio desde la cual empezará a buscar en el log
        :param contenido: Contenido del log
        :param na: Número de átomos
        :return: matriz: Un arreglo en forma de matriz de na * na

        '''

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

        matrize = []
        ca = ''
        for linea in matriz:
            for columna in linea:
                ca = ca + str(columna) + '\t'
            matrize.append(ca)
            ca = ''


        return matriz

    @staticmethod
    def buscarlinea(palabra, contenido):
        ''' Método en deshuso

        :param palabra:
        :param contenido:
        :return:
        '''
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
    def opcnics(resumen, contenidolog, ruta, varexportar):
        ''' Opción NICS

        Calcula el valor de NICS(0) o NICS(1) si en el nombre del archivo dice NICS


        :param resumen: resumen generado hasta el punto en que fue llamada la funcion
        :param contenidolog: contenido del log
        :param ruta: ruta que contiene el nombre del archivo

        '''
        cadnics = ''
        nics = ''
        expreg = re.compile(r'nics', re.I)
        res = expreg.search(ruta)
        if res:
            r = NResumen.buscapalabra('isotropic', contenidolog)
            linea = contenidolog[r].split()
            resumen.append('**** VALOR NICS ****')
            resumen.append('')
            nics = '\tNICS= -' + linea[4]
            cadnics =linea[0] +'\t' + linea[1]+'\t'+'Isotropic= ' + linea[4]+nics
            resumen.append(cadnics)
            varexportar.append(['VALOR_NICS'])
            varexportar.append(['#_Átomo Átomo '])
            varexportar.append([cadnics])


    @staticmethod
    def opcacm(resumen, contenidolog, natomos,varexportar):
        ''' Opcion Atomic Charges Matrix.

        Se invoca este método en caso de que los argumentos de entrada sea -acm, agrega la
        diagonal de Atomic Charges Matrix al resumen si se encuentra.


        :param resumen: resumen generado hasta el punto que fue llamada la función
        :param contenidolog: Contenido del log
        :param natomos: numero de atomos, sirve para generar la matriz

        '''
        diagonal = ''
        r = NResumen.buscapalabra('Condensed to atoms', contenidolog)
        if r == -1 or 'Mulliken atomic charges:' in contenidolog[r + 1]:
            resumen.append('**** NO HAY DATOS DE ATOMIC CHARGES MATRIX ****')
            resumen.append(' ')
        else:
            listaatomos = NResumen.obtenlistaatomos(contenidolog)
            matriz = NResumen.obtenmatriz(r, contenidolog, natomos)
            resumen.append('***** VALORES DE LA DIAGONAL DE ATOMIC CHARGES MATRIX *****\n')
            for i in range(len(matriz)):
                diagonal = diagonal + str(matriz[i][i]) + ' '
                resumen.append(str(i+1) + ' ' + listaatomos[i] + '\t' + matriz[i][i])
            resumen.append(' ')
            d = []
            d = diagonal.split()
            varexportar.append(['VALORES_DE_LA_DIAGONAL_DE_ATOMIC_CHARGES_MATRIX'])
            j = 0
            for elemento in d:
                varexportar.append([listaatomos[j] +' '+ elemento])
                j = j + 1
        resumen.append(' ')

    @staticmethod
    def opchf(contenidolog):
        hf = ''
        r = NResumen.buscapalabra('HF=', contenidolog)
        if not r is -1:
            hf = ''
            index = contenidolog[r].index('HF=')
            i = index + 3
            lenren = len(contenidolog[r]) - 1
            while (True):
                if contenidolog[r][i] == '\\' or contenidolog[r][i] == '|':
                    break
                if contenidolog[r][i] is not ' ':
                    hf = hf + contenidolog[r][i]
                i = i + 1
                if i >= len(contenidolog[r]) - 1:
                    r = r + 1
                    i = 0

        return hf

    @staticmethod
    def opcasd(resumen, contenidolog, natomos,varexportar):
        ''' Opcion Atomic Charges Matrix.

        Se invoca este método en caso de que los argumentos de entrada sea -asd, agrega la
        diagonal de Atomic spin densities Matrix al resumen si se encuentra.

        :param resumen: resumen generado hasta el punto que fue llamada la función
        :param contenidolog: Contenido del log
        :param natomos: numero de atomos, sirve para generar la matriz

        '''

        r = NResumen.buscapalabra('Atomic-Atomic Spin Densities.', contenidolog)
        diagonal = ''
        if r == -1:
            resumen.append('**** NO HAY DATOS DE ATOMIC SPIN DENSITIES ****')
            resumen.append('')
        else:
            listaatomos = NResumen.obtenlistaatomos(contenidolog)
            matriz2 = NResumen.obtenmatriz(r, contenidolog, natomos)
            resumen.append(' ')
            diagonal = ''
            resumen.append('***** VALORES DE LA DIAGONAL DE ATOMIC-ATOMIC SPIN DENSITIES *****\n')
            for i in range(len(matriz2)):
                diagonal = diagonal + str(matriz2[i][i]) + ' '
                resumen.append(str(i+1) + ' ' + listaatomos[i] + '\t' + matriz2[i][i])
            d = []
            d = diagonal.split()
            varexportar.append(['VALORES_DE_LA_DIAGONAL_DE_ATOMIC_SPIN_DENSITIES'])
            j = 0
            for elemento in d:
                varexportar.append([listaatomos[j]+' '+elemento])
                j = j+1
            resumen.append(' ')


    @staticmethod
    def opchsd(resumen, contenidolog, natomos, varexportar ):
        ''' Opcion Hirshfeld spin densities.

        Obtiene los átomos, sus densidades de espin y sus cargas cuando en  los argumentos
        de entrada está -hsd

        :param resumen: resumen generado hasta el punto que fue llamada la función
        :param contenidolog: Contenido del log
        :param natomos: numero de atomos, sirve para generar la matriz


        '''
        hsd = []
        r = NResumen.buscapalabra('Hirshfeld spin densities, ', contenidolog)
        if r != -1:
            resumen.append(' ******* HIRSHFELD SPIN DENSITIES *******\n')
            resumen.append('Átomo\tSpin Densities\tCharges')
            resumen.append('')
            indice = 1
            for i in range(r + 2, r + natomos + 2, 1):
                resumen.append(str(indice) + ' ' + '\t'.join(contenidolog[i].split()[1:4]))
                hsd.append('\t'.join(contenidolog[i].split()[1:4]))
                indice = indice + 1
            varexportar.append(['Hirshfeld spin densities'])
            varexportar.append(['Átomo Spin_Densities Charges'])
            varexportar.append(hsd)
        else:
            resumen.append('**** NO HAY DATOS DE HIRSHFELD SPIN DENSITIES ****')

        resumen.append(' ')


    @staticmethod
    def opcapt(resumen, contenidolog, varexportar):
        ''' Opción APT.

        Obtiene los vectores APT atomic Charges y APT atomic charges with hydrogens summed
        cuando en los argumentos está -apt

        :param resumen: el resumen generado hasta el momento en que fue llamado el método
        :param contenidolog: contenido del log

        '''
        r = NResumen.buscapalabra('APT atomic charges:', contenidolog)
        aptch = []
        if r != -1:
            aptch = NResumen.obtendatosaptmulliken(r, contenidolog)
            r = NResumen.buscapalabra('APT Atomic charges with hydrogens summed', contenidolog)
            varexportar.append(['APT_Atomic_charges'])
            for elemento in aptch:
                varexportar.append([' '.join(elemento)])
            aths = []
            if r != -1:
                aths = NResumen.obtendatosaptmulliken(r, contenidolog)
                resumen.append('***Átomo\tAPT atomic charges \t APT atomic charges hydrogens summed ***\n')
                varexportar.append(['APT_Atomic_charges_with_hydrogens_summed'])
                for elemento in aths:
                    varexportar.append([' '.join(elemento)])
            for i in range(0,len(aptch),1):
                resumen.append(str(i + 1)+' '+'\t\t'.join(aptch[i]) + '\t\t\t' + str(aths[i][1]))
            resumen.append('')
        else:
            resumen.append(('**** NO HAY DATOS APT *****'))
            resumen.append('')


    @staticmethod
    def opcmulliken(resumen, contenidolog,varexportar):
        ''' Opción Mulliken.

        Obtiene los vectores Mulliken atomic charges, mulliken atomic spin densities y
        Mulliken atomic charges with hydrogens summed cuando en los argumentos esta -m
        y los agrega al resumen

        :param resumen: el resumen generado hasta el momento en que fue llamado el método
        :param contenidolog: contenido del log

        '''
        r = NResumen.buscapalabra('Mulliken atomic charges:', contenidolog)
        mac = []
        enc = 'Atom'
        if  r == -1:
            r = NResumen.buscapalabra('Mulliken charges:',contenidolog)
        if not r == -1:
            resumen.append('')
            resumen.append('**** MULLIKEN POPULATION ANALISIS *****')
            resumen.append('')
            mac = NResumen.obtendatosaptmulliken(r, contenidolog)
            varexportar.append(['Mulliken_Atomic_Charges'])
            for elemento in mac:
                varexportar.append([' '.join(elemento)])
            enc = enc + '\tAtomic charges'
            r = NResumen.buscapalabra('^ Mulliken atomic spin', contenidolog)
            mas = []
            if not r == -1:
                mas = NResumen.obtendatosaptmulliken(r, contenidolog)
                enc = enc + '\tAtomic spin densities'
                varexportar.append(['Mulliken_atomic_spin_densities'])
                for elemento in mas:
                    varexportar.append([' '.join(elemento)])
            r = NResumen.buscapalabra('^ Mulliken charges with', contenidolog)
            mchs = []
            if not r == -1:
                mchs = NResumen.obtendatosaptmulliken(r, contenidolog)
                enc = enc + '\tCharges with hidrogens summed'
                varexportar.append(['Mulliken_charges_with_hydrogens_summed'])
                for elemento in mchs:
                    varexportar.append([' '.join(elemento)])

            resumen.append(enc)




        else:
            resumen.append('**** NO HAY DATOS DE MULLIKEN ****')
        j = 0
        for i in range(0, len(mac), 1):
            aux = str(i + 1) + ' '
            try:
                aux = aux + '\t'.join(mac[i])
            except:
                pass
            try:
                aux = aux + '\t\t'.join(mas[i])[1:]
            except:
                pass
            if mac[i][0] is 'H':
                aux = aux + '\t\t' + '0.00000'
            else:
                try:
                    aux = aux + '\t\t'.join(mchs[j])[1:]
                    j = j + 1
                except:
                    pass
            resumen.append(aux)
        resumen.append('')

    @staticmethod
    def opctq(resumen, contenidolog, natomos):
        cad = ''
        r = NResumen.buscapalabra('Dipole=', contenidolog)
        if not r is -1:
            resumen.append('*** DATOS TERMOQUÍMICOS ***')
            resumen.append('')
            dp = ''
            index = contenidolog[r].index('Dipole=')
            i = index + 7
            while (True):
                if contenidolog[r][i] == '\\' or contenidolog[r][i] == '|':
                    break
                if contenidolog[r][i] is not ' ':
                    dp = dp + contenidolog[r][i]
                i = i + 1
                if i >= len(contenidolog[r]) - 1:
                    r = r + 1
                    i = 0
            ch = 'X'

            for elemento in dp.split(','):
                cad = cad + ch + '=' + elemento + ' '
                ch = chr(ord(ch) + 1)

            r = NResumen.buscapalabra('pressure', contenidolog)
            if r != -1:
                aux = contenidolog[r].split()
                resumen.append("Temperatura: " + aux[1] + ' ' + aux[2] + ' Presión: ' + aux[4] + ' ' + aux[5])
                resumen.append(' ')
            r = NResumen.buscapalabra('Zero-point correction', contenidolog)
            if r != -1:
                for i in range(r, len(contenidolog) - 1, 1):
                    if '(Thermal' in contenidolog[i]:
                        break
                    resumen.append(' '.join(contenidolog[i].split()))
                resumen.append('')
                resumen.append('\t\tE(Thermal)(Kcal/Mol)\tCV(Cal/Mol-Kelvin)\tS(Cal/Mol-Kelvin)')
                for j in range(i + 2, i + 100, 1):
                    aux = contenidolog[j].split()
                    if len(aux[0]) < 8:
                        aux[0] = aux[0] + '\t'
                    resumen.append(aux[0] + '\t\t' + '\t\t\t'.join(aux[1:]))
                    if 'Vibrational ' in contenidolog[j]:
                        break
        else:
            resumen.append('**** NO HAY DATOS TERMOQUÍMICOS ****')
        resumen.append('')

        return cad

    @staticmethod
    def opcnao(resumen,contenidolog,varexportar):
        '''

        :param resumen: el resumen generado hasta el momento en que fue llamado el método
        :param contenidolog: contenido del log
        :return:
        '''
        nao = []
        r = NResumen.buscapalabra('Natural populations:', contenidolog)
        if r != -1:
            resumen.append('**** NATURAL ATOMIC ORBITAL OCCUPANCIES ****')
            resumen.append('')
            resumen.append('\t'.join(contenidolog[r + 2].split()))
            resumen.append('')
            for i in range (r,len(contenidolog)-1,1):
                if args.Atomo in contenidolog[i].split():
                    nao.append(contenidolog[i])
                    resumen.append('\t'.join(contenidolog[i].split()))
                if 'Summary of Natural'in contenidolog[i]:
                    break
            if len(nao) > 0:
                nao.append('NATURAL_ATOMIC_ORBITAL_OCCUPANCIES')
                nao.append('NAO	Atom No	lang Type (AO) Occupancy Energy')
            else:
                resumen.append('**** NATURAL ATOMIC ORBITAL OCCUPANCIES ****')
                resumen.append('No hay datos para el átomo: '+ args.Atomo)
            varexportar.append(nao)
        else:
            resumen.append('**** No se encontraron datos NAO ****')

    @staticmethod
    def opcmep(resumen, contenidolog,varexportar):
        mep = []
        r = NResumen.buscapalabra('Electrostatic Properties', contenidolog)
        if r != -1:
            resumen.append('**** ELECTROSTATIC PROPERTIES ****')
            resumen.append('')
            contador = 0
            resumen.append('\tCenter\tElectric potential')
            resumen.append('')
            mep.append('ELECTROSTATIC_PROPERTIES')
            mep.append('\t Center Electric_potential')
            for i in range(r+6,len(contenidolog) -1, 1):
                if '------------------------' in contenidolog[i]:
                    break
                resumen.append('\t'.join(contenidolog[i].split()))
                mep.append(contenidolog[i])
        else:
            resumen.append('**** No se encontraron datos de Electrostatic Properties ****')
        varexportar.append(mep)

    @staticmethod
    def obtenlistaatomos(contenido):
        ''' Obtiene la lista de los átomos

        La lista obtenida sirve para agregar la primera columna en las diagonales

        :param lineainicio: Linea desde donde  empezara a obtener la lista
        :param contenido: contenido del log
        :return: listaatomos: La lista que contiene todos los átomos de la molécula
        '''

        listaatomos = []
        datos = []
        vaux = 0
        lineainicio = NResumen.buscapalabra('Mulliken atomic charges:', contenido)
        if lineainicio == -1:
            lineainicio = NResumen.buscapalabra('Condensed to atoms ', contenido)
            if lineainicio == -1:
                lineainicio = NResumen.buscapalabra('Atomic charges:', contenido)
        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+-?\d+.?\d+\s+[A-Z]?$')
        for i in range(lineainicio + 1, len(contenido) - 1):
            if expreg.search(contenido[i]) is not None and vaux < 2:
                cad = contenido[i].split()[1]
                listaatomos.append(cad)
                vaux = 1
            else:
                if vaux == 1:
                    break
                pass

        return listaatomos


class DResumen:
    ''' Clase de datos DResumen

        Se encarga de abrir el archivo .log o .out generado por Gaussian
        Tambien se encarga de escribir el csv

    '''

    @staticmethod
    def abrearchivo(ruta):
        ''' Abre el archivo indicado en la ruta.

        :param ruta: Ruta del archivo a abrir
        :return: regresa el texto contenido en el archivo

        '''
        contenido = []
        try:
            archivo = open(ruta)
            contenido = archivo.readlines()
            archivo.close()
        except IOError as e:
            contenido = []
            contenido.append('Error al abir el archivo {0} {1}'.format(ruta, e.strerror))
        return contenido

    @staticmethod
    def guardaarchivo(nombrearchivo, datos):
        ''' Guarda archivos

        Metodo para guardar archivos en formato csv

        :param ruta: Ruta donde se va a guardar el archivo
        :param datos: los datos que van a ir en el archivo
        :return: status: el estatus de la operación, si es 0 ocurrio un error si es 1 se realizó correctamente

        '''
        status = 1
        csvfile = nombrearchivo + '.csv'
        mensaje = 'AAA'
        try:
            with open(csvfile, 'w') as output:
                writer = csv.writer(output)
                for elemento in datos:

                    if elemento is not '' and elemento is not ' ':
                        writer.writerow(elemento.split())
            output.close()
            mensaje = 'Se guardó correctamente el archivo {0}'.format(csvfile)
        except IOError as e:
            mensaje = e.strerror + ' no se puede guardar el archivo en: {0}'.format(nombrearchivo)
            status = 0
        except:
            mensaje = 'Error desconocido al guardar {0}'.format(csvfile)
            status = 0
        return status, mensaje


class VResumenTer:
    ''' Clase VResumenTer

    Sirve para mostrar los datos directamente en la terminal

    '''

    def __init__(self, parametrosentrada, archivo):
        ''' Constructor para la clase VResumenTer

        :param parametrosentrada: lista con los parámetros ingresados en la terminal
        :param archivo: Ruta del archivo procesado
        '''
        mensaje = ''
        self.paramentrosresumen = parametrosentrada
        self.contenidoArchivo = NResumen.obtencontenidolog(archivo)
        try:
            if 'Error' in self.contenidoArchivo[0]:
                print self.contenidoArchivo[0]
                exit(0)
        except:
            pass
        self.resumen= NResumen.hazresumen(self.contenidoArchivo, self.paramentrosresumen, archivo)
        if not args.debug :
            for elemento in self.resumen:
                print elemento






