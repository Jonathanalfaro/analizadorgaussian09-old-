# analizadorgaussian
Analizador  de datos de salida del programa Gaussian09 hecho en python y con la libreria curses

## Ayuda de descarga

Para el uso local del programa necesita descargar el programa.

1. En la página de Github de clic en la opción 'Clone or download'
![Imagen 2](Img/i1.jpg)

2. Despues de clic en la opción  'Download ZIP'
![Imagen 2](Img/i2.jpg)

3. Extraiga el contenido del archivo

## Ayuda de uso
1. Puede ejecutar el programa directamente desde la cuenta Aess(También puedes continuar desde el punto 2)

    `Ag09principal.py [opciones] [ruta]`
    
    ***Para esto ya no es necesario descargar nada
    Ejemplo:
    
    ![Imagen_4](Img/i4.jpg)  
      
        
2. En una terminal cambie el directorio de trabajo a la ubicación donde extrajo el contenido del archivo descargado

3. Ejecute el programa de la siguiente manera

`python Resumen/Ag09principal.py [opciones] [ruta del log]`

Ejemplo:

`python Resumen/Ag09principal.py -a /home/lsvp/Documentos/SERVICIO_SOCIAL/BzPhsolo.out
`

El programa cuenta con una ayuda a la que puede accederse con el atajo -h

`python /home/lsvp/PycharmProjects/ag09/Resumen/Principal.py -h`

Lo cual da como salida lo siguiente

![Imagen 3](Img/i3.jpg)




Lista de opciones


| Opción | Acción |
| - | - |
| -a | Muestra toda la informacion que se puede extraer del archivo .log|
| -m | Muestra la informacion de APT atomic charges y APT atomic charges whit hydrogens summed |
| -acm | Muestra Atomic Charges Matrix y los valores de su diagonal|
| -hsd | Muestra Hirshfeld Spin Densities | 
| -asd | Muestra Atomic Spin Densities Matrix y su diagonal| 
| -apt | Muestra APT atomic charges| 
| -t | Muestra el resumen en la salida estándar|
| -e | Exporta los datos a una hoja de cálculo de Excel | 