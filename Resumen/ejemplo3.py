# -*- coding: utf-8 -*-
from Ag09principal import *

archivos = sys.argv[1:]

if len(archivos) != 3:
    print 'Error, se necesitan exactamente 3 archivos e intentaste usar {0}'.format(len(archivos))
    exit(0)
else:
    listacontenidos = [None]*3
    print 'Hay {0} archivos'.format(len(archivos))
for archivo in archivos:
    if '-1' in archivo:
        listacontenidos[0] = NResumen.obtencontenidolog(archivo)
    elif '+1' in archivo:
        listacontenidos[2] = NResumen.obtencontenidolog(archivo)
    else:
        listacontenidos[1] = NResumen.obtencontenidolog(archivo)
    print archivo

if listacontenidos[0] is None:
    print 'No se encontró el archivo N-1'
    exit(0)
if listacontenidos[1] is None:
    print 'No se encontró el archivo N'
    exit(0)
if listacontenidos[0] is None:
    print 'No se encontró el archivo N+1'
    exit(0)
listahf = []

for contenido in listacontenidos:
    listahf.append(NResumen.opchf('', contenido))


try:
    I = float(listahf[1]) - float(listahf[0])
    A = float(listahf[1]) - float(listahf[2])
except:
    'Error al procesar el valor HF'
    exit(0)
N = (I - A) / 2
S = 1 / N

print 'Valor I = {0}'.format(I)
print 'Valor A = {0}'.format(A)
print 'Blandura = {0}'.format(N)
print 'Dureza = {0}'.format(S)
