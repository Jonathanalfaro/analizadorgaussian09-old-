from NResumen import  NResumen

class VResumenTer:


    def __init__(self, parametrosentrada):
        self.ruta1 = parametrosentrada[len(parametrosentrada) - 1]
        self.paramentrosresumen = parametrosentrada
        self.contenidoArchivo = NResumen.obtencontenidolog(self.ruta1)
        self.resumen = NResumen.hazresumen(self.contenidoArchivo, self.paramentrosresumen)
        for elemento in self.resumen:
            print elemento