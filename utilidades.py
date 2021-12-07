import random

class Utilidades:
    def __init__(self):
        self.partes = 0

    def get_true_false(self):
        return random.choice([True, False])
    
    def get_enabled_feature(self, contador, total, index, numAgent):
        restantes = numAgent - index - 1
        faltan = total - contador
        if(faltan < restantes):
            return self.get_true_false()
        else:
            return True
    
    def get_random_days(self):
        return random.randint(5,12)
    
    def get_random_from(self, inicio, final):
        return random.randint(inicio, final)
    
    def get_direction(self):
        return random.choice(["izq", "cen", "der"])
    
    def get_step(self):
        return random.randint(1, 5)
