#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que representa los objetos bases que son
utilizados para realizar las operaciones correspondientes.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

class Bounds :
    """
    Clase para representar la extensión de los puntos. La extensión de se
    encuentra compuesta por un conjunto de puntos
        x_min : El minimo valor de x
        x_max : El máximo valor de x
        y_min : El minimo valor de y
        y_max : El máximo valor de y
    """

    def __init__(self, x_min=0, x_max=0, y_min=0, y_max=0):
        self.x_min = x_min;
        self.y_min = y_min;
        self.x_max = x_max;
        self.y_max = y_max;

    def parse_array (self, x_array, y_array):
        """
        Este método se encarga de obtener el par de valores min y max
        correspondiente a cada array y setear los valores a los atributos
        de la clase.

        @type  x_array : Array
        @param x_array : Lista de puntos correspondientes al eje x

        @type  y_array : Array
        @param y_array : Lista de puntos correspondientes al eje y
        """
        self.x_min = x_array.min();
        self.y_min = y_array.min();
        self.x_max = x_array.max();
        self.y_max = y_array.max();


import numpy

class Grid :
    """
    Clase para representar la grilla de puntos en 3 dimensiones (x,y,z). Un
    grilla esta compuesta por n puntos.
    """
    def __init__ (self, x=[], y=[], z=[]) :
        self.x = x;
        self.y = y;
        self.z = z;

    def get_bounds(self):
        """
        Este método se encarga de obtener la extensión de la grilla de
        puntos.

        @rtype  : Bounds
        @return : La extensión de la grilla de puntos.
        """
        bounds = Bounds();
        bounds.parse_array(self.x, self.y);
        return bounds;

    def gen_grid (self, cols, rows) :
        """
        Este método se encarga de generar un grid con `col*rows` puntos.
        Los puntos generados son equidistantes entre sí.

        @type  cols : Integer
        @param cols : La cantidad de columnas del nuevo grid.

        @type  rows : Integer
        @param rows : La cantidad de filas del nuevo grid.

        @rtype  : Grid
        @return : La grilla generada con los nuevos puntos.

        """
        bounds = self.get_bounds();
        xi = numpy.linspace(bounds.x_min, bounds.x_max, cols);
        yi = numpy.linspace(bounds.y_min, bounds.y_max, rows);
        #genera la matriz de coordenadas
        xi, yi = numpy.meshgrid(xi, yi)
        # Copia los subarrays en un un array de una dimensión
        xi, yi = xi.flatten(), yi.flatten();
        #se retorna el nuevo grid generado.
        return Grid(xi, yi);

    def distanceTo(self,grid):
        """
        Calcula la distancia entre los puntos pertenecientes a grilla
        actual y la grilla especificada.

        @type  grid : Grid
        @param grid : La grilla de puntos entre la que se

        @rtype ndarray
        @return La matriz de distancia entre la grilla de puntos.
        """
        obs = numpy.vstack((self.x, self.y)).T
        interp = numpy.vstack((grid.x, grid.y)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = numpy.subtract.outer(obs[:,0], interp[:,0])
        d1 = numpy.subtract.outer(obs[:,1], interp[:,1])
        #Given the “legs” of a right triangle, return its hypotenuse.
        return numpy.hypot(d0, d1)
