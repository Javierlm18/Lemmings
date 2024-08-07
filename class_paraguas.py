import pyxel


# Creamos la clase paraguas para que se creen los paraguas
class Paraguas:
    """Esta clase va a representar a los objetos paraguas"""

    # Usamos el método init para crear los atributos de la clase
    def __init__(self, posx, posy):
        """Usamos el método init para establecer los atributos de la clase y darles valor"""
        self.__posx = posx
        self.__posy = posy
        # Creamos un atributo que indica las coordenadas del objeto
        self.coordenadas = [self.__posx, self.__posy]

    # Usamos el método draw para dibujar cada paraguas y llamaremos a este método desde la clase Board
    def draw(self):
        """Usamos el método draw para dibujar el objeto en la pantalla"""
        pyxel.blt(self.__posx, self.__posy, 0, 48,16,16,16, colkey=0)



