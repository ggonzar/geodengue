#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del AeAegypti y sus estados (Huevo,
Larva, Pupa, Adulto) para, finalmente, representar a un individuo.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
#Se impotan los modulos.
from models import *

from random import randint
"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])
class AeAegypti :
    """
    Clase base, contiene la definición los atributos básicos.
    """
    @property
    def espectativa_vida(self):
        """
        Expectativa de vida : es un valor numérico que varía de acuerdo a las
        condiciones climáticas a las que es sometido el mosquito.
        """
        return self.__espectativa_vida

    @property
    def edad(self):
        """
        La edad es la cantidad de horas que lleva el individuo lleva vivo.
        """
        return self.__edad

    @property
    def sexo(self):
        """
        El sexo puede ser Macho o hembra, valor generado aleatoriamente.
        """
        return self.__sexo

    @property
    def estado(self):
        """
        Indica el estado actual de la clase.
        """
        return self.__estado

    def __init__(self, sexo=None, estado=None) :
        """
        Inicializa la clase setenado la espectativa de vida y la edad a
        cero.

        @type sexo : Enum
        @param sexo: El sexo del AeAegypti

        @type estado : Enum
        @param estado: El estado del AeAegypti
        """
        self.__edad = 0;
        self.__espectativa_vida = 100;
        self.__sexo = sexo;
        self.__estado = estado;

    def se_reproduce (self, hora) :
        """
        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return False;

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            "vida=" + str(self.espectativa_vida) + \
            " edad=" + str(self.edad) + \
            " id=" +str(self._id)


class Huevo(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    huevo.
    """
    def __init__(self) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [estado]: El estado del individuo
        """
        # Se genera de forma aleatoria el sexo del huevo
        sexo = randint(0, 1)
        if sexo == 0 :
            sexo = Sexo.MACHO
        else :
            sexo = Sexo.HEMBRA
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,sexo, Estado.HUEVO);

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            huevo   2 a 3 dias
        """
        return self.espectativa_vida <= 0

    def desarrollar(self, hora) :
        """
        El desarrollo embriológico generalmente se completa en 48 horas
        si el ambiente es húmedo y cálido, pero puede prolongarse hasta
        5 días a temperaturas más bajas.

        1) Los huevos son depositados individualmente en las paredes de los
        recipientes por encima del nivel del agua.
        2) Una vez que se ha completado el desarrollo embrionario los
        huevos son capaces de resistir largos períodos de desecación,
        que pueden prolongarse por más de un año.
        3) Cuando los huevos son mojados, se genera un estímulo para la eclosión.
        4) Algunos huevos hacen eclosión en los primeros 15 minutos de
        contacto con el agua, al tiempo que otros pueden no responder hasta
        que han sido mojados varias veces.

        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 5*24 :
            estado = randint(2, 5) * 24
            if estado <= self.edad :
                return Larva(self.sexo);
        """
        TODO Como afecta las condiciones climáticas al desarrollo del huevo ?
        """
        self.espectativa_vida -= 0.1389

        return self;

class Larva(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    larva.
    """
    def __init__(self, previous_sexo=None) :
        """
        @type previous_sexo : Enum
        @param previous_sexo: El el sexo del huevo a partir del cual eclosionó la larva.
        """
        if previous_sexo == None :
            # Se genera de forma aleatoria el sexo del mosquito
            sexo = randint(0, 1)
            if sexo == 0 :
                previous_sexo = Sexo.MACHO
            else :
                previous_sexo = Sexo.HEMBRA

        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,previous_sexo, Estado.LARVA);

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            larva   4 a 14 dias
        """
        return (self.espectativa_vida <= 0 or self.edad > 14 * 24 )


    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de larva

        El desarrollo larval a 14oC es irregular y la mortalidad
        relativamente alta. Por debajo de esa temperatura, las larvas
        eclosionadas no alcanzan el estado adulto. En condiciones óptimas
        el período larval puede durar 5 días pero comúnmente se extiende
        de 7 a 14 días.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 14*24  :
            estado = randint(4, 14) * 24
            if estado <= self.edad :
                print str(self)
                return Pupa(self.sexo)

        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        larva ?
        """
        self.espectativa_vida -= 0.1389
        return self;

class Pupa(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    pupa.
    """
    def __init__(self, previous_sexo) :
        """
        @type previous_sexo : Enum
        @param previous_sexo: El sexo de la larva a partir del cual evoluciono a pupa.
        """
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,previous_sexo, Estado.PUPA);

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            pupa    1 a 4 dias
        """
        return (self.espectativa_vida <= 0 or self.edad > 19*24 )

    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de pupa.

        El estado de pupa demora de 2 a 3 días.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 19*24 :
            estado = randint(14, 19) * 24
            if estado <= self.edad :
                print str(self)
                return Adulto(self.sexo)

        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        pupa ?
        """
        self.espectativa_vida -= 0.1389
        return self

class Adulto(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    adulto.
    """

    @property
    def ultima_oviposicion (self):
        return self.__ultima_oviposicion;

    def __init__(self, previous_sexo) :
        """
        @type previous_sexo : Enum
        @param previous_sexo: El sexo de la pupa a partir del cual evoluciono a adulto.
        """
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,previous_sexo, Estado.ADULTO);

    def se_reproduce (self, hora):
        """
        El apareamiento ocurre dentro de las 24 horas siguientes a la
        emergencia. Éste se realiza durante el vuelo, pero en algunas
        ocasiones se lleva a cabo en una superficie vertical u horizontal

        El mosquito se reproduce si :
        * No está muerto = no
        * Sexo = hembra, temperatura > 18 C

        * Un día cualquiera es día de oviposición, si T>18o C en algún
        lapso del día, pero si T<18o todo el día, no pone huevos.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        """
        return self.esta_muerto() == False \
            and self.sexo == Sexo.HEMBRA \
            and hora.temperatura > 18

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.

        adulto  si espectativa de vida <= 0, si edad >= 30 dias.
        """
        return (self.espectativa_vida <= 0 or self.edad >= 30*24 )

    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado final de adulto.

        Cómo le afecta la temperatura : Limitantes para el desarrollo poblacional.
        Entre ellos, dentro del ambiente abiótico el potencial del vector

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        if hora.temperatura >= 40 or hora.temperatura <= 0 :
            """
            Día letal: si ocurre T<0o (T mínima diaria <0o) ó T> 40o C
            (T máxima diaria >40o C), ó aire muy seco. Se consideran
            fenecidas todas las formas adultas, y larvarias en el caso térmico,
            """
            self.espectativa_vida -= 4.3;
        else :
            """
            En el mejor de los casos y en condiciones optimas el individuo
            llegaría a los 30 días. Teniendo en cuenta que su espectativa
            de vida es 100, se debería disminuir su espectativa de vida
            según el siguiente cálculo:

               delta = 100/(30*24)
            """
            self.espectativa_vida -= 0.1389
        return self;

    def buscar_alimento(self, hora):
        """
        Se tiene en cuenta la ubicacion del mosquito adulto y la densidad
        poblacional en dicha ubicación.

        * Día adverso, si T máxima <15oC no vuela (por debajo de este umbral
        de vuelo, no vuela, no pica, ni ovipone). En definitiva, el potencial
        climático del vector es función de la temperatura y de la no-ocurrencia
        de valores por encima o por debajo de umbrales críticos, tanto térmicos
        como de humedad. Es de notar que para el caso de deficiencias de
        humedad, lo letal es función de la duración del período.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        if hora.temperatura < 15 :
            return


    def poner_huevos(self, hora) :
        """
        Generalmente el apareamiento se realiza cuando la hembra busca
        alimentarse; se ha observado que el ruido que emite al volar es
        un mecanismo por el cual el macho es atraído.

        Una vez copulada e inseminada la hembra, el esperma que lleva es
        suficiente para fecundar todos los huevitos que produce durante su
        existencia, no aceptando otra inseminación adicional.

        Su ciclo para poner huevos es de aproximadamente cada tres días.
        Su alimentación puede hacerla en cualquier momento (puede picar
        varias veces a las personas de una casa). Las proteínas contenidas
        en la sangre le son indispensables para la maduración de los huevos.
        La variación de temperatura y humedad, así como la latitud pueden
        hacer variar estos rangos del ciclo de vida de los mosquitos.

        La hembra deposita sus huevos en las paredes de recipientes con
        agua estancada, limpia y a la sombra. Un solo mosquito puede poner
        80 a 150 huevos, cuatro veces al día.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """

        #Su ciclo para poner huevos es de aproximadamente cada tres días a
        # cuatro días
        ciclo = randint(3, 4)
        # se verifica la cantidad de días que pasaron desde su ultima
        # oviposición.
        if self.ultima_oviposicion % (ciclo * 24) == 0 :
            # Un solo mosquito puede poner 80 a 150 huevos, cuatro veces
            # al día.
            cantidad = randint(80, 150)
            huevos = []
            for i in range(cantidad) :

                huevos.append(self.get_child())
            # se reinicia el contador
            self.ultima_oviposicion = 1;

            return huevos

        # se aumenta el contador de ultima oviposición
        self.ultima_oviposicion += 1
        return None


class Individuo :
    INDEX_IND = 1
    """
    Esta clase contiene la representación de un individuo de la población.
    Un mosquito de la población tiene los siguientes atributos :
    * mosquito : Huevo, Larva, Pupa, Adulto.
    * Ubicación : coordenadas longitud y latitud
    * Dispositivo de origen : el código del dispositivo de ovipostura de origen.
    """
    def __init__ (self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [estado]: El estado del individuo
        @keyword [id]: El identificador del punto de control de origen.
        @keyword [x]: Coordenada x del dispositivo de origen.
        @keyword [y]: Coordenada y del dispositivo de origen.
        @keyword [edad]: La edad del individuo en horas
        """

        estado = kargs.get('estado', Estado.HUEVO);
        #~ Se inicializa el mosquito de acuerdo al estado.
        self.mosquito = None
        if estado == Estado.HUEVO :
            self.mosquito = Huevo()
        else :
            self.mosquito = Larva()

        #~ TODO : ver estado inicial para los individuos que provienen de
        #~ las larvitrampas
        self.coordenada_x = kargs.get('x', None);
        self.coordenada_y = kargs.get('y', None);

        self.id_dispositivo = kargs.get('id', None);
        self.index = kargs.get('index', None);

        self._id = Individuo.INDEX_IND
        Individuo.INDEX_IND += 1

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para
        alimentarse, reproducirse, protegerse y dispersarse.
        """
        return self.mosquito.esta_muerto();

    def desarrollar(self, hora) :
        """
        Se verifica si el individuo debe o no cambiar de estado segun su
        edad. El cambio de estado esta determinado de forma randomica
        bajo los siguientes parametros.
            Estado  Tiempo promedio
            huevo   2 a 3 dias
            larva   4 a 14 dias
            pupa    1 a 4 dias

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        self.mosquito = self.mosquito.desarrollar(hora)


    def se_reproduce (self, hora):
        """
        El apareamiento ocurre dentro de las 24 horas siguientes a la
        emergencia. Éste se realiza durante el vuelo, pero en algunas
        ocasiones se lleva a cabo en una superficie vertical u horizontal

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        """
        return self.mosquito.se_reproduce(hora)

    def poner_huevos(self, hora) :
        """

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return self.mosquito.poner_huevos(hora)

    def get_child (self):
        """
        Este método se encarga de obtener el hijo del inidividuo, el hijo
        hedea de su padre todos sus atributos.
        """
        return Individuo(x=self.coordenada_x, y=self.coordenada_y, \
                    id=self.id_dispositivo, index=self.index)


