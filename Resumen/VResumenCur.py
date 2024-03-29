import curses

from NResumen import NResumen


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
