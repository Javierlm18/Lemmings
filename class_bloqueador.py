import pyxel


# Creamos la clase bloqueador
class Bloqueador:
    """Esta clase va a crear  objetos que representen a los bloqueadores"""

    # Usamos el método init
    def __init__(self, posx, posy):
        """Usamos el método init para crear los atributos de la clase y darles valores"""
        # Creamos dos atributos que obtendrán el valor de entrada
        self.__posx = posx
        self.__posy = posy
        # Creamos un atributo que obtendrán las coordenadas del objeto
        self.coordenadas = [self.__posx, self.__posy]

    # Creamos el método draw que llamaremos desde la clase Board
    def draw(self):
        """Usamos el método draw para dibujar los objetos sobre la pantalla"""
        pyxel.blt(self.__posx, self.__posy, 0, 0, 48, 16, 16, colkey=0)