
/**
 * Este workspace abarca las clases que manejan las capas pertenecientes
 * al mapa.
 * @namespace
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name common.Layer
 */
Layer = {
    /**
     * Construye el Stratergy tipo Save que es aplicado a las capas
     * del tipo vector.
     * @class
     *
     * @name common.Layer.StrategySave
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @return {OpenLayers.Strategy.Save}
     */
    StrategySave : function(){
        return  new OpenLayers.Strategy.Save({
            onCommit: function(response) {
                if(!response.success() && this.failure){
                    this.failure();
                    return;
                }else if(this.success){
                    this.success(response);
                }

                this.layer.refresh();
            }
        });
    },

    /**
     * Construye el protocolo WFS para obtener una capa.
     * @class
     *
     * @name common.Layer.Protocol
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param options {Object}
     * @config {String} layerName El nombre de la capa
     * @config {String} service El nombre del servicio (wfs o ows).
     * @config {String} geometyName El nombre de la columna que contiene
     *              el geometry del layer.
     * @config {OpenLayers.Layer.Filter} [filter] el filtro utilizado para acotar
     *              los datos.
     * @config {String} [featureNS] la url del workspace en el que se
     *              encuentra el layer.
     * @return {OpenLayers.Protocol.WFS}
     */
    Protocol : function(options){
        var params = {
            url:  DataSource.host + service,
            version: "1.1.0",
            //featureNS : DataSource.workspace,
            featureType: options.layerName,
            geometryName: options.geometryName,
            srsName: DataSource.projectionCode
        };
        if(options["featureNS"]){
            params['featureNS'] = options.featureNS;
        }

        if(options["filter"]){
            params['filter'] = options.filter;
        }
        return new  OpenLayers.Protocol.WFS(options);
    },

    /**
     * Crea una capa del tipo vector, del servidor y del workspace
     * definidos en las vairables host y workspace.
     * @class
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @name common.Layer.Vector
     * @param options {Object}
     * @config {String} layerName El nombre de la capa
     * @config {String} [geometyName] El nombre de la columna que contiene
     *              el geometry del layer.
     * @config {OpenLayers.Filter} [filter] el filtro utilizado para acotar
     *              los datos.
     * @config {String} [featureNS] La url del workspace en el que se
     *              encuentra el layer.
     * @config {Function} [callback] Función que es invocada cuando se
     *               obtiene los datos del layer.
     * @return {OpenLayers.Layer.Vector} La capa del tipo vector construida.
     */
    Vector : function(options){
        if(!options["geometryName"] && !options["featureNS"]){
            return new OpenLayers.Layer.Vector(options.layerName,
                    {displayInLayerSwitcher: false});
        }
        //se construye el strategy
        var params = {};
        //se copian los atributos
        $.extend(params, options);
        //se establece el servicio
        params.service = "ows";
        var fixed = new OpenLayers.Strategy.Fixed();
        var strategySave =  new Layer.StrategySave();
        //se construye el protocolo
        var protocol = null;
        protocol = new Layer.Protocol(options)

        if(params['callback']){
            protocol.read({
                callback: params['callback']
            });
        }

        //Se construye la capa del tipo vector
        return new OpenLayers.Layer.Vector(layerName,
            {
                strategies : [fixed, strategySave],
                protocol: protocol,
                /**
                 * Se encarga de confirmar los cambios realizados en las capas.
                 * @function
                 * @name common.Layer.Vector#commit
                 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
                 * @param options {Object}
                 * @config {Function} [success] Función que se invoca cuando
                 *              la operacion se realizó correctamente
                 * @config {Function} [failure] Función que es invocada
                 *              cuando ocurrio un error al realizar la operación.
                 */
                commit : function(options){
                    if(options){
                        this.strategies[1]["success"] = options.success;
                        this.strategies[1]["failure"] = options.failure;
                    }
                    this.strategies[1].save();
                },
                displayInLayerSwitcher: false
            }
        );
    },

    /**
     * Obtiene las capas del servidor mediante el protocolo WMS.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @params options {Object}
     * @config {Array} names Un array con los nombres de las capas a construir
     * @config {OpenLayers.Filter} [filter] Un filtro para acotar la capa
     * @config {Boolean} [base] Establece si es o no una capa base
     * @return {Array} La lista de capas WMS obtenidas.
     */
    WMS : function(options){
        //direccion del servidor al cual se le realizan las peticiones de las
        //capas via WMS
        var server = DataSource.host + "wms";
        //var server = DataSource.host + "gwc/service/wms";
        //formato en el que el servidor retorna el mapa
        var format = 'image/png';
        // nombre de las capas que se solicitan al servidor
        var layers = [];
        options.transparent = true;
        options.format = format;
        if(options["filter"]){
            var filter_1_1 = new OpenLayers.Format.Filter({version: "1.1.0"});
            var xml = new OpenLayers.Format.XML();
            options['filter'] = xml.write(filter_1_1.write(options.filter));
        }
        if(!options["base"]){
            options.base =false;
        }
        var names = options.names;
        // se construyen las capas
        for(var i=0; i<names.length; i++){
            var name = names[i].name;
            options['layers'] = name;
            layers[i] = new OpenLayers.Layer.WMS(
                name, server, options, {attribution:""});

            layers[i].transitionEffect = 'resize';
            layers[i].isBaseLayer = options.base;
        }
        //se retorna las capas
        return layers;
    }

};
