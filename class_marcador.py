import pyxel
from random import randint


# Creamos una clase para crear el marcador
class Marcador:
    """Esta clase va a crear objetos que usaremos como marcador para expresar los resultados de la partida"""
    # Usamos el método init para establecer los atributos de la clase
    def __init__(self, lista_objetos, lista_lemmings):
        """Usamos el método init para crear los atributos de la clase y darles valor"""
        # Creamos una serie de atributos que señalen el número máximo de cada herramienta,
        # los lemmings que van a aparecer, los que se salvan o los que mueren.
        self.lista_lemmings = lista_lemmings
        self.lemmings_restantes = randint(10,20)
        self.__lemmings_restantes_totales = 0
        self.lista_objetos = lista_objetos
        self.lemmings_muertos = 0
        self.palas = randint(2,3)
        self.palas_total, self.paraguas_total, self.escaleras_total, self.bloqueadores_total = 0, 0, 0, 0
        self.paraguas = randint(2,4)
        self.escaleras = randint(10,12)
        self.bloqueadores = randint(3,4)
        self.salvados = 0
        # Usamos dos variables para darle fin al juego y para ver si se ha conseguido la victoria
        self.final = False
        self.victoria = False

    # Creamos el método update para que se hagan cambios y que se llamará desde la clase board.
    def update(self):
        """Usamos el método update para que los valores del marcador se vayan modificando según los fps"""
        self.palas_total = self.palas - len(self.lista_objetos[2])
        self.escaleras_total = self.escaleras - len(self.lista_objetos[0]) - len(self.lista_objetos[1])
        self.bloqueadores_total = self.bloqueadores - len(self.lista_objetos[3])
        self.paraguas_total = self.paraguas - len(self.lista_objetos[4])
        self.__lemmings_restantes_totales = self.lemmings_restantes - len(self.lista_lemmings)
        m = 0
        s = 0
        # Recorremos la lista de los lemmings para saber cuantos han muerto y cuantos se han salvado
        for i in self.lista_lemmings:
            if i.muerto:
                m += 1
            if i.victoria:
                s += 1
        self.lemmings_muertos = m
        self.salvados = s
        # Comprobamos si la partida se ha acabado
        if self.salvados + self.lemmings_muertos == self.lemmings_restantes:
            self.final = True
            # Comprobamos si se ha obtenido la victoria
            if self.salvados >= self.lemmings_restantes / 2:
                self.victoria = True

    # Creamos el método draw para dibujar los resultados y que llamaremos desde el draw de la clase Board
    def draw(self):
        """Usamos el método draw para dibujar el objetos sobre la pantalla"""
        pyxel.rect(0, 0, 256, 32, 0)
        pyxel.text(120, 8, "Lemmings muertos: %s" % self.lemmings_muertos, 3)
        pyxel.text(12, 8, "Lemmings restantes: %s" % self.__lemmings_restantes_totales, 3)
        pyxel.text(215, 8, "Palas: %s" % self.palas_total, 3)
        pyxel.text(8, 18, "Salvados: %s" % self.salvados, 3)
        pyxel.text(65, 18, "Bloqueadores: %s" % self.bloqueadores_total, 3)
        pyxel.text(140, 18, "Paraguas: %s" % self.paraguas_total, 3)
        pyxel.text(200, 18, "Escaleras: %s" % self.escaleras_total, 3)
