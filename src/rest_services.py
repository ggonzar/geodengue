#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify
from controller import *
from pdi import *
import traceback

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
    print "rest"
    return ""

@app.errorhandler(500)
def internal_error(error):
    print error
    return "500 error "+ str(error), 500

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

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
    resp, muestras_evol = gis.method_evolutive()
    print "parsing"
    layer_name = gis.to_geoserver(resp, col, row, "evol")
    return jsonify(layer=layer_name, mosquitos=str(muestras_evol))

@app.route('/pdi_img', methods=['POST'])
def pdi_img():

    print "Metodo"
    print request.method
    print "el file!"
    f = request.files['file']
    print "6- " +str(f)
    f.save("data/file.jpeg")
    cantidad = pdi.cantidad_contornos()
    return jsonify(json=cantidad)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
