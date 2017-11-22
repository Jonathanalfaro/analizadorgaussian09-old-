
class DResumen:


    @staticmethod
    def abreArchivo(ruta):
        archivo = open(ruta)
        contenido = archivo.readlines()
        archivo.close()

        return contenido