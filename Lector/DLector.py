

class DLector:
    
    @staticmethod

    def __abreArchivos__(rutas):
        contenido = []
        for ruta in rutas:
            archivo = open(ruta)
            contenido.append(archivo.readlines())
            archivo.close()
        return contenido

    @staticmethod
    def __guardaArchivos__(ruta,nombre,datos):
        nomArchivo = ruta+nombre
        archivo = open(nomArchivo,'w')
        for elemento in datos:
            archivo.write(elemento)
        archivo.close()
