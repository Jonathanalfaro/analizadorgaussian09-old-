#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from DResumen import DResumen

class NResumen:

    @staticmethod
    def obtencontenidolog(ruta):
        contenido = []
        contenidoLog =  DResumen.abreArchivo(ruta)
        for linea in contenidoLog:
            l = linea.replace('\r','')
            contenido.append(l)

        return contenido


    @staticmethod
    def hazresumen(contenidoLog,parametros):
        caux = ''
        r = 0
        r = NResumen.buscaPalabra('natoms=',contenidoLog)
        if r != -1:
            natomos = int(contenidoLog[r].split()[1])
        else:
            n = NResumen.obtenDatosMulliken(105,contenidoLog)
            natomos = len(n)
        resumen = []
        matriz = []
        r = NResumen.buscaPalabra(' #',contenidoLog)
        resumen.append('Comando inicial: ' + contenidoLog[r])
        resumen.append('')
        r = NResumen.buscaPalabra('termination',contenidoLog)
        if r == -1:
            resumen.append('Error, no se encontraron datos de la terminación')
        else:
            if 'Normal' in contenidoLog[r]:
                resumen.append('Terminación normal')
            else:
                resumen.append(('Terminación erronea'))
        resumen.append(' ')
        resumen.append('Numero de átomos: ' + str(natomos))
        resumen.append(' ')
        r = NResumen.buscaPalabra('multiplicity',contenidoLog)
        if r ==-1:
            resumen.append('Error, no hay datos de carga y multiplicidad en el archivo')
        else:
            aux = contenidoLog[r].split()
            resumen.append('Carga: '+ aux[2] + ' Multiplicidad: ' + aux[5])
            resumen.append(' ')
        r = NResumen.buscaPalabra('HF=',contenidoLog)
        if r ==-1:
            resumen.append('Error, no hay datos HF')
        else:
            hf = ''
            index = contenidoLog[r].index('HF=')
            for i in range(index,len(contenidoLog[r])):
                if (contenidoLog[r][i]) == ('\\'):
                    break
                hf = hf + contenidoLog[r][i]

            resumen.append('Valor ' + hf)
            resumen.append(' ')

        r = NResumen.buscaPalabra('pressure',contenidoLog)
        if r == -1:
            resumen.append('Error, No se encontraron resultados para temperatura y presión')
        else:
            aux = contenidoLog[r].split()
            resumen.append("Temperatura: " + aux[1] +' '+ aux[2] + ' Presión: ' + aux[4] + ' ' + aux[5] )
            resumen.append(' ')
        r = NResumen.buscaPalabra('imaginary frequencies \(',contenidoLog)
        if r == -1:
            resumen.append('No hay frecuencias negativas')
            resumen.append(' ')
        else:
            fneg = NResumen.obtenFrequenciasNegativas(contenidoLog,r)
            resumen.append('Hay ' + str(len(fneg)) + ' frecuencias negativas')
            for elemento in fneg:
                resumen.append(elemento)
            resumen.append(' ')


        #A partir de aqui se mostrarán solo si la palabra se pasó como parámetro en la ejecucion del programa
        for elemento in parametros:
            if elemento =='--APT atomic charges':
                r = NResumen.buscaPalabra('APT atomic charges:',contenidoLog)
                aptch = []
                if r == -1:
                    resumen.append('Error, no se encontraron datos')
                else:
                    aptch = NResumen.obtenDatosMulliken(r,contenidoLog)
                r = NResumen.buscaPalabra('APT Atomic charges with hydrogens summed',contenidoLog)
                aths = []
                if r == -1:
                    resumen.append('Error, no se encontraron datos')
                    resumen.append(' ')
                else:
                    aths = NResumen.obtenDatosMulliken(r,contenidoLog)
                    resumen.append('APT atomic charges \t APT atomic charges hydrogens summed')
                for i in range (len(aptch)):
                    resumen.append(str(float(aptch[i])) + '\t\t\t' + str(aths[i]))
                resumen.append(' ')
            r = NResumen.buscaPalabra('Condensed to atoms',contenidoLog)
            if r == -1:
                resumen.append('No hay datos de la matriz')
            else:
                matriz = NResumen.obtenMatriz(r,contenidoLog,natomos)
                resumen.append('Atomic Charges Matrix\n\n')
                resumen.append(' ')
                for linea in matriz:
                    caux = ''
                    for elemento in linea:
                        caux += str(elemento) +'\t'
                    resumen.append(caux)
            resumen.append(' ')
            r = NResumen.buscaPalabra('Atomic-Atomic Spin Densities.',contenidoLog)
            diagonal = ''
            resumen.append('Valores de la diagonal: ')
            for i in range(len(matriz)):
                diagonal = diagonal + str(matriz[i][i]) + ' '

                resumen.append(matriz[i][i])
            resumen.append(' ')
            if r == -1:
                resumen.append('No hay datos de la matriz')
            else:
                matriz2 = NResumen.obtenMatriz(r,contenidoLog,natomos)
                resumen.append('Atomic Spin Densities Matrix\n\n')
                resumen.append(' ')
                for linea in matriz2:
                    caux = ''
                    for elemento in linea:
                        caux += str(elemento) + '\t'
                    resumen.append(caux)
                resumen.append(' ')
                diagonal = ''
                resumen.append('Valores de la diagonal: ')
                for i in range(len(matriz2)):
                    diagonal = diagonal + str(matriz2[i][i]) + ' '

                    resumen.append(matriz2[i][i])

                resumen.append(' ')
            r = NResumen.buscaPalabra('Hirshfeld spin densities, ',contenidoLog)
            if r == -1:
                resumen.append('No hay datos de la matriz Hirshfeld spin densities')
            else:
                matriz = NResumen.obtenMatriz(r,contenidoLog,natomos)
                resumen.append(' Hirshfeld spin densities, charges and dipoles using IRadAn= 4:\n\n')
                resumen.append(' ')
                for linea in matriz:
                    caux = ''
                    for elemento in linea[0:2]:
                        caux += str(elemento) +'\t'
                    resumen.append(caux)

        return resumen



    @staticmethod
    def buscaPalabraold(palabra, contenido):
        nl= 0
        pos = -1
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:
            res = expreg.search(linea)
            if res == None:
                pass
            else:
                pos = nl
                if (palabra == ' #'):
                    break
            nl = nl + 1
        return pos

    @staticmethod
    def buscaPalabra(palabra, contenido):
        pos = -1
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for i in range(len(contenido) - 1,0,-1):
            res = expreg.search(contenido[i])
            if res == None:
                pass
            else:
                pos = i
                break
        return pos

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
    #Modificar para que busque en al expresion regular 3 o mas flotantes y una letra al final
    @staticmethod
    def obtenDatosMulliken(lineainicio,contenido):
        datos = []
        vaux = 0
        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+-?\d+.?\d+\s+')
        for i in range(lineainicio + 1, len(contenido) - 1):
            if expreg.search(contenido[i]) != None and vaux < 2:
                cad = contenido[i].split()
                datos.append(cad[len(cad)-1] + '\n')
                vaux = 1
            else:
                if vaux == 1:
                    break
                pass
        return datos

    @staticmethod
    def obtenMatriz(pos, contenido,na):
        matriz = []
        for i in range(na):
            matriz.append([0] * na)
        ultimapos = 0
        c = 0
        natomos = 0
        ind = 0
        expreg = re.compile(r'\s+\d+\s+[a-zA-Z]+\s+(-?\d+\.?\d+\s{0,})+$')
        for linea in contenido[pos+2:]:
            if expreg.search(linea) != None:
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
    def buscarLinea(palabra,contenido):
        nl = 0
        posiciones = []
        expreg = re.compile(r'(%s)+' % palabra, re.I)
        for linea in contenido:
            res = expreg.search(linea)
            if res == None:
                pass
            else:
                posiciones.append(nl)
            nl = nl + 1
        return posiciones

