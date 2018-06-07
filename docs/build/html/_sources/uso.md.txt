
# Uso

El programa permite el paso de parámetros para indicarle que secciones de la salida de **Gaussian** quieres extraer.  

El siguiente texto tiene como objetivo brindarte ayuda de como se utiliza el programa, la información está acompañada por un video en el que se explica detalladamente como utilizar cada una de las opciones y puedes seleccionar los comandos del video y pegarlos en tu sesión de terminal para probar su funcionamiento.  

Recuerda que puedes pausar el video en cualquier momento y seleccionar los comandos de ejemplo. También puedes descargar el archivo de prueba para seguir exactamente el funcionamiento explicado.

## Uso básico

Despues de descargar y extraer el programa abra una terminal y cambie al directorio donde extrajo el contenido.  
El uso del programa es de la siguiente forma:

` $ python Ag09principal.py [opciones] [archivos] `  

Se puede acceder a una lista de opciones que soporta el programa de la siguiente manera:  

<script src="https://asciinema.org/a/1xLsTi5X4O7pHukn4TqQYAZJ8.js" id="asciicast-1xLsTi5X4O7pHukn4TqQYAZJ8" async></script>

## Opciones -m, -apt, -hf, -tc, hsd, acm, mep


Estas opciones no requieren un parámetro adicional y pueden ser combinadas entre ellas


<script src="https://asciinema.org/a/IyELYw8hcxTMW8L9BnqWuBjA7.js" id="asciicast-IyELYw8hcxTMW8L9BnqWuBjA7" async></script>


## Opción NAO


La opción NAO admite el paso de un parámetro adicional, este parametro es el símbolo químico del átomo al cual se le va a hacer
el análisis, ejemplo:  

` $ python Ag09principal.py -nao H salida.log `  

El comando anterior procesara el archivo ` salida.log ` filtrando el resultado para el átomo de hidrógeno (H).

## Opción exportar -e


Si se especifica la opcion ` -e ` se guardarán los datos de las opciones especificadas a un archivo separado por comas CSV, y se pedirá que escriba la ruta o el nombre de un archivo donde se guardarán los datos obtenidos segun las opciones que se hayan especificado.

<script src="https://asciinema.org/a/928rzEI7VoqBDj0JEgxAt1tQP.js" id="asciicast-928rzEI7VoqBDj0JEgxAt1tQP" async></script>

### Nota  


## Procesar todas las opciones


Se pueden procesar todas las opciones al mismo tiempo con la opcion corta -a o la opcion larga --ALL

<script src="https://asciinema.org/a/XqYBLYVsG2RDCgik97aTt4cQp.js" id="asciicast-XqYBLYVsG2RDCgik97aTt4cQp" async></script>  

Se debe dar una ruta existente y tener permisos de escritura en este directorio, de lo contrario se dará un error  


## Opción -t


Muestra el resultado del análisis directamente en la terminal, es un modo no interactivo salvo si se especifica la opcion `-e`
en cuyo caso se pedirá la ruta o nombre del archivo a exportar.
Si no se especifica esta opción los resultados se mostrarán en un modo interactivo.

### Ejemplo con la opcion -t  

<script src="https://asciinema.org/a/A7mAanC41YN9tEZhxQq3eoiWr.js" id="asciicast-A7mAanC41YN9tEZhxQq3eoiWr" async></script>

### Ejemplo sin la opcion -t  

<script src="https://asciinema.org/a/MLW34JFR7aP9U9brs3fdiv2CR.js" id="asciicast-MLW34JFR7aP9U9brs3fdiv2CR" async></script>






