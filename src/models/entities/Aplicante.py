class Aplicante:
    
    def __init__(self, id_aplicante, nombre_completo_aplicante):
        self.id_aplicante = id_aplicante
        self.nombre_completo_aplicante = nombre_completo_aplicante

    def to_dict(self):
        return {
            "id_aplicante": self.id_aplicante,
            "nombre_completo_aplicante": self.nombre_completo_aplicante
        }