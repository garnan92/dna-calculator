from flask import Flask,jsonify,request,make_response,Response
from Solucion.DNA import hasMutation,NUM,ContadorValores
from Conexion.DB import GET_DNAS,GET_STATS,CLEAN_BLACKBOARD,GET_LOG,CLEAN_LOG

app = Flask(__name__)

@app.route('/')
def get_tables():
    
    registros = GET_DNAS()

    return jsonify({"hola":registros})

@app.route('/clean')
def clean_tables():
    CLEAN_BLACKBOARD()
    return jsonify({"":"tablas limpiadas"})

@app.route('/cleanLog')
def clean_Logs():
    CLEAN_LOG()
    return jsonify({"":"log borrado"})

@app.route('/registros')
def get_registros():
    return jsonify(GET_LOG())

@app.route('/stats')
def get_stats_req():
    return jsonify(GET_STATS())

@app.route('/mutation',methods=['POST'])
def post_table_data():
    req_data = request.get_json(force=True)

    lista = req_data["dna"]

    validator = {"discrepancia":False}

    for i in lista:
        for j in i:
            ContadorValores([0,0,0,0],j,0,validator)
            if validator["discrepancia"]:
                return Response('{"respuesta":"Entrada no valida"}', status=403, mimetype='application/json')

    if hasMutation(lista):
        return Response('{"respuesta":"mutaciones encontradas -> '+str(NUM['val'])+'"}', status=200, mimetype='application/json')
    else:
        return Response('{"respuesta":"no posee mutaciones"}', status=403, mimetype='application/json')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(threaded=True, port=5000)