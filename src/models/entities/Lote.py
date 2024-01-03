class Lote:
    
    def __init__(self, id_lote, numero_lote):
        self.id_lote = id_lote
        self.numero_lote = numero_lote

    def to_dict(self):
        return {
            "id_lote": self.id_lote,
            "numero_lote": self.numero_lote
        }