## Uso básico

Despues de descargar y extraer el programa abra una terminal y cambie al directorio donde extrajo el contenido.  
El uso del programa es de la siguiente forma:

` $ python Ag09principal.py [opciones] [archivos] `  

## Opciones  

Se puede acceder a una lista de opciones que soporta el programa de la siguiente manera:  

` $ python Ag09principal.py -h `  

## Procesar todas las opciones

Se pueden procesar todas las opciones al mismo tiempo con la opcion corta -a o la opcion larga --ALL

` $ python Ag09principal.py -a salida.log `  

o  

` $ python Ag09principal.py -ALL salida.log `  


## Opciones -m, -apt, -hf, -tc, hsd, acm, mep

Estas opciones no requieren un parámetro adicional y pueden ser usadas de la siguiente manera:

* ` $ python Ag09principal.py -m salida.log `
* ` $ python Ag09principal.py -apt salida.log `
* ` $ python Ag09principal.py -hf salida.log `
* ` $ python Ag09principal.py -tc salida.log `
* ` $ python Ag09principal.py -hsd salida.log `
* ` $ python Ag09principal.py -acm salida.log `
* ` $ python Ag09principal.py -mep salida.log `

Tambien pueden combinarce entre ellas

## Opción NAO

La opción NAO admite el paso de un parámetro adicional, este parametro es el símbolo químico del átomo al cual se le va a hacer
el análisis, ejemplo:  

` $ python Ag09principal.py -nao H salida.log `  

El comando anterior procesara el archivo ` salida.log ` filtrando el resultado para el átomo de hidrógeno (H).

## Opción exportar -e

Si se especifica la opcion ` -e ` se guardarán los datos de las opciones especificadas a un archivo separado por comas CSV
Por ejemplo con el siguiente comando:  

` $ python Ag09principal.py -a -e salida.log `  

Se pedirá escriba la ruta o el nombre de un archivo y se guardarán al archivo CSV todas las opciones que se hayan encontrado en el archivo  `salida.log`

  ![Imagen 5](Img/i5.jpg)  

##### Nota  

Se debe dar una ruta existente y tener permisos de escritura en este directorio, de lo contrario se dará un error  


## Opción -t

Muestra el resultado del análisis directamente en la terminal, es un modo no interactivo salvo si se especifica la opcion `-e`
en cuyo caso se pedirá la ruta o nombre del archivo a exportar.
Si no se especifica esta opción los resultados se mostrarán en un modo interactivo.

Ejemplo con la opcion -t

<script src="https://asciinema.org/a/A7mAanC41YN9tEZhxQq3eoiWr.js" id="asciicast-A7mAanC41YN9tEZhxQq3eoiWr" async></script>

Ejemplo sin la opcion -t  

<script src="https://asciinema.org/a/MLW34JFR7aP9U9brs3fdiv2CR.js" id="asciicast-MLW34JFR7aP9U9brs3fdiv2CR" async></script>






