from flask import Flask,jsonify,request,make_response,Response
from solution.dna import hasMutation,NUM,listCounter
from connetion.db import get_dnas,get_stats,clean_blackboard,get_log,clean_log

app = Flask(__name__)

@app.route('/')
def get_tables():
    
    registros = get_dnas()

    return jsonify({"hola":registros})

@app.route('/clean')
def clean_Tables_Req():
    clean_blackboard()
    return jsonify({"":"tablas limpiadas"})

@app.route('/cleanLog')
def clean_Logs_Req():
    clean_log()
    return jsonify({"":"log borrado"})

@app.route('/registros')
def get_Logs_Req():
    return jsonify(get_log())

@app.route('/stats')
def get_Stats_Req():
    return jsonify(get_stats())

@app.route('/mutation',methods=['POST'])
def post_Mutation_Req():
    req_data = request.get_json(force=True)

    lista = req_data["dna"]

    validator = {"fail":False}

    for i in lista:
        for j in i:
            listCounter([0,0,0,0],j,0,validator,False)
            if validator["fail"]:
                return Response('{"respuesta":"Entrada no valida"}', status=403, mimetype='application/json')

    if hasMutation(lista):
        return Response('{"respuesta":"mutaciones encontradas -> '+str(NUM['val'])+'"}', status=200, mimetype='application/json')
    else:
        return Response('{"respuesta":"no posee mutaciones"}', status=403, mimetype='application/json')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(threaded=True, port=5000)