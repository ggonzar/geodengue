#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición de datos utilizados en el simulador.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
import math
#Se impotan los modulos.
from ranking_table import *
from models import *
from huevo import *
from larva import *
from pupa import *
from adulto import *

class Poblacion:
    ID = 0
    """

    """
    @property
    def memory(self) :
        """Tabla en memoria"""
        return self.__memory

    @memory.setter
    def memory(self, value):
        self.__memory = value

    @property
    def individuos(self) :
        """Array de individuos de la población"""
        return self.__individuos

    @individuos.setter
    def individuos(self, value):
        self.__individuos = value

    @property
    def total_huevos(self) :
        """Total de huevos generados"""
        return self.__total_huevos

    @total_huevos.setter
    def total_huevos(self, value):
        self.__total_huevos = value

    def __init__ (self, args) :
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        self.__memory = {}
        self.__individuos =  [];
        self.zonas_table = RankingTable();
        self.__total_huevos = 0;
        if args.has_key("poblacion") == True:
            self.generar_poblacion(args["poblacion"])

    def gen_sub_poblacion(self, **kargs):
        """
        """
        cantidad_larvas = kargs.get('cantidad_larvas', 0)
        clazz = kargs.get('clazz', Huevo)
        posicion = kargs.get('posicion', Point(kargs))
        sub_poblacion = []
        # se inicializa la población
        self.new_grupo(posicion=posicion, cantidad=cantidad_larvas);

        for cantidad in range(cantidad_larvas) :
            indv = clazz(posicion=posicion, zonas=self.zonas_table)
            # id del mosquito
            indv._id_mosquito = Poblacion.ID
            Poblacion.ID += 1
            #~ se añade el individuo a la sub población
            sub_poblacion.append(indv)

        return sub_poblacion

    def generar_poblacion (self, data ):
        """
        Este método se encarga de procesar los datos de las muestras y
        generar los inidividuos para inicializar la población.

        """
        grid = Grid()
        grid.parse(data)
        for i in range(len(grid)):
            # se obtine la cantidad de individuos
            cantidad_larvas = int(grid.z[i]);
            #~ se genera la sub población de larvas
            sub_poblacion = self.gen_sub_poblacion(\
                cantidad_larvas=cantidad_larvas,\
                clazz=Larva,\
                x=grid.x[i], y=grid.y[i])
            self.individuos.extend(sub_poblacion)

    def cambiar_estado (self, aedes) :
        """
        Se encarga de realizar el cambio de estado para el individuo de
        acuerdo a su estado actual.
        """

        grupo = self.get(aedes.posicion)
        if grupo == None :
            print aedes

        Clazz = {
            "HUEVO" : Larva,
            "LARVA" : Pupa,
            "PUPA" : Adulto
        }

        next_state = {
           "HUEVO" : Estado.LARVA,
            "LARVA" : Estado.PUPA,
            "PUPA" : Estado.ADULTO
        }
        #~ Se actualizan los individuos
        grupo[aedes.estado]["cantidad"] -= 1;
        grupo[next_state[aedes.estado]]["cantidad"] += 1;

        return Clazz[aedes.estado](sexo=aedes.sexo,posicion=aedes.posicion,\
                    zonas=self.zonas_table, id=aedes.id_mosquito)

    def gen_key (self, punto):
        """
        Genera una clave única para el punto
        """
        return str(punto.x) + "-" + str(punto.y)

    def new_grupo (self, **kargs) :
        """
        """
        estados = [Estado.HUEVO, Estado.LARVA, Estado.PUPA, Estado.ADULTO];
        grupo = {};
        punto = kargs.get('posicion', Point(kargs));
        key = self.gen_key(punto)
        if self.memory.has_key(key):
            return self.memory[key]

        for estado in estados :
            grupo[estado] = {};
            grupo[estado]["cantidad"] = 0;
            grupo[estado]["to_kill"] = 0;
            grupo[estado]["periodo"] = -1;
            grupo[estado]["killed"] = 0;

        cantidad = kargs.get('cantidad', 0);
        estado = kargs.get('estado', Estado.LARVA);
        grupo[estado]["cantidad"] = cantidad;
        self.memory[key] = grupo;
        return grupo

    def get(self, punto) :
        """
        Se ecarga de verificar si la zona ya fue rankeada, de ser así
        se retorna el valor de la tabla de zonas rankeadas. Si no fue
        rankeada se rankea la zona y se guarda en la tabla de ranking.
        """
        key = self.gen_key(punto)
        if not self.memory.has_key(key) :
            return None

        return self.memory[key]

    def kill (self, aedes) :
        """
        """
        self.individuos.remove(aedes);
        grupo = self.get(aedes.posicion)
        if grupo != None :
            grupo[aedes.estado]["cantidad"] -= 1
            grupo[aedes.estado]["to_kill"] -= 1
            grupo[aedes.estado]["killed"] += 1;

    def regular (self, aedes, dia, periodo) :
        """
        """
        if aedes.estado == Estado.ADULTO :
            grupo = self.get(aedes.posicion_origen)
        else :
            grupo = self.get(aedes.posicion)

        grupo_estado = grupo[aedes.estado];
        if grupo_estado["periodo"] < periodo :
            # se actualiza el periodo
            grupo_estado["periodo"] = periodo
            #se calcula la tasa de mortalidad del individuo
            tasa_mortalidad = aedes.mortalidad(dia.temperatura);
            cantidad = grupo_estado["cantidad"]
            """
            se actualiza la canitdad de inviduos que deben desaparecer
            en el periodo.
            """
            grupo_estado["to_kill"] = math.ceil(cantidad * tasa_mortalidad);

        return grupo_estado["to_kill"] > 0


    def ovipostura (self, adulto, dia):
        """
        """
        huevos = adulto.poner_huevos(dia)
        self.total_huevos +=  huevos;
        sub_poblacion = self.gen_sub_poblacion(posicion=adulto.posicion,\
                cantidad_larvas=huevos)

        return sub_poblacion

    def extend (self, nueva_poblacion) :
        """
        """
        self.individuos.extend(nueva_poblacion)

    def __str__ (self) :
        resumen = {}
        estados = [Estado.HUEVO, Estado.LARVA, Estado.PUPA, Estado.ADULTO];
        for estado in estados :
            resumen[estado] = {};
            resumen[estado]["total"] = 0;
            resumen[estado]["muertas"] = 0;

        for key in self.memory :
            for estado in self.memory[key] :
                resumen[estado]["total"] += self.memory[key][estado]["cantidad"]
                resumen[estado]["muertas"] += self.memory[key][estado]["killed"]

        to_str = "Huevos Generados : " + str(self.total_huevos) +"\n"
        for estado in estados :
            to_str +=  str(estado) + " total :" + str(resumen[estado]["total"]) + "\n"
            to_str +=  str(estado) + " muertas :" + str(resumen[estado]["muertas"]) + "\n"

        return to_str
