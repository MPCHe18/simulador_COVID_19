from flask import Flask, render_template, request, flash
from flask.json import jsonify
import random
from controlador import *

app = Flask(__name__)

controlador = None

@app.route('/', methods=['POST','GET'])
def home():
    return render_template('principal.html')

@app.route('/sendInfo', methods=['POST','GET'])
def getInfo():
    global controlador
    #print("Entra a sendInfo")
    if request.method == 'POST':
        #print("Es un POST")
        request_data2 = str(request.data)
        request_data = request_data2[3:-2]
        parts = request_data.split(",")
        #print("Data", request_data)
        #Obtener los datos del json
        numAgentes = parts[0].split(":")[1]
        numAgentes = numAgentes[1:-1]
        NumInfectados = parts[1].split(":")[1]
        NumInfectados = NumInfectados[1:-1]
        NumVacunados = parts[2].split(":")[1]
        NumVacunados = NumVacunados[1:-1]
        NumComorbilidades = parts[3].split(":")[1]
        NumComorbilidades = NumComorbilidades[1:-1]
        NumTiempo = parts[4].split(":")[1]
        NumTiempo = NumTiempo[1:-1]
        #NumTiempo = NumTiempo[:-1]
        print("numAgentes: ",numAgentes)
        print("NumInfectados: ",NumInfectados)
        print("NumVacunados: ",NumVacunados)
        print("NumComorbilidades: ",NumComorbilidades)
        print("NumTiempo: ",NumTiempo)
        controlador = Controlador(int(numAgentes), int(NumInfectados), int(NumVacunados), int(NumComorbilidades))
        #return jsonify(estado="creado")
        return controlador.showInfoAgentes()

@app.route('/tick', methods=['POST','GET'])
def getTick():
    global controlador
    if request.method == 'GET':
        print("GET Tick")
        res = controlador.tick()
        #convertir a json
        return res
        #return json.dumps(res)
##Incio del servidor
if __name__ == '__main__':
    app.run(debug = False)