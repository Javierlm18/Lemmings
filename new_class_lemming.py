import pyxel


# Creamos la clase lemming
class Lemming:
    """Con esta clase crearemos objetos que representaran a los lemmings"""
    # Usamos el método innit para establecer los atributos de la clase
    def __init__(self, tablero: object):
        """Con el método init declaramos los atributos de la clase y les damos valor"""
        # Declaramos un atributo en el que se guarde la entrada que será el objeto de la clase Board
        self.tablero = tablero
        # Declaramos un atributo en el que se guarde la matriz del tablero
        self.ground = self.tablero.ground
        # Declaramos una serie de atributos que me indicarán como debe ser el movimiento del lemming
        self.__paraguas = False
        self.__escalera_derecha = False
        self.__escalera_izquierda = False
        self.__caer = False
        self.victoria = False
        self.muerto = False
        self.__escalera_derecha_bajar = False
        self.__escalera_izquierda_bajar = False
        self.cavar = False
        # Declaramos un atributo en que se guarde la lista con objetos
        self.lista_objetos = self.tablero.lista_objetos
        # Establecemos la posición inicial del lemming dependiendo de la posición de la puerta de entrada
        self.px = self.tablero.puerta[1] * 16 + 4
        self.py = self.tablero.puerta[0] * 16 + 6
        # Establecemos la velocidad del lemming, lo normal es que sea 1
        self.vx = 1
        # Cambiamos la velocidad del lemming si la puerta aparece orientada hacia la izquierda
        if self.tablero.columna_puerta_inicio == 1:
            self.vx *= -1
        # Establecemos una velocidad en el eje y inicial en 0
        self.vy = 0
        # Establecemos un valor para la gravedad
        self.gravedad = 0.5
        # Establecemos un valor de la velocidad en y cuando usa el paraguas y nos aseguramos que sea positiva
        self._vpar = (self.vx ** 2) ** 0.5

    # Creamos una propiedad para que la velocidad no sea mayor que 5
    @property
    def vx(self):
        return self.__vx

    @vx.setter
    def vx(self, vx):
        if vx > 5:
            self.__vx = 5
        else:
            self.__vx = vx

    @property
    def gravedad(self):
        return self.__gravedad

    # Creamos una propiedad para que el valor de la gravedad no sea mayor que uno.
    @gravedad.setter
    def gravedad(self,gravedad):
        if gravedad > 1:
            self.__gravedad = 1
        else:
            self.__gravedad = gravedad


    # Creamos un método para conseguir una lista con las coordenadas de todas las escaleras que suben hacia la derecha.
    def __lista_con_posiciones_esc_der(self) -> list:
        """Con este método conseguiremos una lista con las coordenada de todas las escaleras que van hacia la derecha"""
        lista_pos_esc_dere = []
        for i in self.lista_objetos[0]:
            lista_pos_esc_dere.append(i.coordenadas)
        return lista_pos_esc_dere

    # Creamos un método para conseguir una lista con coordenadas de todas las escaleras que suben hacia la izquierda.
    def __lista_con_posiciones_esc_izd(self) -> list:
        """Con este método conseguiremos una lista con todas las coordenadas de escaleras que van hacia la izquierda"""
        lista_pos_esc_izd = []
        for i in self.lista_objetos[1]:
            lista_pos_esc_izd.append(i.coordenadas)
        return lista_pos_esc_izd

    # Creamos un método para conseguir las coordenadas de todos los paraguas.
    def __lista_con_posiciones_paraguas(self) -> list:
        """Con este método conseguiremos una lista con las coordenadas de todos los paraguas"""
        lista_pos_paraguas = []
        for i in self.lista_objetos[4]:
            lista_pos_paraguas.append(i.coordenadas)
        return lista_pos_paraguas

    # Creamos un método para conseguir las coordenadas de todos los bloqueadores.
    def __lista_con_posiciones_bloqueadores(self) -> list:
        """Este método sirve para obtener una lista con las coordenada de las posiciones de todos los bloqueadores."""
        lista_pos_bloqueadores = []
        for i in self.lista_objetos[3]:
            lista_pos_bloqueadores.append(i.coordenadas)
        return lista_pos_bloqueadores

    # Creamos un método para conseguir las coordenadas de todas las palas.
    def __lista_con_posiciones_palas(self) -> list:
        """Este método sirve para obtener una lista con todas las coordenadas de las posiciones de las palas"""
        lista_pos_palas = []
        for i in self.lista_objetos[2]:
            lista_pos_palas.append(i.coordenadas)
        return lista_pos_palas

    # Definimos el movimiento de caminar
    def __caminar(self):
        """Con este método definiremos el movimiento del lemming cuando camina normal"""
        # Comprobamos si lo que tiene el lemming debajo es un bloque sobre el que caminar
        if self.ground[int((self.py // 16) + 1)][int(self.px // 16)] in (1, 5, 6):
            # Comprobamos si tiene debajo una pala
            if [(int(self.px // 16)) * 16,(int((self.py // 16) + 1) * 16)] in self.__lista_con_posiciones_palas():
                self.px = (self.px // 16) * 16 + 4
                # Cambiamos el valor del atributo de la clase para que ejecute el método excavar
                self.cavar = True
            # Si se sitúa sobre la salida
            elif self.ground[int((self.py // 16))][int(self.px // 16)] == 30:
                # Cambiaremos el valor del atributo la clase para que no se siga moviendo.
                self.victoria = True
                # Colocaremos al lemming justo en la casilla de la salida
                self.px = (self.px // 16) * 16
                self.py = (self.py // 16) * 16
            # Si no ocurre nada de lo anterior
            else:
                # Si se mueve hacia la derecha
                if self.vx > 0:
                    # Si se choca
                    if (self.ground[int(self.py // 16)][int((self.px + 6 + self.vx) // 16)] in (1,5, 6,) or
                        [((self.px + 6 + self.vx) // 16) * 16, ((self.py // 16) * 16)]
                            in self.__lista_con_posiciones_bloqueadores()):
                        self.vx *= -1
                    # Si se encuentra con una escalera para subir
                    elif ([(int((self.px + 6 + self.vx) // 16)) * 16, (self.py // 16) * 16]
                          in self.__lista_con_posiciones_esc_der()):
                        # Cambiamos el valor del atributo para que se ejecute el método de subir
                        self.__escalera_derecha = True
                        # Establecemos una velocidad en y
                        self.vy = - self.vx
                        # Colocamos al lemming justo al comienzo de la escalera
                        self.px = (((self.px + 6 + self.vx) // 16) * 16)
                        self.py -= 2
                    # Si se encuentra unas escaleras para bajar
                    elif ([(int((self.px + 6 + self.vx) // 16)) * 16, (int((self.py // 16) + 1) * 16)]
                          in self.__lista_con_posiciones_esc_izd()):
                        # Colocamos al lemming justo al comienzo de la escalera
                        self.px = (int((self.px + self.vx + 6) // 16)) * 16
                        self.py = (int((self.py // 16) + 1) * 16) - 6
                        # Cambiamos el valor de la variable para que ejecute el método de bajar esa escalera
                        self.__escalera_derecha_bajar = True
                        # Le damos un valor a la velocidad en y
                        self.vy = self.vx
                    # Si no se encuentra con nada avanza
                    else:
                        self.px += self.vx
                # Si se mueve hacia la izquierda
                else:
                    # Para que rebote
                    if (self.ground[self.py // 16][int((self.px + self.vx) // 16)] in (1,5, 6) or
                            [((self.px + self.vx) // 16) * 16, (self.py // 16) * 16] in
                            self.__lista_con_posiciones_bloqueadores()):
                        self.vx *= -1
                    # Si se encuentra unas escaleras por las que poder subir
                    elif ([(int((self.px + self.vx) // 16)) * 16, int(self.py // 16) * 16] in
                          self.__lista_con_posiciones_esc_izd()):
                        # Cambiamos el valor del atributo para que pueda subirlas
                        self.__escalera_izquierda = True
                        # Establecemos la velocidad en y correspondiente
                        self.vy = self.vx
                        # Colocamos al lemming al comienzo de la escalera
                        self.px = (((self.px + self.vx) // 16) * 16) + 10
                        self.py -= 2
                    # Si se encuentra unas escaleras por las que poder bajar
                    elif ([(int((self.px + self.vx) // 16)) * 16, (int(self.py // 16) + 1) * 16]
                          in self.__lista_con_posiciones_esc_der()):
                        # Colocamos al lemming al comienzo de las escaleras
                        self.px = (int((self.px + self.vx) // 16)) * 16 + 9
                        self.py = (int((self.py // 16) + 1) * 16) - 6
                        # Cambiamos el valor del atributo para que empiece a bajarlas
                        self.__escalera_izquierda_bajar = True
                        # Establecemos el valor de la velocidad en y
                        self.vy = - self.vx
                    # Si no se encuentra con nada, avanza
                    else:
                        self.px += self.vx
        # Si no tiene suelo sobre el que caminar, se cae
        else:
            self.__caer = True
            # Ajustamos la posición del lemming para que caiga por el medio de la casilla
            if self.vx < 0:
                self.px -= 7

    # Creamos un método para definir el movimiento de subir una escalera
    def __subir_escalera_derecha(self):
        """Con este método definiremos el movimiento del lemming si sube por una escalera que va hacia la izquierda"""
        # Para que siga subiendo si se encuentra con una escalera
        if ([((self.px + self.vx * (1 / (2 ** 0.5))) // 16) * 16,
             ((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16] in self.__lista_con_posiciones_esc_der()):
            # Avanza desplazándose en la misma medida en ambos ejes
            self.px = self.px + self.vx * (1 / (2 ** 0.5))
            self.py = self.py + self.vy * (1 / (2 ** 0.5))
        # Si no se encuentra con ninguna escalera
        else:
            # Cambiamos el valor del atributo para que ya no ejecute el método de subir la escalera
            self.__escalera_derecha = False
            # Si se encuentra con una pared o un bloque va a rebotar y va a comenzar a bajar la escalera
            if (self.ground[(int(self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16)]
                    [int(self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16] in (1, 5, 6)):
                # Cambiamos el valor del atributo para que baje la escalera
                self.__escalera_izquierda_bajar = True
                # Colocamos al lemming justo al comienzo de la escalera
                self.px = int((self.px // 16) * 16) + 9
                self.py = (int((self.py // 16) + 1) * 16) - 6
                # Cambiamos los valores de las velocidades en ambos ejes
                self.vy = self.vx
                self.vx = - self.vx
            # Si se encuentra un bloque sobre el que volver a caminar
            elif (self.ground[(int(self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) + 1]
                    [int(self.px + self.vx * (1 / (2 ** 0.5))) // 16] == 1):
                # Colocamos al lemming justo encima del bloque
                self.px = ((self.px + self.vx * (1 / (2 ** 0.5))) // 16) * 16
                self.py = int((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16 + 6
                #self.py += 1
            else:
                # Si no ocurre nada de lo anterior comienza a caer
                # Colocamos al lemming en la mitad de la casilla
                self.px = ((self.px + self.vx * (1 / (2 ** 0.5))) // 16) * 16 + 4
                self.py = int((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16 + 6
                # Cambiamos el valor del atributo para que ejecute el método descenso
                self.__caer = True
                # Modificamos la velocidad en el eje y
                self.vy *= -1

    # Definimos el método con los movimientos que realizará el lemming al subir una escalera que va hacia la izquierda.
    def __subir_escalera_izquierda(self):
        """Con este método definiremos el movimiento del lemming si sube escaleras hacia la izquierda"""
        # Si se encuentra con otra escalera
        if ([((self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16) * 16,
                ((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16] in self.__lista_con_posiciones_esc_izd()):
            # Sigue subiendo
            self.px = self.px + self.vx * (1 / (2 ** 0.5))
            self.py = self.py + self.vy * (1 / (2 ** 0.5))
        # Si no se encuentra con otra escalera para subir
        else:
            # Cambiamos el valor del atributo para que deje de subir
            self.__escalera_izquierda = False
            # Si se encuentra con una pared o con un bloque
            if (self.ground[(int(self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16)]
                    [int(self.px + self.vx * (1 / (2 ** 0.5))) // 16] in (1,5, 6)):
                # Cambiamos el valor del atributo para que comience a bajar
                self.__escalera_derecha_bajar = True
                # Colocamos al lemming justo al comienzo de la escalera
                self.py = ((int(self.py + 12 + self.vy * (1 / (2 ** 0.5)))) // 16 + 1) * 16 - 6
                self.px = (((self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16) + 1) * 16
                # Cambiamos los valores de las velocidades de ambos ejes
                self.vx = - self.vx
                self.vy = self.vx
            # Si se encuentra un bloque sobre el que caminar
            elif (self.ground[(int(self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) + 1]
                    [int(self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16] == 1):
                # Colocamos al lemming justo encima del bloque
                self.px = (((self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16) * 16) + 10
                self.py = int((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16 + 6
            # Si no se encuentra nada va a caer
            else:
                # Colocamos al lemming justo en el medio de la casilla
                self.px = ((self.px + 6 + self.vx * (1 / (2 ** 0.5))) // 16) * 16 + 4
                self.py = int((self.py + 12 + self.vy * (1 / (2 ** 0.5))) // 16) * 16 + 6
                # Cambiamos el valor del atributo para que empiece a caer
                self.__caer = True
                # Cambiamos el valor de la velocidad
                self.vy *= -1

    # Definimos un método para bajar escaleras orientadas hacia la derecha
    def __bajar_escalera_derecha(self):
        """Con este método definiremos el movimiento del lemming si baja escaleras hacia la derecha"""
        # Si se sigue encontrando escaleras va a seguir bajando
        if[int((self.px + 5) // 16) * 16, int((self.py + 11) // 16) * 16] in self.__lista_con_posiciones_esc_izd():
            # Hacemos que el lemming baje
            self.px = self.px + self.vx * (1 / (2 ** 0.5))
            self.py = self.py + self.vy * (1 / (2 ** 0.5))
        # Si no se encuentra otra escalera sobre la que seguir bajando
        else:
            # Cambiamos el valor del atributo para que deje de bajar
            self.__escalera_derecha_bajar = False
            # Si se encuentra con una pared o un bloque va a comenzar a subir esa escalera
            if self.ground[(int(self.py + 11) // 16) - 1][int((self.px + 5) // 16)] in (1, 5, 6):
                # Cambiamos el valor del atributo para que comience a subir
                self.__escalera_izquierda = True
                # Cambiamos el valor de las velocidades de ambos ejes
                self.vy = - self.vx
                self.vx *= -1
                # Colocamos al lemming justo al comienzo de la escalera
                self.px = (((self.px + 5) // 16) - 1) * 16 + 10
                self.py = (((self.py + 11) // 16) - 1) * 16 + 4
            # Si se encuentra un bloque sobre el que caminar
            elif self.ground[int((self.py + 11) // 16)][int((self.px + 5) // 16)] == 1:
                self.px = (int((self.px + 5) // 16)) * 16
                self.py = (int((self.py + 11) // 16) - 1) * 16 + 6
            # Sino comenzará a caer, por lo que calocamos al lemming justo en medio de la casilla
            else:
                self.px = (int((self.px + 5) // 16)) * 16 + 3
                self.py = (int((self.py + 11) // 16) - 1) * 16 + 6

    # Definimos un método para que el lemming baje escaleras orientadas hacia la izquierda
    def __bajar_escalera_izquierda(self):
        """Con este método definiremos el movimiento del lemming si baja hacia la izquierda"""
        # Si se encuentra otra escalera por la que bajar
        if [int(((self.px + 1) // 16) * 16), int((self.py + 12) // 16) * 16] in self.__lista_con_posiciones_esc_der():
            # Hacemos que el lemming baje la escalera
            self.px = self.px + self.vx * (1 / (2 ** 0.5))
            self.py = self.py + self.vy * (1 / (2 ** 0.5))
        # Si no se encuentra otra escalera por la que bajar
        else:
            # Cambiamos el valor del atributo para que no siga más el método de bajar
            self.__escalera_izquierda_bajar = False
            # Si se encuentra con una pared o un bloque, va a comenzar a subir la escalera
            if self.ground[int(((self.py + 12) // 16) - 1)][int((self.px + 1) // 16)] in (1,5, 6):
                # Cambiamos el valor del atributo para que comience a subir
                self.__escalera_derecha = True
                # Colocamos al lemming al comienzo de la escalera
                self.px = (int((self.px + 1) // 16) + 1) * 16
                self.py = (((int(self.py + 12)) // 16) - 1) * 16 + 4
                # Modificamos los valores de las velocidades de ambos ejes
                self.vy = self.vx
                self.vx *= -1
            # Si se encuentra un bloque sobre el que comenzar a caminar
            elif self.ground[int((self.py + 12) // 16)][int((self.px + 1) // 16)] == 1:
                # Colocamos al lemming justo encima del bloque
                self.px = int((self.px + 1) // 16) * 16
                self.py = (int((self.py + 12) // 16) - 1) * 16 + 6
            # Si no se encuentra nada, va a caer
            else:
                # Colocamos al lemming justo en mitad de la casilla
                self.px = int((self.px + 1) // 16) * 16 + 3
                self.py = (int((self.py + 12) // 16) - 1) * 16 + 6

    # Definimos el método para que caiga
    def __descenso(self):
        """Con este método definiremos el movimiento del lemming si esta cayendo"""
        # Si está sobre un paraguas
        if [int(self.px // 16) * 16, int(self.py // 16) * 16] in self.__lista_con_posiciones_paraguas():
            # Modificamos la posición en el eje x para que parezca que no se ha desviado, ya que la imagen ocupa más
            self.px = (self.px // 16) * 16 + 1
            # Cambiamos el valor del atributo para que se active el paraguas
            self.__paraguas = True
        # Si no tiene un bloque debajo
        if self.ground[int((self.py + self.vy + 14) // 16)][int(self.px//16)] in (0, 20, 30):
            # Tiene un paraguas debajo
            if ([int(self.px // 16) * 16, int((self.py + self.vy + 15) // 16) * 16]
                    in self.__lista_con_posiciones_paraguas()):
                # Si no llevaba un paraguas
                if not self.__paraguas:
                    # Modificamos la posición como antes
                    self.px = (self.px // 16) * 16 + 1
                    self.__paraguas = True
                    # Colocamos al lemming justo al comienzo de la casilla
                    self.py = int((self.py + self.vy + 14) // 16) * 16
            # Si no lleva paraguas
            if not self.__paraguas:
                # Controlamos el valor de la velocidad para que nunca sea mayor que 5
                if self.vy + self.gravedad < 5:
                    self.vy += self.gravedad
                # Si es mayor que 5, establecerla en 5
                else:
                    self.vy = 5
                # Bajará con la velocidad correspondiente
                self.py += self.vy
            # Si se encuentra con la meta mientras baja
            if self.ground[int((self.py + self.vy + 14) // 16)][int(self.px//16)] == 30:
                # Dejará de bajar
                self.__caer = False
                # Colocaremos al lemming en la posición adecuada
                self.py = (((self.py + self.vy + 15) // 16) * 16)
                self.px = (self.px // 16) * 16
                # Cambiaremos el valor de los atributos, para que deje el paraguas y para que muestre la victoria
                self.victoria = True
                self.__paraguas = False
            # Si no se encuentra con la meta, bajar con la velocidad con paraguas
            else:
                self.py += self._vpar
        # Si se encuentra con n bloque
        else:
            # Si no lleva el paraguas
            if not self.__paraguas:
                # El lemming muere, por lo que cambiamos los valores de los atributos
                self.muerto = True
                # Colocamos al lemming para que el cadaver aparezca justo en el medio de la casilla
                self.px = int(self.px//16) * 16 + 2
                self.py = int(((self.py + self.vy + 14) // 16) - 1) * 16 + 10
                # Cambiamos el valor del atributo para que deje de caer
                self.__caer = False
            # Si lleva el paraguas
            else:
                # Hacemos que deje de llevar el paraguas
                self.__paraguas = False
                # Colocamos al lemming justo encima del bloque
                self.px = (self.px // 16) * 16 + 3
                self.py = int(((self.py + self.vy + 14) // 16) - 1) * 16 + 6
                # Hacemos que deje de caer
                self.__caer = False

    # Definimos el método de cavar
    def excavar(self):
        """Con este método definiremos el comportamiento del lemming si se encuentra sobre una pala"""
        # Lo único que hacemos es que deje de cavar y comience a caer
        self.__caer = True
        self.cavar = False

    # Definimos el método update, que va a llamar al resto de métodos y que va a ser llamado por el update de App
    def update(self):
        """A través de este método actualizaremos la posición del lemming dependiendo de los valores de los atributos"""
        # Si no está muerto
        if not self.muerto:
            # Está subiendo escaleras que van hacia la derecha
            if self.__escalera_derecha:
                self.__subir_escalera_derecha()
            # Está bajando escaleras que están orientadas hacia la izquierda
            elif self.__escalera_derecha_bajar:
                self.__bajar_escalera_derecha()
            # Está cayendo
            elif self.__caer:
                self.__descenso()
            # Está subiendo escaleras hacia la izquierda
            elif self.__escalera_izquierda:
                self.__subir_escalera_izquierda()
            # Está bajando escaleras que están orientadas hacia la izquierda
            elif self.__escalera_izquierda_bajar:
                self.__bajar_escalera_izquierda()
            # Tiene que excavar
            elif self.cavar:
                self.excavar()
            # Ha ganado
            elif self.victoria:
                self.px = self.px
            # No se cumplen el resto de cosas por que va a caminar
            else:
                self.__caminar()
        # Si está muerto
        else:
            self.muerto = True

    # Definimos el método draw que va a ser llamado por el draw de App.
    def draw(self):
        """A través de este método se dibujará la imagen correspondiente del lemming, dependiendo de los valores
        de los atributos"""
        # Al igual que el método update, dependiendo de lo que haga el lemming va a dibujar una u otra cosa
        if self.__escalera_derecha:
            pyxel.blt(self.px, self.py, 1, 4, 35, 6, 11, colkey=0)
        elif self.__escalera_izquierda:
            pyxel.blt(self.px, self.py, 1, 12, 35, 7, 11, colkey=0)
        elif self.__escalera_derecha_bajar:
            pyxel.blt(self.px, self.py, 1, 12, 35, 7, 11, colkey=0)
        elif self.__escalera_izquierda_bajar:
            pyxel.blt(self.px, self.py, 1, 4, 35, 6, 11, colkey=0)
        elif self.muerto:
            pyxel.blt(self.px, self.py, 1, 18, 26, 11, 6, colkey=0)
        elif self.__paraguas:
            pyxel.blt(self.px, self.py, 1, 49, 1, 14, 17, colkey=0)
        elif self.__caer:
            pyxel.blt(self.px, self.py, 1, 35, 17, 9, 16, colkey=0)
        elif self.cavar:
            pyxel.blt(self.px, self.py, 1, 4, 21, 10, 10, colkey=0)
        elif self.victoria:
            pyxel.blt(self.px, self.py, 0, 32, 48, 16, 16, colkey=0)
        else:
            pyxel.blt(self.px, self.py, 1, 5, 6, 6, 10, colkey=0)
