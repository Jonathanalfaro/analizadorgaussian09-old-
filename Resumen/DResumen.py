class DResumen:


    @staticmethod
    def abrearchivo(ruta):
        archivo = open(ruta)
        contenido = archivo.readlines()
        archivo.close()
        return contenido
