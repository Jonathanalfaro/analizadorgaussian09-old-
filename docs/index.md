
## Gaussian09

Gaussian es un programa que proporciona capacidades avanzadas para el modelado de estructuras electrónicas.


## Ag09 (Analizador de datos de salida para Gaussian09)

### ¿Qué es?

Programa hecho en Python para el análisis de datos de salida del programa Gaussian09


### ¿Qué hace?

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


<a href="https://asciinema.org/a/14"><img src="https://asciinema.org/a/14.png" width="836"/></a>
