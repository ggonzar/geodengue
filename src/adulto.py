#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estado Adulto

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from aaegypti import *


class Adulto(AeAegypti) :
    """
    ECOLOGÍA DEL ADULTO
    Emergencia
    Luego de emerger de la pupa, el insecto se posa sobre las paredes del
    recipiente durante varias horas hasta el endurecimiento de sus alas y
    su exoesqueleto.

    Apareamiento
    Dentro de las 24 h, después de la emergencia, puede ocurrir el apareamiento.
    El macho es atraído por el sonido emitido por el batir de las alas de la
    hembra durante el vuelo.

    Alimentación
    Las hembras se alimentan de la mayoría de vertebrados, pero prefieren
    a los humanos, vuelan en sentido contrario al viento y son atraídas por
    los olores y gases del hombre. La sangre sirve para el desarrollo de
    los huevos.

    Ciclo gonadotrófico
    Después de cada alimentación se desarrolla un lote de huevos. Si la
    hembra completa su alimentación sanguínea (2-3 mg) desarrollará y
    pondrá 100-200 huevos, el intervalo dura de dos a tres días. La hembra
    grávida buscará recipientes oscuros o sombreados para depositar sus
    huevos, prefiriendo aguas limpias y claras.

    Rango de vuelo
    La hembra no sobrepasa los 50-100 m durante su vida (puede permanecer
    en la misma casa donde emergió). Si no hay recipientes, una hembra
    grávida puede volar tres kilómetros para poner sus huevos. Los machos
    se dispersan menos que las hembras.

    Conducta de reposo
    Descansan en lugares sombreados como alcobas, baños, patios o cocinas.
    Se les captura sobre ropas colgadas, debajo de muebles, toallas, cortinas
    y mosquiteros.

    Longevidad
    Los adultos pueden permanecer vivos en el laboratorio durante meses y
    en la naturaleza pocas semanas. Con una mortalidad diaria de 10 %, la
    mitad de los mosquitos morirán durante la primera semana y 95 % en el
    primer mes.

    Fuente : http://scielo.sld.cu/scielo.php?pid=S0864-34662010000100015&script=sci_arttext
    """

    @property
    def ultima_oviposicion (self):
        """
        Cantidad de horas desde la última oviposición.
        """
        return self._ultima_oviposicion;

    @property
    def cantidad_oviposicion (self):
        """
        Cantidad de veces que el mosquito hembra ovipuso.
        """
        return self._cantidad_oviposicion

    @property
    def ultimo_alimento (self):
        """
        Tiempo transcurrido desde la ultima alimentación.
        """
        return self._ultimo_alimento;

    @property
    def cantidad_alimentacion (self):
        """
        Porcentaje no digerido de la última alimentación.
        """
        return self._cantidad_alimentacion;

    @property
    def se_alimenta( self ):
        """
        Boolean que determina si se alimento o no
        """
        return self._se_alimenta

    @property
    def distancia_recorrida (self):
        """
        La distancia en metros recorrida por el mosquito adulto.
        """
        return self._distancia_recorrida;

    @property
    def is_inseminada (self):
        """
        True si la hembra fue inseminada, False en caso contrario.
        """
        return self._is_inseminada;

    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El sexo de la pupa a partir del cual evoluciono a adulto.
        @keyword [position]: El punto que determina la ubiación de la pupa
        """
        # se invoca al constructor de la clase padre.
        kargs['estado'] = Estado.ADULTO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,**kargs);
        #~ print "new "+ str(self)
        self._ultima_oviposicion = 1
        self._ultimo_alimento = 1
        self._distancia_recorrida = 0
        self._cantidad_oviposicion = 0
        self._cantidad_alimentacion = 0
        self._is_inseminada = False
        self._se_alimenta = False
        self._se_reproduce = False

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

        self._se_reproduce = self.is_inseminada == True \
            and self.esta_muerto() == False \
            and self.sexo == Sexo.HEMBRA \
            and hora.get_tipo_clima() != Clima.FRIO
            #~ and (hora.get_tipo_hora == Horario.TARDE_NOCHE \
                #~ or hora.get_tipo_hora == Horario.NOCHE ) \

        return self._se_reproduce

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.

        adulto  si expectativa de vida <= 0, si edad >= 30 dias.

        * Muchos mueren al momento de emerger
        * Si la población emergente original es grande, la restante es suficiente
          para transmitir la enfermedad y mantener o provocar una epidemia (Nelson,1986).
        """
        return self.expectativa_vida <= 0

    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado adulto

        El tiempo de vida restante de un mosquito adulto depende de la
        calidad de su zona, el clima y su capacidad de alimentarse

        Cómo le afecta la temperatura : Limitantes para el desarrollo poblacional.
        Entre ellos, dentro del ambiente abiótico el potencial del vector

        Variable atmosférica    Valor umbral letal  Duración letal (días)
        Déficit de saturación       >30 mb              2
        Déficit de saturación       entre 25 y 30 mb    3
        Déficit de saturación       entre 20 y 25 mb    5
        Déficit de saturación       entre 15 y 20 mb    10
        Temperatura máxima          > 40 oC             1
        Temperatura mínima          < 0 oC              1

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        cantidad_dias = self.get_expectativa_zona(hora)
        #~ se calcula el promedio de días que puede vivir el adulto
        self._tiempo_vida += cantidad_dias

        if (cantidad_dias > 0 ) :
            #~ se disminuye la expectativa de vida del adulto
            self._expectativa_vida -= 100/(cantidad_dias * 24)

        #~ se envejece el adulto
        self._edad +=1

        if not hora.get_tipo_clima() == Clima.FRIO :
            self.buscar_alimento(hora)

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

        * La alimentación y la postura ocurren principalmente durante el día
        * Existe una mayor actividad en las primeras horas de haber amanecido,
         a media mañana, a media tarde o al anochecer.
        *  La hembra embarazada es capaz de volar hasta 3km en busca de un
         sitio optimo para la ovipostura.
        * Los machos suelen dispersarse en menor magnitud que las hembras.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        rank = self.rank_zona()
        self.inseminacion(hora)
        """
        Permanece físicamente en donde emergió, siempre y cuando no
        halla algún factor que la perturbe o no disponga de huéspedes,
        sitios de reposo y de postura. El alcance noral es de 100 metros.

        En caso de no haber recipientes adecuados, la hembra grávida
        es capaz de volar hasta tres kilómetros en busca de este sitio.
        Los machos suelen dispersarse en menor magnitud que las hembras
        """
        self._ultimo_alimento += 1
        #~ el mosquito se alimenta por primera vez de 20 a 72 horas
        p = randint(20, 72)

        if rank == Zonas.MALA or rank == Zonas.PESIMA:
            self.volar(hora)

        elif (hora.get_tipo_hora() == Horario.MADUGRADA_MANHANA \
            or hora.get_tipo_hora() == Horario.TARDE_NOCHE) \
            and self._se_alimenta == False \
            and p % (self.edad + 1 ) == 0:

                self._se_alimenta = True
                self._ultimo_alimento = 0
                """
                2-3 mg = 20-30 cg
                """
                self._cantidad_alimentacion += randint(0, MAX_ALIMENTACION)

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

        El mosquito hembra necesita la sangre para obtener proteínas y
        poner sus huevos.

        La mayoría de las posturas ocurre cerca del crepúsculo.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        huevos = 0
        #~ se obtiene el ciclo gonotrofico
        ciclo_gonotrofico = self.get_ciclo_gonotrofico(hora)
        # se aumenta el contador de ultima oviposición
        self._ultima_oviposicion += 1

        #~ se realizan los controles de las condiciones
        if self.ultima_oviposicion >= ciclo_gonotrofico \
            and self.cantidad_alimentacion >= 10:

            huevos = self.generar_huevos()
            self._se_alimenta = False
            self._cantidad_alimentacion = 0
            self._cantidad_oviposicion +=1

        return huevos

    def inseminacion (self, hora):
        """
        Inseminación :
        *  Antes de 24 horas ambos sexos están listos para el apareamiento
        *
        * El macho es atraído por el sonido emitido de las alas de la hembra durante
          el vuelo.
        * La inseminación,generalmente, se efectúa durante el vuelo.
        * Una vez alimentada de sangre ocurren pocos apareamientos.
        """
        p = randint(1, 24)
        if (hora.get_tipo_hora() == Horario.MADUGRADA_MANHANA \
            or hora.get_tipo_hora() == Horario.TARDE_NOCHE) \
            and p <= self.edad:

            if self.sexo == Sexo.MACHO :
                #~ buscar a hembras para inseminarse
                self.inseminar_macho(hora)
            else :
                self.inseminar_hembra(hora)

    def inseminar_macho (self, hora) :
        """
        Buscar hembras para inseminar
        """
        pass

    def inseminar_hembra (self, hora) :
        """
        Se encarga de verificar el estado de las hembras y verificar si
        estas pueden ser insemindadas.

        Sólo las hembras nulíperas son insemindandas debido a que una
        inseminación es suficiente para que la hembra pueda poner huevos
        toda su vida.

        TODO : Se debe verificar si existe algun macho cerca para poder
        realizar la inseminación.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        @return True si se puede inseminar a la hembra, False en caso
            contrario.
        @rtype Boolean
        """

        porcentaje =  randint(1, 100)
        #~ Para las hembras nulíperas (no ha puesto ningún huevo)
        if self.cantidad_oviposicion == 0  \
            and self._cantidad_alimentacion == 0\
            and porcentaje <= 58 \
            and self.is_inseminada == False :
                """
                El 58% son inseminadas antes de su primera alimentación
                sanguínea.
                """
                self._is_inseminada = True
                return True

        elif  self.cantidad_oviposicion == 0 \
            and porcentaje <= 17 \
            and self.se_alimenta == True  \
            and self.is_inseminada == False :
                """
                El 17% durante durante la alimentación
                """
                self._is_inseminada = True
                return True

        elif  self.cantidad_oviposicion <= 1 \
            and self.se_alimenta == True  \
            and porcentaje <= 25 :
                """
                El 25% es inseminada entre la segunda alimentación y la
                primera oviposición.
                """
                self._is_inseminada = True
                return True;
        """
        Una inseminación es suficiente para fecundar todos los huevos que
        la hembra produzca en toda su vida. Por lo que no es es relevante
        las inseminaciones posteriores a la primera debido que se busca
        'habilitar' la hembra para que ponga huevos.
        """
        return False

    def get_ciclo_gonotrofico (self, hora) :
        """
        El ciclo gonotrófrico de los mosquitos es el nombre que se le
        adjudico al período que existe desde que el mosquito chupa la
        sangre- ovopostura- hasta que vuelve a alimentarse.

        Consiste en la absorción de sangre, seguido de la digestión, la
        maduración de los oocytos y la oviposición. El tiempo para la
        digestión de sangre y su consecuente producción de huevos varía
        de 3 a 5 días dependiendo de la temperatura ambiental.
        La temperatura influye en la duración de la digestión y el desarrollo
        de los ovarios, ya que cuando las temperaturas son bajas la digestión
        tarda más tiempo.
        """
        if hora.get_tipo_clima() == Clima.FRIO :
            return randint (96, 120)

        elif hora.get_tipo_clima() == Clima.FRESCO :
            return randint (72, 96)

        elif hora.get_tipo_clima() == Clima.NORMAL :
            return randint (48, 96)

        elif hora.get_tipo_clima() == Clima.CALIDO :
            return randint (48, 72)

        elif hora.get_tipo_clima() == Clima.CALUROSO :
            return randint (48, 72)

    def generar_huevos (self) :
        """
        Su ciclo para poner huevos es de aproximadamente cada tres días a
        cuatro días.

        Una alimentación escasa produce menos huevos por lote y si es muy
        reducida no se producen huevos.

        Este metodo se encarga de generar una cantidad aleatoria de huevos.
        Un solo mosquito hembra puede poner 80 a 150 huevos, cuatro veces
        al día.
        """
        huevos = self.cantidad_alimentacion * MAX_HUEVOS / MAX_ALIMENTACION
        # se reinicia el contador
        self._ultima_oviposicion = 0;

        return huevos

    def volar(self, hora) :
        """
        Los machos rondan como voladores solitarios aunque es más común
        que lo hagan en grupos pequeños (Bates, 1970; Kettle, 1993) atraídos
        por los mismos huéspedes vertebrados que las hembras.

        Vuelan en sentido contrario al viento, desplazándose mediante lentas
        corrientes de aire, siguen los olores y gases emitidos por el
        huésped (CO2), al estar cerca utilizan estímulos visuales para
        localizarlo mientras sus receptores táctiles y térmicos las guían
        hacia el sitio donde se posan.

        Por lo general, la hembra de Ae. aegypti no se desplaza más allá de
        5,000 m de distancia de radio de vuelo en toda su vida, permanece
        físicamente en donde emergió, siempre y cuando no halla algún factor
        que la perturbe o no disponga de huéspedes, sitios de reposo y de
        postura. En caso de no haber recipientes adecuados, la hembra grávida
        es capaz de volar hasta tres kilómetros en busca de este sitio.
        Los machos suelen dispersarse en menor magnitud que las hembras

        En un ensayo de laboratorio, con viento en calma mosquitos
        Ae. aegypti se desplazan a 17 cm/s, al introducir viento en contra
        de 33 cm/s, incrementaron su velocidad para contrarrestarle disminuyendo
        su avance a 16 cm/s, lo que implica un esfuerzo de desplazamiento
        como si hubieran volado a 49 cm/s, por consiguiente volar con
        viento de mayor velocidad le representa un mayor esfuerzo y suelen
        hacerlo (Kettle, 1993).
        """
       #~ se genera un angulo 'delta', para simular las corrientes de aire
        #~ que sigue el mosquito.
        delta = randint(-45, 45)
        #~ Vuelan en sentido contrario al viento
        angulo_vuelo = hora.direccion_viento + 180 + delta
        #~ se calcula la velocidad de vuelo
        velocidad = self.velocidad_vuelo(hora, angulo_vuelo);
        """
        Como la velocidad de vuelo esta en m/h y el tiempo de estudio
        es 1 hora, se utiliza la velocidad como distancia a recorrer

        distancia = Xo + Velocidad * Tiempo = Velocidad * 1h

        """
        #~ print "Vel : "+str(velocidad)
        self.posicion.move(velocidad, angulo_vuelo)

    def move_to_neighbors (self, hora) :
        """
        Este método se encarga de evaluar el vecino inmediato y comparalo
        con el valor de la posicion actual, si el vecino posee un puntaje
        mayor que el puntaje actual retorna true.

        En caso de no haber recipientes adecuados, la hembra grávida
        es capaz de volar hasta tres kilómetros en busca de este sitio.
        Los machos suelen dispersarse en menor magnitud que las hembras

        Son muchos los factores que afectan el vuelo de los mosquitos:

        1. disponibilidad de sitios resguardados del sol,
        2. disponibilidad de vegetación y fuentes de néctar,
        3. ubicación, cantidad y disponibilidad de sitios de cría,
        4. dirección del viento,
        5. lluvias,
        6. urbanización,
        7. fuentes para la ingesta de sangre
        8. estado del mosquito: recién emergido, hembras grávidas, edad,
            nivel de alimentación, etc.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        @return True si el vecino posee una mayor puntación, False en caso
            contrario.
        @rtype Boolean
        """
        #~ se evalua la zona
        rank = self.rank_zona()
        #~ se verifica el estado de la zona
        if rank == Zonas.MALA or rank == Zonas.PESIMA :
            return True

        return False

    def velocidad_vuelo(self, hora, angulo_vuelo) :
        """
        Al volar en busca de sangre, la hembra bate sus alas de 250 a 600
        veces/segundo, ello depende de la especie y en menor grado de su
        velocidad que puede llegar ser de 2 km por hora.

        Aedes albopictus
        TOP SPEED (FLYING) :  2km/h

        The Anopheles mosquito can fly for up to four hours continuously
        at 1–2 km/h ,traveling up to 12 km (7.5 mi) in a night.
        """

        speed = randint(1000, 2000)
        wind_speed = hora.viento

        """
        Se calcula la velocidad resultante medinte algebra de vectores.

        vx = sen(180 - angulo_vuelo) * speed + wind_speed
        vy = cos(180 - angulo_vuelo) * speed
        v = sqrt (Vx^2 + Vy^2 )
        """
        vx = math.sin(180 - angulo_vuelo) * speed - wind_speed
        vy = math.cos(180 - angulo_vuelo) * speed
        v = math.sqrt (vx**2 + vy**2 )

        return  v
