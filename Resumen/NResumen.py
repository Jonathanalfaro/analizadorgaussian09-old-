#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        r = NResumen.buscaPalabra(' #',contenidoLog)
        resumen.append('Comando inicial: ' + contenidoLog[r])
        r = NResumen.buscaPalabra('termination',contenidoLog)
        if r == -1:
            resumen.append('Error, no se encontraron datos de la terminación')
        else:
            if 'Normal' in contenidoLog[r]:
                resumen.append('Terminación normal')
            else:
                resumen.append(('Terminación erronea'))

        r = NResumen.buscaPalabra('multiplicity',contenidoLog)
        if r ==-1:
            resumen.append('Error, no hay datos de carga y multiplicidad en el archivo')
        else:
            aux = contenidoLog[r].split()
            resumen.append('Carga: '+ aux[2] + ' Multiplicidad: ' + aux[5])

        r = NResumen.buscaPalabra('pressure',contenidoLog)
        if r == -1:
            resumen.append('Error, No se encontraron resultados para temperatura y presión')
        else:
            aux = contenidoLog[r].split()
            resumen.append("Temperatura: " + aux[1] +' '+ aux[2] + ' Presión: ' + aux[4] + ' ' + aux[5] )
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
