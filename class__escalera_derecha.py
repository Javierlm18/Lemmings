import pyxel


# Creamos una clase que cree objetos que representen escaleras que van hacia la derecha
class EscaleraDer:
    """Esta clase va a crear objetos que representen escaleras que están orientadas hacia la derecha """
    # Utilizamos el método init para establecer los atributos de la clase
    def __init__(self, posx, posy):
        """Usamos el método init para crear los valores de la clase y establecer sus valores"""
        # Establecemos los valores de la posición utilizando los valores de entrada
        self.__posx = posx
        self.__posy = posy
        # Creamos un atributo que utilizaremos fuera de la clase, que contenga las coordenadas del objeto
        self.coordenadas = [self.__posx, self.__posy]

    # Usamos el método draw que llamaremos en la clase Board
    def draw(self):
        """Usamos el método draw para pintar los objetos sobre la pantalla"""
        pyxel.blt(self.__posx, self.__posy, 0, 16, 16, 16, 16, colkey=0)






