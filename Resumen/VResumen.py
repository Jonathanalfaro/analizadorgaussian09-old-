import curses

from NResumen import NResumen

class VResumen:

    def __init__(self, ruta):
        self.ruta1 = ruta
        self.contenidoPad1 = NResumen.obtenContenidoLog(self.ruta1)
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
        self.tamypad1 = len(self.contenidoPad1)
        self.pad1 = curses.newpad(self.tamypad1 + 1, 1000)
        self.pad2 = curses.newpad(self.tamypad1 + 1, 1000)
        self.contenidoPad2 = NResumen.hazResumen(self.contenidoPad1)
        self.ponDatosPad(self.contenidoPad1, self.contenidoPad2)
        self.barraAyuda = "Presiona 'q' para salir | Presiona b para buscar"
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)



    def ponDatosPad(self, contenido1, contenido2):
        y = 0
        for linea in contenido1:
            self.pad1.addstr(y, 1, linea)
            y = y + 1
        y = 0
        for linea in contenido2:
            self.pad2.addstr(y, 1, linea)
            y = y + 1




    def muestraVentana(self, stdscr):
        k = 1
        stdscr.timeout(10)
        stdscr.keypad(True)
        while k != ord('q'):

            maxy, maxx = stdscr.getmaxyx()

            self.pad1xf = int(maxx - 1)
            self.pad1yf = maxy // 2 - 1
            self.pad2yi = maxy // 2 + 1
            self.pad2xf = maxx - 1
            self.pad2yf = maxy - 2

            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(1, 0, self.ruta1)
            stdscr.addstr(1, len(self.ruta1), " " * (self.pad1xf - len(self.ruta1)))
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(maxy-1,0,self.barraAyuda)
            stdscr.addstr(self.pad2yf + 1, len(self.barraAyuda), " " * (self.pad2xf - len(self.barraAyuda)))
            stdscr.attroff(curses.color_pair(1))


            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(self.pad1yf + 1, 0, self.ruta1)
            stdscr.addstr(self.pad1yf + 1, len(self.ruta1), " " * (maxx - len(self.ruta1) - 1))
            stdscr.attroff(curses.color_pair(2))



            if k == ord('1'):
                self.posycursor = self.pad1yi
                self.posxcursor = self.pad1xi
                self.padactivo = 1


            if k == ord('2'):
                self.posycursor = self.pad2yi
                self.posxcursor = self.pad2xi
                self.padactivo = 2


            if k == curses.KEY_DOWN:
                self.posycursor = self.posycursor + 1

            if k == curses.KEY_UP:
                self.posycursor = self.posycursor - 1

            if k == curses.KEY_LEFT:
                self.posxcursor = self.posxcursor - 1
                if self.posxcursor <= 0:
                    self.posxpad1 = self.posxpad1 - 1
                    self.posxpad2 = self.posxpad1 - 1

            if k == curses.KEY_RIGHT:
                self.posxcursor = self.posxcursor + 1
                if self.posxcursor >= maxx - 1:
                    self.posxpad1 = self.posxpad1 + 1
                    self.posxpad2 = self.posxpad2 + 1

            if self.padactivo == 1:
                self.posycursor = max(self.pad1yi, self.posycursor)
                self.posycursor = min(self.pad1yf, self.posycursor)
                if self.posycursor > self.pad1yf - 1 and k != -1:
                    self.posypad1 = min(self.posypad1 + 1, self.tamypad1)
                if self.posycursor <= self.pad1yi + 1 and k != -1:
                    self.posypad1 = max(0, self.posypad1 - 1)
            else:
                self.posycursor = max(self.pad2yi, self.posycursor)
                self.posycursor = min(self.pad2yf, self.posycursor)
                if self.posycursor > self.pad2yf - 1 and k != -1:
                    self.posypad2 = min(self.posypad2 + 1, self.tamypad2)
                if self.posycursor <= self.pad2yi + 1 and k != -1:
                    self.posypad2 = max(0, self.posypad2 - 1)



            self.posxcursor = max(0,self.posxcursor)
            self.posxcursor = min(maxx - 1, self.posxcursor)
            stdscr.move(self.posycursor, self.posxcursor)


            self.pad1.refresh(self.posypad1, self.posxpad1, self.pad1yi, self.pad1xi, self.pad1yf, self.pad1xf)
            self.pad2.refresh(self.posypad2, self.posxpad2, self.pad2yi, self.pad2xi, self.pad2yf, self.pad1xf)

            k = stdscr.getch()