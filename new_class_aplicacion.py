import pyxel
from new_class_board import Board
from new_class_lemming import Lemming


# Creamos la clase app que será la encargada de hacer que el juego se inicie
class App:
    """Esta clase va a poner en marcha el juego"""
    # Usamos el método innit para guardar los atributos de la clase
    def __init__(self):
        # Establecemos las dimensiones del juego
        self.HEIGHT = 256
        self.WIDTH = 256
        # Usaremos distintas variables de la librería pyxel para crear el tablero y cargar el fichero con los recursos.
        pyxel.init(self.HEIGHT, 256, caption="It's Lemmings' time", fps=32)
        pyxel.load("total.pyxres")
        # Hacemos que el cursor aparezca en pantalla
        # Establecemos un atributo que pondrá en pausa el juego según sus valores
        self.__pausa = False
        pyxel.mouse(True)
        # Creamos una lista en la que se guardarán todos los objetos de la clase Lemming
        self.lista_lemmings = []
        # Creamos un atributo en el que se guardará un objeto de la clase tablero
        self.nivel = Board(self.lista_lemmings)
        # Creamos un atributo en el que se guardará el máximo de lemmings por partida
        self.__maxim = self.nivel.marcador.lemmings_restantes
        # Creamos un contador para dar entrada a cada lemming
        self.__count = 7
        # Por último hacemos que se ejecuten los métodos update y draw
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    # Definimos un property y un setter para la altura del tablero
    @property
    def HEIGHT(self):
        """Esta propiedad se va a encargar de que la altura del tablero siempre sea 256"""
        return self.__HEIGHT

    @HEIGHT.setter
    def HEIGHT(self, height):
        if height != 256:
            self.__HEIGHT = 256
        else:
            self.__HEIGHT = 256

    # Definimos un property y un setter para la anchura del tablero
    @property
    def WIDTH(self):
        """Está propiedad se va a encargar de que la anchura del tablero siempre sea 256"""
        return self.__WIDTH

    @WIDTH.setter
    def WIDTH(self, width):
        if width != 256:
            self.__WIDTH = 256
        else:
            self.__WIDTH = 256

    # Definimos el método update para que se hagan cambios en el juego
    def update(self):
        """ Este método se usa para que los valores del juego vayan cambiando según los fps establecidos.
        A través de este método llamaremos a todos los métodos update del resto de clases para que se ejecuten"""
        # Para poder pausar el juego al tocar la tecla del espacio
        if pyxel.btnp(pyxel.KEY_SPACE):
            # Se cambia el valor del atributo de la clase cada vez que se pulsa la tecla
            if self.__pausa:
                self.__pausa = False
            else:
                self.__pausa = True
        # Si el juego está en pausa no se hace nada
        if self.__pausa:
            pass
        # Si no está en pausa
        else:
            # Si se pulsa la tecla R se creará un nuevo nivel
            if pyxel.btnp(pyxel.KEY_R):
                # Se reformatearán todos los valores iniciales
                self.__count = 7
                self.lista_lemmings.clear()
                self.nivel = Board(self.lista_lemmings)
                self.__maxim = self.nivel.marcador.lemmings_restantes
            # Si se pulsa la tecla Q se saldrá del juego
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            # Iremos restando valor a uno de los contadores para que los lemmings vayan entrando
            if pyxel.frame_count % 4 == 0 and self.__maxim > 0:
                self.__count -= 1
                if self.__count == 0:
                    self.__maxim -= 1
                    self.lista_lemmings.append(Lemming(self.nivel))
                    self.__count = 7
            # Si hay más de un lemming realizar el update de cada uno
            if len(self.lista_lemmings) > 0:
                for i in self.lista_lemmings:
                    i.update()
                    # Si un lemming cava, cambiar el valor de la matriz del tablero para que el suelo desaparezca
                    if i.cavar:
                        self.nivel.ground[int((i.py // 16) + 1)][int(i.px // 16)] = 0
                        # Hacemos que esa pala no se pueda volver a usar
                        for e in self.nivel.lista_objetos[2]:
                            if e.coordenadas == [int((i.px // 16) * 16), int(((i.py // 16) + 1) * 16)]:
                                e.usado = True
        # Llamamos al método update del tablero
        self.nivel.update()

    # Definimos el método draw para que aparezca el juego por pantalla.
    def draw(self):
        """Este método lo usamos para que aparezcan por pantalla todas la imágenes que queramos introducir.
        A través de este método llamaremos a todos los métodos draw de cada clase para que se ejecuten"""
        # Establecemos un fondo negro
        pyxel.cls(0)
        # Llamamos al método draw del tablero
        self.nivel.draw()
        # Llamamos al método draw de cada lemming
        for i in self.lista_lemmings:
            i.draw()


# Hacemos q el juego se inicie
App()
