# analizadorgaussian
Programa hecho en Python para el análisis de datos de salida del programa Gaussian09

## Ayuda de descarga
Para uso local del programa primero necesita descargarlo a su computadora.

1. En la página de Github de clic en la opción 'Clone or download'

    ![Imagen 2](Img/i1.jpg)

2. Despues de clic en la opción  'Download ZIP'
    
    ![Imagen 2](Img/i2.jpg)

3. Extraiga el contenido del archivo

## Ayuda de uso

1. En una terminal cambie el directorio de trabajo a la ubicación donde extrajo el contenido del archivo descargado

2. Ejecute el programa de la siguiente manera

    ```
        python Resumen/Ag09principal.py [opciones] [ruta del log]
    ```
    Ejemplo:

    ```
        python Resumen/Ag09principal.py -a /home/USUARIO/Documentos/SERVICIO_SOCIAL/BzPhsolo.out
    ```

3. Se puede analizar un archivo o muchos a la vez

    ```
        python Resumen/Ag09Principal.py -a /home/lsvp/Documentos/ARCHIVO.out
    ```
    o
    ```
        python Resumen/Ag09Principal.py -a /home/lsvp/Documentos/*.out
    ```
    
## Ayuda en el programa

El programa cuenta con una ayuda a la que puede accederse con el atajo -h

``` 
    python /home/lsvp/PycharmProjects/ag09/Resumen/Principal.py -h
```

Lo cual da como salida lo siguiente



![Imagen 3](Img/i3.jpg)

## Lista de opciones

| Opción corta | Opción larga | Acción |
| - | - | - |
| -h | --help | muestra la ayuda de uso y parámetros |
| -hf | --hirshfeld | Muestra el valor de la energía de Hirshfeld |
| -m | --mulliken | Muestra las cargas atómicas de Mulliken |
| -apt | --APT_atomic | Muestra atomic polar tensor charges (APT)|
| -tq | --thermochemical | Muestra los datos termoquímicos como dipolo, temperatura, presión, etc |
| -acm | --atomic_charges_matrix | Muestra la diagonal de la matriz de cargas atomicas |
| -asd | --atomic_spin_densities | Muestra la diagonal de matriz de densidades atómicas |
| -hsd | --hirshfeld_spin_densities | Muestra las densidades de spin y las cargas de la matriz de Hirshfeld |
| -nao [Átomo]|| Muestra Natural atomic orbital occupancies| 
| -mep | | Muestra molecular electrostatic potential |
| -a | --ALL | Muestra todos los datos posibles | 
| -e | --exporta | Exporta los datos a un archivo separado por comas (CSV) |
| -t | --texto | Muestra los datos solicitados en directamente en la terminal |