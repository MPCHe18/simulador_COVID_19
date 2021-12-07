from AgentePlusPlus import *
from utilidades import *
import json
from paths import * 

class Controlador:
    def __init__(self, numAgentes = 5, numInfectados = 2, numVacunados = 3, numComorbilidades = 2):
        self.utilidades = Utilidades()
        #contadores para crear los agentes
        contInfectados = 0
        contVacunados = 0
        contComorbilidades = 0

        #lista de agentes
        self.listaAgentes = []

        #Corroborar que numInfectados + numVacunados = numAgentes
        if numAgentes < numInfectados:
            #regresar error
            print("Error  creando Controlador")
            return

        #Crear los agentes
        for index in range(0,numAgentes):
            featureInfectado = False
            featureVacunado = False
            featureComorbilidad = False
            #checar
            if contInfectados < numInfectados:
                featureInfectado = self.utilidades.get_enabled_feature(contInfectados, numInfectados, index, numAgentes)
                if featureInfectado:
                    contInfectados += 1
            
            if contVacunados < numVacunados:
                featureVacunado = self.utilidades.get_enabled_feature(contVacunados, numVacunados, index, numAgentes)
                if featureVacunado:
                    contVacunados += 1
            
            if contComorbilidades < numComorbilidades:
                featureComorbilidad = self.utilidades.get_enabled_feature(contComorbilidades, numComorbilidades, index, numAgentes)
                if featureComorbilidad:
                    contComorbilidades += 1
            
            #crear al agente y agregarlo a la lista
            #nombre = "X", infectado = False, vacunado = False, conmorbilidad = False
            self.listaAgentes.append(AgentePlusPlus(str(index), featureInfectado, featureVacunado, featureComorbilidad))

            #prueba paths
            paths = Paths()

    def getAgentes(self):
        return self.listaAgentes
    
    def move(self):
        for agente in self.listaAgentes:
            agente.move()
    
    def showInfoAgentes(self):
        infoJson = {}
        print("Agente \t Pos \t\t\t Asi \t Est \t Inf \t Vac \t Con \t Dec \t Rec \t inm \t T.E \t T.I")
        for agente in self.listaAgentes:
            info = agente.info()
            infoJson[agente.nombre] = info
        print("\n")
        return infoJson
    
    def tick(self):
        self.move()
        temp_list = []
        for agente in self.listaAgentes:
            agente.tick()
            agente.search_around(self.listaAgentes)
            temp_list.append(agente)
        self.listaAgentes = temp_list
        # cont = 0
        # while cont < len(self.listaAgentes):
        #     temp_list = self.listaAgentes.copy()
        #     self.listaAgentes[cont].tick()
        #     self.listaAgentes[cont].search_around(temp_list)
        #     cont += 1
        res = self.showInfoAgentes()
        #Aqui deberia regresar el diccionario de diccionarios
        return res

    
    def return_json(self):
        pass