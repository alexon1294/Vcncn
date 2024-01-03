class Comprobante:
    
    def __init__(self, id_comprobante, nombre_cliente, a_paterno_cliente, a_materno_cliente, nombre_completo_aplicante, lote, fecha_emision, id_cliente, id_aplicante, id_lote):
        self.id_comprobante = id_comprobante
        self.nombre_cliente = nombre_cliente
        self.a_paterno_cliente = a_paterno_cliente
        self.a_materno_cliente = a_materno_cliente
        self.nombre_completo_aplicante = nombre_completo_aplicante
        self.lote = lote
        self.fecha_emision = fecha_emision
        self.id_cliente = id_cliente
        self.id_aplicante = id_aplicante
        self.id_lote = id_lote

    def to_dict(self):
        return {
            "id_comprobante": self.id_comprobante,
            "nombre_cliente": self.nombre_cliente,
            "a_paterno_cliente": self.a_paterno_cliente,
            "a_materno_cliente": self.a_materno_cliente,
            "nombre_completo_aplicante":self.nombre_completo_aplicante,
            "lote":self.lote,
            "fecha_emision":self.fecha_emision,
            "id_cliente":self.id_cliente,
            "id_aplicante":self.id_aplicante,
            "id_lote":self.id_lote,
        }