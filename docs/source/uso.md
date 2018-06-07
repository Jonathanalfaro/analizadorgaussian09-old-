
# Uso

El programa permite el paso de parámetros para indicarle que secciones de la salida de **Gaussian** quieres extraer.  

El siguiente texto tiene como objetivo brindarte ayuda de como se utiliza el programa, la información está acompañada por un video en el que se explica detalladamente como utilizar cada una de las opciones y  pausar el video en cualquier momento y seleccionar los comandos de ejemplo para pegarlos en tu terminal para probar su funcionamiento.  

## Descarga y asignación de permiso para ejecutar

Esta es una manera sencilla de descargar el programa haciendo uso de la terminal, si sigues las instrucciones del video podras descargar y utilizar el programa en un solo unos minutos.

<script src="https://asciinema.org/a/3iShTUdgTxjFslhUCyuk4SdMc.js" id="asciicast-3iShTUdgTxjFslhUCyuk4SdMc" async></script>

## Uso básico

El uso básico del programa es de la siguiente forma:

` $ ./jag09.py [opciones] [archivos] `  

Como se pudo observar en el video anterior, se puede acceder a una lista de opciones que soporta el programa de la siguiente manera:  

<script src="https://asciinema.org/a/1xLsTi5X4O7pHukn4TqQYAZJ8.js" id="asciicast-1xLsTi5X4O7pHukn4TqQYAZJ8" async></script>

## Opciones -m, -apt, -hf, -tc, hsd, acm, mep  

### Opción -m (Mulliken population analisis)  

<script src="https://asciinema.org/a/J5GHMyixymUKNpUwYIDa2DEoV.js" id="asciicast-J5GHMyixymUKNpUwYIDa2DEoV" async></script>

### Opción -apt (Atomic polar tensor analisis)  

<script src="https://asciinema.org/a/gDiZU16zTz09S9eQWYWy9juNM.js" id="asciicast-gDiZU16zTz09S9eQWYWy9juNM" async></script>

### Opción -hf (Energía de Hirshfeld)  

<script src="https://asciinema.org/a/OVgOTa42JPROOSEwaUrDz7dDT.js" id="asciicast-OVgOTa42JPROOSEwaUrDz7dDT" async></script>

### Opción -tc (Datos termoquímicos)  

<script src="https://asciinema.org/a/9RLu16qdfPO2NXiqth8Zc1G93.js" id="asciicast-9RLu16qdfPO2NXiqth8Zc1G93" async></script>

### Opción -hsd   ( Hirshfeld spin densities)

<script src="https://asciinema.org/a/HMwgeNVxfYkP5U19iKSfGxk6i.js" id="asciicast-HMwgeNVxfYkP5U19iKSfGxk6i" async></script>

### Opción -acm (Atomic charges matrix diagonal)

<script src="https://asciinema.org/a/dpAaZ53iBAqUinE2zuAWMK2rR.js" id="asciicast-dpAaZ53iBAqUinE2zuAWMK2rR" async></script>


Estas opciones pueden ser combinadas entre ellas

<script src="https://asciinema.org/a/IyELYw8hcxTMW8L9BnqWuBjA7.js" id="asciicast-IyELYw8hcxTMW8L9BnqWuBjA7" async></script>


## Opción MEP (Molecular electrostatic potential)

<script width="32" height="24" src="https://asciinema.org/a/oFxTJ7CRfzUWzyu92JJyyFsVH.js" id="asciicast-oFxTJ7CRfzUWzyu92JJyyFsVH" async></script>


## Opción NAO (Natural atomic orbital occupancies)


La opción NAO admite el paso de un parámetro adicional, este parametro es el símbolo químico del átomo al cual se le va a hacer
el análisis, ejemplo para el Átomo de Nitrógeno:  

` $ python Ag09principal.py -nao N salida.log `  

<script src="https://asciinema.org/a/EN6o7gxMhfrkNcVqM6LtjTQnx.js" id="asciicast-EN6o7gxMhfrkNcVqM6LtjTQnx" async></script>  

## Opción exportar -e


Si se especifica la opcion ` -e ` se guardarán los datos de las opciones especificadas a un archivo separado por comas CSV, y se pedirá que escriba la ruta o el nombre de un archivo donde se guardarán los datos obtenidos segun las opciones que se hayan especificado.

<script src="https://asciinema.org/a/928rzEI7VoqBDj0JEgxAt1tQP.js" id="asciicast-928rzEI7VoqBDj0JEgxAt1tQP" async></script>

### Notas  

* Se debe tener permiso para escribir en la ruta especificada.
* Si no se da una ruta y solo se escribe el nombre de archivo el archivo CSV se guardará en el directorio actual de trabajo
* Aunque no es obligatorio se recomienda que los nombres de archivos no contengan espacios ni caracteres especiales.

## Procesar todas las opciones


Se pueden procesar todas las opciones al mismo tiempo con la opcion corta -a o la opcion larga --ALL

<script src="https://asciinema.org/a/zNB976qWDkEOe9oH621bUBzyu.js" id="asciicast-zNB976qWDkEOe9oH621bUBzyu" async></script>  

## Opción -t

Muestra el resultado del análisis directamente en la terminal, es un modo no interactivo salvo si se especifica la opcion `-e`
en cuyo caso se pedirá la ruta o nombre del archivo a exportar.
Si no se especifica esta opción los resultados se mostrarán en un modo interactivo.

### Ejemplo con la opcion -t  

<script src="https://asciinema.org/a/A7mAanC41YN9tEZhxQq3eoiWr.js" id="asciicast-A7mAanC41YN9tEZhxQq3eoiWr" async></script>

### Ejemplo sin la opcion -t  

<script src="https://asciinema.org/a/MLW34JFR7aP9U9brs3fdiv2CR.js" id="asciicast-MLW34JFR7aP9U9brs3fdiv2CR" async></script>
