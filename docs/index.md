
# Gaussian09

Gaussian es un programa que proporciona capacidades avanzadas para el modelado de estructuras electrónicas.


# Ag09 (Analizador de datos de salida para Gaussian09)

## ¿Qué es?

Es un programa que fue parte de mi proyecto de servicio social, realizado en colaboración entre el laboratorio de supercómputo y el área de fisicoquímica teórica de la Universidad Autónoma Metropolitana Unidad Iztapalapa.
Fue programado en Python y sirve para  el análisis de datos de salida del programa Gaussian09


## ¿Qué hace?

Es capaz de extraer información útil para el usario, filtrando el contenido de los archivos de salida de Gaussian09.
También puede guardar los resultados del análisis en un archivo CSV (comma separated values) para facilitar 
la manipulación de los datos en programas como EXCEL, Libreoffice Calc, etcetera.  

Puede procesar uno o tres archivos. Si se desean procesar 3 archivos el programa los organizará
de acuerdo a su carga, entonces los archivos serán procesados y los resultados organizados de la siguiente
manera:

* El archivo con carga +1 será **salidaN-1.log**
* El archivo con carga 0 será **salida.log**
* El archivo con carga -1 será **salidaN+1.log**

En cualquiera de los casos si se pide una opción que no está presente en el archivo de salida
se mostrará la advertencia de que este dato no existe en el archivo. 

Los datos que se pueden extraer son:

* Cargas atómicas de Mulliken
* Cargas de tensor polar atómico (APT)
* Energia de Hirshfeld
* Datos termoquímicos
* Diagonal de la matriz de cargas atómicas
* Diagonal de la matriz de densidades atómicas
* Densidades de spin de Hirshfeld
* Ocupaciones orbitales atómicas naturales (NAO)
* Potencial electrostático Molecular (MEP)

# Lista de opciones

#### Opción -hf (Hirshfeld)

Muestra el valor de la energía de Hirshfeld con unidades Hartrees

#### Opción -m (Mulliken)

Muestra el análisis poblacional de Mulliken, es decir, Mulliken atomic charges, mulliken atomic charges with hydrogens summed
y Mulliken atomic spin densities

#### Opción -apt (Atomic polar tensor)

Muestra el analisis poblacional APT, es decir, APT atomic charges y APT atomic charges with hydrogens summed

#### Opción -tc  (thermochemical)

Muestra los datos termoquímicos como dipolo, temperatura, presión

#### Opción -acm (Atomic charges matrix)

Muestra la diagonal de la matriz de cargas atómicas

#### Opción -asd (Atomic spin densities matrix)

Muestra la diagonal de la matriz de densidades atómicas

#### Opción -hsd (Hirshfeld spin densities)

Muestra las densidades de spin y las cargas de la matriz de Hirshfeld

#### Opción -nao [Átomo] (Natural atomic orbital occupancies)

Muestra Natural atomic orbital occupancies, si no se escribe el parámetro `[Átomo]` se toma por defecto el valor N (Nitrógeno)

#### Opción -mep (Molecular electrostatic potential)

Muestra molecular electrostatic potential

#### Opción -a (ALL)

Muestra todos los datos posibles utilizando todas las opciones anteriores
