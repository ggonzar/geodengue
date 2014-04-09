#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este módulo contiene la definición del proceso evolutivo de los puntos
de control.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

#Se impotan los modulos.


from poblacion import *
#log de eventos
from logger import EventLogger

class Simulador :
    """
    El proceso de evolución de las muestras consiste en un proceso, en el
    cual las muestras obtenidas mediante los dispositivos de ovipostura son
    expuestas a un conjunto de variaciones en un periodo de tiempo. Las
    variaciones que, principalmente, afectan a las muestras son :

    * Las variaciones del clima en dicho periodo : Se someten las muestras
        obtenidas a las distintas variaciones climáticas ocurridas en el
        periodo de tiempo seleccionado para el estudio.

    * La naturaleza del mosquito : Cada elemento de la muestra, es sometido
        a cambios considerando la naturaleza del mosquito. Los aspectos que
        se tienen en cuenta son su ciclo de vida del mosquito, ciclo
        reproductivo y el desplazamiento.

    """


    def __init__ (self, **kargs) :
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        self.zonas_table = RankingTable();
        #~ se inicializa el atributo periodo
        self.poblacion = Poblacion(kargs);
        #~ se inicializa el atributo periodo
        self.historial_clima =[]
        #~ se inicializa el atributo periodo
        self.periodo = kargs.get('periodo',[])

        # se inicializa la clase que hace log de los eventos
        self.logger = EventLogger('event_log_')


    def start(self):
        """
        Se encarga de iniciar el simulador.
        """
        init_dic = self.stats()
        i=0
        total_huevos = 0;
        huevos_muertas = 0;
        larvas_muertas = 0;
        pupas_muertas = 0;
        adultos_muertas = 0;
        olimpia = True
        OBS = -1
        args = {}
        for hora in self.periodo.dias :
            #~ se procesa cada individuo de la población
            j=0
            nueva_poblacion = []
            print "Día Nro :" + str(i) + " poblacion :" + str(len(self.poblacion.individuos))

            for individuo in self.poblacion.individuos :
                poner_huevos = False
                cantidad_huevos = 0
                #~ if individuo.id_mosquito ==308  :
                    #~ print 10*"="
                    #~ print individuo
                    #~ print 10*"="
                #~ Se desarrolla el inidividuo
                individuo.desarrollar(hora)
                #~ Se verifica el estado del individuo
                if self.poblacion.regular(individuo, hora, i) :
                    """
                    si el individuo esta muerto se lo remueve de la poblacion
                    """
                    if individuo.estado == Estado.LARVA :
                        larvas_muertas += 1
                    elif individuo.estado == Estado.PUPA :
                        pupas_muertas += 1
                    elif individuo.estado == Estado.ADULTO:
                        adultos_muertas += 1
                    else :
                        huevos_muertas += 1

                    self.poblacion.kill(individuo)

                elif individuo.esta_maduro() == True:
                    """
                    si el individuo esta maduro, se realiza el cambio de
                    estado.
                    """
                    #~ print  "\tCamibar de estado "+  str(individuo)
                    individuo = self.poblacion.cambiar_estado(individuo)
                    self.poblacion.individuos[j] = individuo

                elif individuo.estado == Estado.ADULTO :
                    if(individuo.se_reproduce(hora) == True \
                        and olimpia == False) :
                        #~ se genera un nueva poblacion
                        sub_poblacion = self.poblacion.ovipostura(individuo)
                        """
                        se extiende la poblacion unicamente si se puso
                        huevos.
                        """
                        if len(sub_poblacion) > 0 :
                            cantidad_huevos = len(sub_poblacion)
                            print "Huevos " + str(cantidad_huevos)
                            nueva_poblacion.extend(sub_poblacion)

                #~ args['individuo'] = individuo
                #~ args['hora'] = hora.hora
                #~ args['dia'] = str(i)
                #~ args['temperatura'] = hora.temperatura
                #~ args['pone_huevos'] = poner_huevos
                #~ args['cantidad_huevos'] = cantidad_huevos

                # log de eventos
                #~ self.logger.to_csv( args )
                #~ fin del preiodo
                j += 1
            #~ fin del preriodo
            if len(nueva_poblacion) > 0 :
                print "Pone " + str(len(nueva_poblacion)) +" huevos"
                total_huevos += len(nueva_poblacion)
                self.poblacion.extend(nueva_poblacion)
            i+= 1


        print 'Poblacion inicial'
        for k in init_dic.keys() :
            print( 'nro de ' + str(k) + ' = ' + str(init_dic[k]))

        print 'Poblacion final'
        out_dic = self.stats()
        for k in out_dic.keys() :
            print( 'nro de ' + str(k) + ' = ' + str(out_dic[k]))

        print "Total de huevos generados : "+ str(total_huevos)
        print "Total huevos muertos : "+ str(huevos_muertas)
        print "Total larvas muertas : "+ str(larvas_muertas)
        print "Total pupas muertas : "+ str(pupas_muertas)
        print "Total adultos muertos : "+ str(adultos_muertas)

    def to_grid (self):
        """
        Este método se encarga de traducir la población de inidviduos
        a un grid interpolable.

        Los adultos no son incluidos en el conteo de individuos.
        """
        key_map = {}
        data_array = []
        max_cantidad = 0
        for individuo in self.poblacion.individuos :
            point = individuo.posicion
            key = str(point.x) + "-" + str(point.y)
            if not key_map.has_key(key) \
                and individuo.estado != Estado.ADULTO :
                # se obtiene los datos
                data = {}
                data['x'] = point.x
                data['y'] = point.y
                data['id'] = 0
                #~ data['index'] = individuo.index
                data['cantidad'] = 1
                #se añade el elemento al array
                data_array.append(data)
                # se añade el indice al array
                key_map[key] = len(data_array) -1
            elif individuo.estado != Estado.ADULTO :
                index = key_map[key]
                # se incrementa la cantidad de larvas
                data_array[index]['cantidad'] += 1
        #ajustar las escala de valores para tener cantidades en el rango
        #de 0 a 80
        #~ for data in data_array :
            #~ data['cantidad'] = \
                #~ float(data['cantidad'])*float(80.0/max_cantidad)

        print 'cantidad de puntos a interpolar: ' + str(len(data_array))

        #orden por coordenada
        print "sort por coordenada..."
        swapped = True
        while swapped :
            swapped = False
            for i in range(1, len(data_array)) :
                comp1 = (data_array[i-1]['x'], data_array[i-1]['y'])
                comp2 = (data_array[i]['x'], data_array[i]['y'])
                if self.compare_coordinates(comp1, comp2) > 0 :
                    aux = data_array[i-1]
                    data_array[i-1] = data_array[i]
                    data_array[i] = aux
                    swapped = True

        # se realiza el parse a grid
        grid = Grid();
        grid.parse(data_array)

        # se retorna la referencia al grid
        return grid;

    def compare_coordinates( self, p1, p2 ) :
        """
        Metodo para comparar 2 puntos
        @param p1, p2
        array puntos
            ej> p1 = (x1, y1)
        """
        if float(p1[0]) == float(p2[0]) :
            return float(p1[1]) - float(p2[1])
        else :
            return float(p1[0]) - float(p2[0])

    def stats( self ) :
        """
        Metodo para analizar el comportamiento global de la pobacion
        Tomando en cuenta la poblacion inicial se analiza durante un periodo
        de tiempo
            cantidad de hembras y machos
            cantidad de individuos en el estado huevo
            cantidad de individuos en el estado larva
            cantidad de individuos en el estado pupa
            cantidad de individuos en el estado adulto
        """
        #~ inicializamos el diccionario con los valores que contabilizaremos
        stats_dic = {}
        stats_dic['huevo'] = 0
        stats_dic['larva'] = 0
        stats_dic['pupa'] = 0
        stats_dic['adulto'] = 0

        for individuo in self.poblacion.individuos :
            if individuo.estado == Estado.HUEVO :
                stats_dic['huevo'] += 1
            elif individuo.estado == Estado.LARVA :
                stats_dic['larva'] += 1
            elif individuo.estado == Estado.PUPA :
                stats_dic['pupa'] += 1
            else :
                stats_dic['adulto'] += 1

        return stats_dic

if __name__ == "__main__" :
    from db_manager import *
    from models import *
    from tutiempo import *

    id_muestras = 1;
    #se obtiene el historial climatico
    print "obteniendo los datos climaticos"
    clima = TuTiempo("Asuncion")
    periodo = clima.get_periodo()

    print "obteniendo los datos de la bd"
    dao = PuntosControlModel()
    data = dao.get_by(id_muestras);
    print "construyendo la grilla"
    #~ print data

    evol = Simulador(periodo=periodo, poblacion=data)

    print "iniciando simulación"
    evol.start()
    """
    for ind in evol.poblacion :
        print str(ind)
    """
    evol.to_grid()
