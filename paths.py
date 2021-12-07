import csv

RUTAS = ["static/paths/rutas-0.csv", "static/paths/rutas-1.csv", "static/paths/rutas-2.csv"
        , "static/paths/rutas-3.csv", "static/paths/rutas-4.csv", "static/paths/rutas-5.csv"
        , "static/paths/rutas-6.csv", "static/paths/rutas-7.csv", "static/paths/rutas-8.csv"]

class Paths:
    def __init__(self):
        self.god_list = []
        for archivo in RUTAS:
            with open(archivo) as file:
                reader = csv.reader(file)
                granma_list = []
                mother_list = []
                temp_list = []
                for row in reader:
                    if row[0] == '':
                        mother_list.append(temp_list)
                        temp_list = []
                    elif row[0] == 'X':
                        pass
                    else:
                        temp_list.append(row)
                mother_list.append(temp_list)
                temp_list = []
                #crear lista con punto de inicio y final
                for way in mother_list:
                    temp_list.append(self.get_point_start_end(way[0]))
                    temp_list.append(self.get_point_start_end(way[len(way)-1]))
                    temp_list.append(way)
                    granma_list.append(temp_list)
                    temp_list = []
                #print("granma list")
                #print(granma_list)
            self.god_list.append(granma_list)
        #print("god list")
        #print(self.god_list)


        #print("mother list")
        #print(mother_list)
    
    def get_god_list(self):
        return self.god_list

    
    def get_point_start_end(self, point):
        #print("get_point_start_end: ", point)
        if point[0] == "3":
            if point[1] == "3":
                return 2
            elif point[1] == "7":
                return 1
            elif point[1] == "13":
                return 0
            else:
                return 0
        elif point[0] == "13":
            if point[1] == "3":
                return 3
            elif point[1] == "7":
                return 8
            elif point[1] == "13":
                return 7
            else:
                return 0
        elif point[0] == "23":
            if point[1] == "3":
                return 4
            elif point[1] == "7":
                return 5
            elif point[1] == "13":
                return 6
            else:
                return 0
