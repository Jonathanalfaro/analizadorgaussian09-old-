import re
from DLector import DLector


class NLector:


    @staticmethod
    def __obtenDatos__(rutas):
        contenido = DLector.__abreArchivos__(rutas)
        return contenido

    @staticmethod
    def buscar(palabra, contenido):
        c = 0
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:

            res = expreg.search(linea)
            if res == None:
                pass
            else:
                return c
            c = c + 1
        return 0

    @staticmethod
    def extraeDatos(palabra,lineainicio,contenido):
        datos = []
        vaux = 0
        expreg1 = re.compile(r'(%s)+\s?' % palabra, re.I)
        if expreg1.search("Mulliken ") != None:
            expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+-?\d+.\d+')
            for i in range(lineainicio+1,len(contenido)-1):
                if expreg.search(contenido[i]) != None and vaux < 2:
                    cad = NLector.formateaCadena(contenido[i])
                    datos.append(cad+'\n')
                    vaux = 1
                    nombreArchivo = 'Mulliken'
                else:
                    if vaux == 1:
                        break
                    pass
        elif( expreg1.search("Otra cosa")) != None:
            expreg = re.compile(r'La otra cosa',re.I)
            nombreArchivo = 'La otra cosa'
        #DLector.__guardaArchivos__('/home/jonathan/', nombreArchivo, datos)


    @staticmethod
    def formateaCadena(linea):
        espacio = '\b'
        l = linea.split()
        cad = espacio.join(l)
        return cad