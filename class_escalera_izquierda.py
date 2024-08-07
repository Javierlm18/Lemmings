import pyxel


# Creamos una clase que cree objetos que representen escaleras orientadas hacia la izquierda
class EscaleraIzd:
    """Esta clase va a crear objetos que representen escaleras que están orientadas hacia la izquierda"""

    # Creamos el método init para crear los atributos de la clase
    def __init__(self, posx, posy):
        """Usamos el método init para crear los atributos de la clase y darles valores"""
        self.__posx = posx
        self.__posy = posy
        # Creamos un atributo que guarde las coordenadas del objeto
        self.coordenadas = [self.__posx, self.__posy]

    # Creamos el método draw y que llamaremos en la clase Board
    def draw(self):
        """Usamos el método draw para dibujar los objetos sobre la pantalla"""
        pyxel.blt(self.__posx, self.__posy, 0, 32, 16, 16, 16, colkey=0)