import pyxel


# Creamos la clase Pala que utilizaremos para crear palas
class Pala:
    """Esta clase va a crear objetos que representen a las palas"""

    # Usamos el método init para crear los atributos de la clase
    def __init__(self, posx, posy):
        """Usamos el método init para crear los atributos de la clase y darles valor"""
        self.__posx = posx
        self.__posy = posy
        # Creamos un atributo que contenga las coordenadas de cada objeto
        self.coordenadas = [self.__posx, self.__posy]
        # Creamos un atributo que nos indicará si la pala ha sido utilizada o no
        self.usado = False

    # Creamos un método draw para dibujar cada pala y que llamaremos desde el draw de la clase Board
    def draw(self):
        """Usamos el método draw para pintar el objeto sobre la pantalla"""
        if not self.usado:
            pyxel.blt(self.__posx, self.__posy, 0, 0, 32, 16, 16, colkey=15)
        # Si la pala se ha usado introduciremos una imagen negra
        else:
            pyxel.blt(self.__posx, self.__posy, 2, 0, 32, 16, 16, colkey=0)

