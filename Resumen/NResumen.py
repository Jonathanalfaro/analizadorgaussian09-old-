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
        for i in range(posicioninicio+1,posicioninicio+100):
            linea = contenido[i]
            if expreg.search(linea) != None:
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
