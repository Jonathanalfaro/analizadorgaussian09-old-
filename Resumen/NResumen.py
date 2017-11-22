import re
from DResumen import DResumen

class NResumen:

    @staticmethod
    def obtenContenidoLog(ruta):
        contenido = []
        contenidoLog =  DResumen.abreArchivo(ruta)
        for linea in contenidoLog:
            l = linea.replace('\r','')
            contenido.append(l)
        return contenido


    @staticmethod
    def hazResumen(contenidoLog):
        resumen = []
        palabras = ['normal','multiplicity','freq','pressure', 'imaginary fre']
        for palabra in palabras:
            r = NResumen.buscaPalabra(palabra,contenidoLog)
            if r == -1:
                resumen.append('Error')
            else:
                resumen.append(contenidoLog[r])
        return resumen


    @staticmethod
    def buscaPalabra(palabra, contenido):
        nl= 0
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:
            res = expreg.search(linea)
            if res == None:
                pass
            else:
                return nl
            nl = nl + 1
        return -1