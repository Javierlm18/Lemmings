from random import randint
import pyxel
from class__escalera_derecha import EscaleraDer
from class_paraguas import Paraguas
from class_escalera_izquierda import EscaleraIzd
from class_bloqueador import Bloqueador
from class_pala import Pala
from class_marcador import Marcador


class Board:
    """Con esta clase crearemos objetos que representarán el tablero de la partida"""
    # Establecemos los atributos de la clase Board a través del método init
    def __init__(self, lista_lemmings):
        """Con este método estableceremos todos los atributos de la clase Board"""
        ground = []
        # Creamos un atributo en el que se guarden listas de cada herramienta.
        self.lista_objetos = [[], [], [], [], []]
        # Guardamos el valor de la entrada
        self.lista_lemmings = lista_lemmings
        # Damos entrada a un objetos de la clase marcador, donde aparecerá la información de la partida.
        self.marcador = Marcador(self.lista_objetos, self.lista_lemmings)
        #self.lemmings_totales = self.marcador.lemmings_restantes_totales
        # Establecemos un contador para quitar los objetos y que no sea inmediato.
        self.__count = 2
        # Establecemos otro contador para que el texto  final no aparezca inmediatamente después del final.
        self.__contador_final = 2
        # Creamos un atributo que comprobará si la partida se ha acabado
        self.fin = False
        # Creamos una matriz de 16 x 16 a través de listas anidadas
        for y in range(16):
            # Añadimos una lista a la lista principal, para finalmente tener 16 listas en una lista
            ground.append([])
            # Establecemos la longitud de las plataformas
            n = randint(5, 7)
            # Hacemos uso de un comprobador para que no salgan dos plataformas en una misma fila
            comprobador = False
            # Usamos una variable para saber si se comienza a poner la plataforma
            mostrar = False
            # Comenzamos a colocar números dentro de las listas de la lista
            for x in range(16):
                # Para que en las filas pares no haya bloques no aseguramos que todos los números sean ceros
                if y % 2 == 0:
                    ground[y].append(0)
                # Para las filas impares
                else:
                    # Si la variable comprobador es falsa, sigue una series de funciones
                    # para ver si cambia la variable mostrar
                    if not comprobador:
                        e = randint(0, 4)
                        # Si el número anterior es 1, las variables comprobador y mostrar se cambiaran
                        if e == 1:
                            comprobador = True
                            mostrar = True
                    # Para que siempre haya una plataforma de logitud mínima 5 nos aseguramos
                    # de que se construya una a partir de la columna 9
                    if x == 9 and not comprobador:
                        comprobador = True
                        mostrar = True
                    # Para establecer que va a haber plataforma
                    if mostrar:
                        ground[y].append(1)
                        # Vamos restando 1 a la longitud de la plataforma
                        n -= 1
                        # Cuando la longitud es 0, la plataforma finaliza y se siguen
                        # agregando ceros a la matriz
                        if n == 0:
                            mostrar = False
                    else:
                        ground[y].append(0)
        # Establecemos la matriz anterior como un atributo de la clase
        self.ground = ground

        # Ahora establecemos el suelo y las paredes, además del techo,
        # ya que arriba se va a dibujar el resultado de la partida
        for x in range(16):
            # Definimos el suelo
            self.ground[15][x] = 1
            # Definimos las paredes de ambos lados para darles una imagen diferente
            self.ground[x][0] = 5
            self.ground[x][15] = 6

        # El techo, al que vamos a pintar de otro color
        for y in range(0,2):
            for x in range(0,16):
                self.ground[y][x] = 1

        # Ahora vamos a colocar la entrada y la salida siguiendo un par de normas
        # Establecemos las filas de cada una de ellas
        self.fila_puerta = (randint(1, 7))*2
        self.fila_salida = (randint(1, 7))*2
        # Establecemos, la columna de lla puerta que estará o a la derecha o a la izquierda
        self.columna_puerta_inicio = randint(0, 1)
        # Si la variable anterior es un cero, la entrada se colocará a la izquierda
        if self.columna_puerta_inicio == 0:
            self.columna_entrada = 1
            # Establecemos dos bucles para encontrar un suelo sobre el que poner la entrada y la salida
            while self.ground[self.fila_puerta + 1][self.columna_entrada] != 1:
                self.columna_entrada += 1
            self.columna_salida = 15
            while self.ground[self.fila_salida + 1][self.columna_salida] != 1:
                self.columna_salida -= 1
        # Si no es un cero, se colocará a la derecha
        else:
            # Seguimos el mismo procedimiento anterior
            self.columna_entrada = 15
            while self.ground[self.fila_puerta + 1][self.columna_entrada] != 1:
                self.columna_entrada -= 1
            self.columna_salida = 1
            while self.ground[self.fila_salida + 1][self.columna_salida] != 1:
                self.columna_salida += 1

        self.puerta = (self.fila_puerta, self.columna_entrada)
        self.salida = (self.fila_salida, self.columna_salida)


        # Cambiamos el valor en la matriz para poder dibujar a su vez la entrada y la salida
        self.ground[self.fila_puerta][self.columna_entrada] = 20  # La entrada
        self.ground[self.fila_salida][self.columna_salida] = 30  # La salida

    # Definimos un método que comprueba si bajo la posición del cursor hay un objeto
    def __comprobar_posicion(self) -> bool:
        """Con este método estraeremos  un booleano que nos indicará si el cursor está sobre un objeto"""
        for i in range(len(self.lista_objetos)):
            for e in range(len(self.lista_objetos[i])):
                # Aquí comprobamos las coordenadas de cada herramienta con las del cursor
                if (self.lista_objetos[i][e].coordenadas == [int((pyxel.mouse_x // 16) * 16),
                                                             int((pyxel.mouse_y // 16) * 16)]):
                    return True

    # Creamos un método que aportará un texto  cuando la partida se acabe
    def __final(self):
        """Este método lo usaremos para mostrar por pantalla el resutado. Lo que hace es comprobar el número de
        lemmings que se han salvado. Según el resultado muestra un texto u otro"""
        if self.marcador.final:
            # Iremos restando uno a uno de los contadores de la clase
            if pyxel.frame_count % 32 == 0:
                self.__contador_final -= 1
                # Cuando el contador se haga 0 la partida habrá finalizado completamente
                if self.__contador_final == 0:
                    self.fin = True
        # Le indicaremos al jugador el modo para jugar una nueva partida
        if self.fin:
            pyxel.rect(0, 0, 256, 32, 0)
            pyxel.text(20, 16, "PULSA R PARA VOLVER A JUGAR", 3)
            # Si gana se mostrará por pantalla el resultado de su victoria
            if self.marcador.victoria:
                pyxel.text(20, 8, "ENHORABUENA HAS CONSEGUIDO SALVAR %s LEMMING." % self.marcador.salvados, 3)
            # Si pierde se mostrará por pantalla el resultado de su derrota
            else:
                pyxel.text(20, 8, "LO SIENTO, SOLO HAS SALVADO %s LEMMING." % self.marcador.salvados, 3)

    # Definimos el método update de la clase, en el que se guardarán todos los cambios que se hagan en el tablero
    def update(self):
        """Con este método haremos que se actualice toda la información del juego que aparezca a continuación"""
        # Vamos guardando en el atributo de la clase los nuevos valores se las herramientas.
        self.marcador.lista_objetos = self.lista_objetos
        # Vamos a dar la entrada a objetos
        # Primero nos aseguramos de que el ratón está situado sobre la pantalla del juego
        if pyxel.mouse_x < 256 and pyxel.mouse_y < 256:
            # Establecemos una variable para saber donde vamos a poder colocar objetos o no,
            # dependiendo de si hay un bloque o no, siguiendo los valores de la matriz del tablero
            if self.ground[pyxel.mouse_y // 16][pyxel.mouse_x // 16] in (1,5,6,20,30):
                bloque = True
            else:
                bloque = False
            # Establecemos la posibilidad de poder quitar objetos
            if pyxel.btn(pyxel.KEY_D):
                # Iremos restando 1 a uno de los contadores de la clase para que la herramienta tarde en quitarse
                if pyxel.frame_count % 16 == 0:
                    self.__count -= 1
                    # Si el contador se hace 0
                    if self.__count == 0:
                        self.__count = 2
                        # Busca el objeto con esas coordenadas dentro de la lista con todos los objetos, y lo elimina
                        for i in range(len(self.lista_objetos)):
                            for e in range(len(self.lista_objetos[i])):
                                if (self.lista_objetos[i][e].coordenadas == [int((pyxel.mouse_x // 16) * 16),
                                                                             int((pyxel.mouse_y // 16) * 16)]):
                                    del self.lista_objetos[i][e]


            # Para colocar cada objeto nos aseguramos de que no se dibuja sobre el bloque, salvo la pala, y de que no
            # hay un objeto ya en esa posición, para eso usamos el método creado anteriormente.
            # Establecemos la entrada de escaleras con dirección derecha a través de la tecla E
            if (pyxel.btnp(pyxel.KEY_E) and not bloque and not self.__comprobar_posicion()
                    and self.marcador.escaleras_total > 0):
                self.lista_objetos[0].append(EscaleraDer((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16))

            # Establecemos la entrada de paraguas a través de la tecla U
            if (pyxel.btnp(pyxel.KEY_U) and not bloque and not self.__comprobar_posicion()
                    and self.marcador.paraguas_total > 0):
                self.lista_objetos[4].append(Paraguas((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16))
            # Establecemos la entrada de escaleras con dirección hacia la izquierda con la tecla T
            if (pyxel.btnp(pyxel.KEY_T) and not bloque and not self.__comprobar_posicion()
                    and self.marcador.escaleras_total > 0):
                self.lista_objetos[1].append(EscaleraIzd((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16))
            # Establecemos la entrada de los bloqueadores a través de la tecla X
            if (pyxel.btnp(pyxel.KEY_X) and not bloque and not self.__comprobar_posicion()
                    and self.marcador.bloqueadores_total > 0):
                self.lista_objetos[3].append(Bloqueador((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16))
            # Establecemos la entrada de palas a través de la tecla A:
            if (pyxel.btnp(pyxel.KEY_A) and bloque and pyxel.mouse_y < 240 and not self.__comprobar_posicion()
                    and self.marcador.palas_total > 0):
                self.lista_objetos[2].append(Pala((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16))

        # Llamamos al método update del marcador para que se vaya actualizando también
        self.marcador.update()

    def draw(self):
        """Con este método haremos que aparezca por pantalla toda imagen relevante al tablero"""
        # Para pintar el tablero vamos comprobando valor por valor la matriz
        for y in range(16):
            for x in range(16):
                # Si hay un 1 pintamos el suelo
                if self.ground[y][x] == 1:
                    pyxel.blt(x * 16, y * 16, 0, 0, 0, 16, 16)
                # Si hay un 5 o un 6 pintamos las paredes
                elif self.ground[y][x] == 5:
                    pyxel.blt(x * 16, y * 16, 0, 16, 0, 16, 16)
                elif self.ground[y][x] == 6:
                    pyxel.blt(x * 16, y * 16, 0, 32, 0, 16, 16)
                # Pintamos la puerta
                elif self.ground[y][x] == 20:
                    pyxel.blt(x * 16, y * 16, 0, 16, 32, 16, 16, colkey=0)
                # Pintamos la salida
                elif self.ground[y][x] == 30:
                    pyxel.blt(x * 16, y * 16, 0, 32, 32, 16, 16, colkey=0)
        # Dibujamos cada herramienta recorriéndola lista de objetos y llamando al método update de cada objeto
        for i in self.lista_objetos:
            if len(i) > 0:
                for e in i:
                    e.draw()

        # Para dibujar el lugar donde se encuentra el cursor
        pyxel.blt((pyxel.mouse_x // 16) * 16, (pyxel.mouse_y // 16) * 16, 0, 0, 16, 16, 16, colkey=0)
        # Para dibujar el marcador
        self.marcador.draw()
        # Para dibujar el texto de final de partida
        self.__final()
