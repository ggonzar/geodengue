#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify
from controller import *

"""
Este modulo define la interfaz de los servicios rest.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se inicializa la api rest
app = Flask(__name__)

@app.route('/', methods=['GET'])
def api_root():
    """Path por defecto de los servicios"""
    return ""

@app.route('/muestras/<muestra>/instantanea', methods=['POST'])
def interpolate_idw(muestra):
    gis = GisController(muestra);
    col= row = 300
    resp = gis.method_idw(col, row);
    print "parsing"
    layer_name = gis.to_geoserver(resp, col, row, "inst")
    return jsonify(layer=layer_name)


@app.route('/muestras/<muestra>/evolucionar', methods=['POST'])
def evolutive(muestra):
    col= row = 300
    gis = GisController(muestra);
    print "starting..."
    resp = gis.method_evolutive()
    print "parsing"
    layer_name = gis.to_geoserver(resp, col, row, "evol")
    return jsonify(layer=layer_name)


if __name__ == '__main__':
    app.run(debug=True)
