from utilidades import *
import math
import json
from paths import *

#constantes
SANA_DISTANCIA = 6
LARGO = 100 #30
ANCHO = 60 #15
PASO = 4
LIMITE = 8

ORIGENES = [[3,13],[3,7],[3,3],[13,3],[23,3],[23,7],[23,13],[13,13],[13,7]]

class AgentePlusPlus:
    def __init__(self, nombre = "X", infectado = False, vacunado = False, conmorbilidad = False):
        self.utilidades = Utilidades()
        # Atributos inicializados
        self.nombre = nombre
        self.suceptible = True  # en principio es suceptible a contagio
        self.asintomatico = False
        self.estadoEnfermo = False # Falso = leve, True = crítico
        self.infectado = infectado
        self.vacunado = vacunado
        self.conmorbolidad = conmorbilidad

        #atributos default
        self.deceso = False
        self.recuperado = False
        self.inmunidad = False
        self.tiempoEnfermo = 0
        self.tiempoInmunidad = 0
        
        self.pasos = []
        self.sentido_recto = 0 #0 -> X, 1-> -X, 2-> Y, 3-> -Y
        self.hubo_giro = False
        #posicion
        self.x = self.utilidades.get_random_from(0+PASO,LARGO-PASO)
        self.y = self.utilidades.get_random_from(0+PASO,ANCHO-PASO)

        if self.infectado: # and not self.vacunado:
            # A partir de si está infectado y no vacunado, se crea para ver si es asintomático o no
            self.asintomatico = self.utilidades.get_true_false()
            if self.asintomatico:
                # Si es asintomatico, obtener el estado de la enfermedad
                if self.conmorbolidad:
                    self.estadoEnfermo = True
            # Si self.asintomatico es falso, entonces self.estadoEnfermo será falso (leve)
            # Ahora obtener el tiempo que va a tener la enfermedad, por ahora será en rango de 5-12
            self.tiempoEnfermo = self.utilidades.get_random_days()
        #self.info()
        rutas = Paths()
        self.rutas_originales = rutas.get_god_list()
        self.punto_final = self.utilidades.get_random_from(0,8)
        self.punto_inicio = self.utilidades.get_random_from(0,8)

        caminos_punto = self.rutas_originales[self.punto_final]
        primer_info_camino = caminos_punto[self.utilidades.get_random_from(0,len(caminos_punto)-1)]
        puntos = primer_info_camino[2]
        primer_punto = puntos[0]

        #self.x = int(primer_punto[0])*4
        #self.y = int(primer_punto[1])*4

        #modo 2
        self.modo = 0
        self.offset = 0
        self.cuadrante = self.get_quadrant()
        print("position initial: ", self.x, " , ", self.y)

    def get_theta(self, punto_fin):
        temp_x = punto_fin[0] - self.x
        temp_y = punto_fin[1] - self.y
        theta = 0
        if temp_x != 0:
            theta = math.atan(temp_y/temp_x)
        print("theta: ", theta)
        sign_x = 1
        sign_y = 1

        if (punto_fin[0] < self.x and punto_fin[1] < self.y) or (punto_fin[0] < self.x and punto_fin[1] >= self.y) :
            sign_x = -1
            sign_y = -1

        # if punto_fin[0] >= self.x:
        #     sign_x = 1
        # else:
        #     sign_x = -1
        
        # if punto_fin[1] >= self.y:
        #     sign_y = -1
        # else:
        #     sign_y = 1
        
        return theta, sign_x, sign_y

    def get_point_in_quadrant(self, quadrant):
        x = 0
        y = 0
        if quadrant == 0:
            x = self.utilidades.get_random_from(5, 33)
            y = self.utilidades.get_random_from(40, 55)
        elif quadrant == 1:
            x = self.utilidades.get_random_from(5, 33)
            y = self.utilidades.get_random_from(20, 40)
        elif quadrant == 2:
            x = self.utilidades.get_random_from(5, 33)
            y = self.utilidades.get_random_from(5, 20)
        elif quadrant == 3:
            x = self.utilidades.get_random_from(33, 66)
            y = self.utilidades.get_random_from(5, 20)
        elif quadrant == 4:
            x = self.utilidades.get_random_from(66, 95)
            y = self.utilidades.get_random_from(5, 20)
        elif quadrant == 5:
            x = self.utilidades.get_random_from(66, 95)
            y = self.utilidades.get_random_from(20, 40)
        elif quadrant == 6:
            x = self.utilidades.get_random_from(66, 95)
            y = self.utilidades.get_random_from(40, 55)
        elif quadrant == 7:
            x = self.utilidades.get_random_from(33, 66)
            y = self.utilidades.get_random_from(40, 55)
        else:
            x = self.utilidades.get_random_from(33, 66)
            y = self.utilidades.get_random_from(20, 40)
        return x,y

    def get_quadrant(self):
        if 0 <= self.x <= 33:
            if 0 <= self.y <= 20:
                return 2
            elif 21 <= self.y <= 40:
                return 1
            else:
                return 0
        elif 34 <= self.x <= 66:
            if 0 <= self.y <= 20:
                return 3
            elif 21 <= self.y <= 40:
                return 8
            else:
                return 7
        else:
            if 0 <= self.y <= 20:
                return 4
            elif 21 <= self.y <= 40:
                return 5
            else:
                return 6

    def make_path_to_quadrant(self):
        cuadrante_fin = 0
        while True:
            cuadrante_fin = self.utilidades.get_random_from(0,8)
            self.cuadrante = self.get_quadrant()
            if cuadrante_fin != self.cuadrante:
                break
        #crear camino del punto de origen al 
        ## pedir un número de 0-2 para saber el camino que se va a usar
        tipo_camino = self.utilidades.get_random_from(0,1) #0,2
        # pedir un punto en el cuadrante fin
        fin_x, fin_y = self.get_point_in_quadrant(cuadrante_fin)
        print("cuadrante: ", self.cuadrante, " , cuadrante_fin: ", cuadrante_fin)
        print("punto actual: ", self.x, " , ", self.y)
        print("punto fin: ", fin_x, " , ", fin_y)
        temp_pasos = []
        if tipo_camino == 0:
            #directo
            distancia = math.sqrt(pow((self.x - fin_x),2) + pow((self.y - fin_y),2))
            theta, sign_x, sign_y = self.get_theta([fin_x, fin_y])
            for step in range(1, int(distancia)):
                tt_X = int((sign_x*step*math.cos(theta)) + self.x)
                tt_Y = int((sign_y*step*math.sin(theta)) + self.y)
                temp_pasos.append([tt_X, tt_Y])
        elif tipo_camino == 1:
            #paso positivo o negativo
            p_x = 1
            p_y = 1
            if fin_x >= self.x:
                p_x = 1
            else:
                p_x = -1
            if fin_y >= self.y:
                p_y = 1
            else:
                p_y = -1
            #componente x y y
            for paso_x in range(self.x, fin_x, p_x):
                temp_pasos.append([paso_x+1, self.y])
            for paso_y in range(self.y, fin_y, p_y):
                temp_pasos.append([fin_x, paso_y+1])
        else:
            #pasar, girar y regresar
            pass
        print("make_path_to_quadrant: ", tipo_camino)
        print(temp_pasos)
        return temp_pasos

    def info(self):
        print("{} \t ({:2d},{:2d}) \t\t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {}".format(self.nombre, self.x,self.y,self.asintomatico, self.estadoEnfermo, self.infectado, self.vacunado, self.conmorbolidad, self.deceso, self.recuperado, self.inmunidad, self.tiempoEnfermo, self.tiempoInmunidad))
        temp_dict = {
            "nombre": self.nombre,
            "posicion": str(self.x) + "," + str(self.y),
            "asintomatico": str(self.asintomatico),
            "estadoEnfermo": str(self.estadoEnfermo),
            "infectado": str(self.infectado),
            "vacunado": str(self.vacunado),
            "conmorbolidad": str(self.conmorbolidad),
            "deceso": str(self.deceso),
            "recuperado": str(self.recuperado),
            "inmunidad": str(self.inmunidad),
        }
        return temp_dict

        # print("Agente ",self.nombre, " en la posicion: ",self.x,",",self.y)
        # print("\t Asintomatico: ", self.asintomatico)
        # print("\t EstadoEnfermo: ", self.estadoEnfermo)
        # print("\t Infectado: ", self.infectado)
        # print("\t Vacunado: ", self.vacunado)
        # print("\t Conmorbolidad: ", self.conmorbolidad)
        # print("\t Deceso: ", self.deceso)
        # print("\t Recuperado: ", self.recuperado)
        # print("\t Inmunidad: ", self.inmunidad)

    # checar si está enfermo o esta inmune
    def tick(self):
        if self.deceso: #Si el agente ya es deceso, no se termina la funcion
            return

        if self.infectado:
            #checar si es grave, si sí, entonces obtener probabilidad de que muera
            if self.estadoEnfermo:
                if self.utilidades.get_true_false():
                    self.deceso = True
                    print("El agente: ",self.nombre, " ha muerto!")
                    self.infectado = False
                    self.tiempoEnfermo = 0
                    self.asintomatico = False
                    self.estadoEnfermo = False
                    return
            # restar tiempo enfermo
            if self.tiempoEnfermo > 0:
                self.tiempoEnfermo -= 1
            else:
                #poner recuperado y obtener tiempo de inmunidad
                self.infectado = False
                self.inmunidad = True
                self.tiempoInmunidad = self.utilidades.get_random_days()
                print("El agente: ",self.nombre, " ahora tiene inmunidad de: ", self.tiempoInmunidad)
        elif self.inmunidad:
            if self.tiempoInmunidad > 0:
                self.tiempoInmunidad -= 1
            else:
                self.inmunidad = False
                self.suceptible = True
                print("El agente: ",self.nombre, " ha perdido inmunidad")

    def get_position(self):
        return self.x, self.y
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    # def move(self):
    #     if self.deceso: #Si el agente ya es deceso, no se termina la funcion
    #         return

    #     move_x = -PASO if self.utilidades.get_true_false() else PASO
    #     move_y = -PASO if self.utilidades.get_true_false() else PASO
    #     if 0 <= self.x + move_x <= LARGO-5 and 0 <= self.y + move_y <= ANCHO-5:
    #         self.set_position(self.x + move_x, self.y + move_y)

    def set_straight_way(self):
        pasos = self.utilidades.get_random_from(4,8)
        for cont in range(1, pasos):
            if self.sentido_recto == 0:
                #X
                if self.x + cont*PASO <= LARGO-LIMITE:
                    self.pasos.append([self.x + cont*PASO, self.y])
            elif self.sentido_recto == 1:
                #-X
                if 0 <= self.x - cont*PASO:
                    self.pasos.append([self.x - cont*PASO, self.y])
            elif self.sentido_recto == 2:
                #Y
                if self.y + cont*PASO <= ANCHO-LIMITE:
                    self.pasos.append([self.x, self.y + cont*PASO])
            elif self.sentido_recto == 3:
                #-Y
                if 0 <= self.y - cont*PASO:
                    self.pasos.append([self.x, self.y - cont*PASO])

    def move(self):
        #print("move-", self.nombre)
        if self.deceso: #Si el agente ya es deceso, no se termina la funcion
            return

        #si la lista está vacia, entonces llenarlar
        if len(self.pasos) == 0:
            #print("call make_path_to_quadrant: ", self.nombre)
            #obtener los caminos del punto final
            """caminos_punto = self.rutas_originales[self.punto_final]
            primer_info_camino = caminos_punto[self.utilidades.get_random_from(0,len(caminos_punto)-1)] #aqui despues va a ser un random dependiendo del numero de caminos_punto
            puntos = primer_info_camino[2]
            self.punto_inicio = primer_info_camino[0]
            self.punto_final = primer_info_camino[1]
            self.pasos = puntos"""
            self.pasos = self.make_path_to_quadrant()

        if len(self.pasos) > 0:
            temp_list = self.pasos.pop(0)
            #self.set_position(int(temp_list[0])*4, int(temp_list[1])*4)
            #print("move-",self.nombre," : ", temp_list[0], " , ", temp_list[1])
            self.set_position(int(temp_list[0]), int(temp_list[1]))

    # def move(self):
    #     if self.deceso: #Si el agente ya es deceso, no se termina la funcion
    #         return

    #     #si la lista está vacia, entonces llenarlar
    #     if len(self.pasos) == 0:
    #         if self.hubo_giro:
    #             self.hubo_giro = False
    #             #llenar con sentido recto
    #             self.set_straight_way()
    #         else:
    #             self.sentido_recto = self.utilidades.get_random_from(0,3)
    #             #pedir sentido
    #             direccion = self.utilidades.get_direction()
    #             pasos = 0
    #             if direccion == "cen":
    #                 self.set_straight_way()
    #             else:
    #                 self.hubo_giro = True
    #                 if self.sentido_recto == 0:
    #                     if self.x + PASO <= LARGO-LIMITE and self.y + PASO <= ANCHO-LIMITE:
    #                         self.pasos.append([self.x + PASO, self.y + PASO])
                        
    #                     if self.x + 2*PASO <= LARGO-LIMITE:
    #                         self.pasos.append([self.x + 2*PASO, self.y + PASO])
    #                 elif self.sentido_recto == 1:
    #                     if self.x + PASO <= LARGO-LIMITE and 0 <= self.y - PASO:
    #                         self.pasos.append([self.x + PASO, self.y - PASO])
                        
    #                     if 0 <= self.y - 2*PASO:
    #                         self.pasos.append([self.x + PASO, self.y - 2*PASO])
    #                 elif self.sentido_recto == 2:
    #                     if 0 <= self.x - PASO and 0 <= self.y - PASO:
    #                         self.pasos.append([self.x - PASO, self.y - PASO])
                        
    #                     if 0 <= self.x - 2*PASO:
    #                         self.pasos.append([self.x - 2*PASO, self.y - PASO])
    #                 elif self.sentido_recto == 3:
    #                     if 0 <= self.x - PASO and self.y + PASO <= ANCHO-LIMITE:
    #                         self.pasos.append([self.x - PASO, self.y + PASO])
                        
    #                     if self.y + 2*PASO <= ANCHO-LIMITE:
    #                         self.pasos.append([self.x - PASO, self.y + 2*PASO])
        
    #     if len(self.pasos) > 0:
    #         temp_list = self.pasos.pop(0)
    #         self.set_position(temp_list[0], temp_list[1])

    def set_infected(self, nombre):
        if self.inmunidad:
            return

        self.estadoEnfermo = False
        self.asintomatico = self.utilidades.get_true_false()
        if not self.asintomatico:
                # Si es asintomatico, obtener el estado de la enfermedad
                if self.conmorbolidad:
                    self.estadoEnfermo = True
        self.tiempoEnfermo = self.utilidades.get_random_days()
        self.infectado = True
        print("El paciente ", self.nombre, " es infectado con estado asintomatico ", self.asintomatico, " con tiempo: ", self.tiempoEnfermo, " por: ", nombre)

    #checar si no esta infectado y no esta vacunado, preguntar por la distancia y si es menor
    # a la permitida, entonces poner a infectado al agente, con todo lo que conlleva (estado y tiempo) 
    def search_around(self, agentes):
        for agente in agentes:
            if not self.infectado and not self.vacunado and self.nombre != agente.nombre and not agente.deceso and not self.deceso and agente.infectado:
                distance = self.euclidean_distance(agente)
                if distance < SANA_DISTANCIA:
                    self.set_infected(agente.nombre)

    # def search_around(self, agentes):
    #     for agente in agentes:
    #         distance = self.euclidean_distance(agente)
    #         if distance < SANA_DISTANCIA:
    #             if not self.infectado and not self.vacunado and self.nombre != agente.nombre:
    #                 self.set_infected()
    #             else:
    #                 print("NO INFECTADO")
                    

    def euclidean_distance(self, agente):
        agente_x, agente_y = agente.get_position()
        d = math.sqrt(pow((self.x - agente_x),2) + pow((self.y - agente_y),2))
        #print("euclidean distance: ", d)
        return d

        

        
