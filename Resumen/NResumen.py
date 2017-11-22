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
        r = 0
        resumen = []
        palabras = ['normal','multiplicity','freq','pressure']
        for palabra in palabras:
            r = NResumen.buscaPalabra(palabra,contenidoLog)
            if r == -1:
                resumen.append('Error')
            else:
                resumen.append(contenidoLog[r])
        r = NResumen.buscaPalabra('imaginary frequencies',contenidoLog)
        if r == -1:
            resumen.append('No hay frecuencias negativas')
        else:
            fneg = NResumen.obtenFrequenciasNegativas(contenidoLog,r)
            for elemento in fneg:
                resumen.append(elemento)
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

    @staticmethod
    def obtenFrequenciasNegativas(contenido,posicioninicio):
        fneg = []
        expreg = re.compile(r'(Frequencies){1}\s+(-){2}\s+-?')
        for i in range(posicioninicio,posicioninicio+100):
            linea = contenido[posicioninicio]
            fneg.append(str(i))
            if expreg.search(linea) != None:
                fneg.append(linea)
                aux = linea.split()
                for elemento in linea:
                    try:
                        f = float(elemento)
                        f.append(f)
                        if f < 0.0:
                            fneg.append(f)
                        else:
                            return fneg
                    except:
                        pass
            else:
                pass
            return fneg
