class Table():

    def __init__(self, id='', fecha_hora_registro='', fecha_emision_comprobante='',nombre_aplicante='', lote='', nombre='', a_paterno='', a_materno='', f_nacimiento='', edad='', sexo='', alergias='', alergia_especifica='', fecha_ultima_vac_covid='', fecha_ultima_vac_influenza='', comprobante='',conformidad='', conformidad_vaxigrip='', telefono='', email='', calle='', num_ext='', colonia='', alcaldia='', cp='', aplicaVacunaCovid='', aplicaVacunaInfluenza='') -> None:
        self.id = id
        self.fecha_hora_registro = fecha_hora_registro
        self.fecha_emision_comprobante = fecha_emision_comprobante
        self.nombre_aplicante = nombre_aplicante
        self.lote = lote
        self.nombre = nombre
        self.a_paterno = a_paterno
        self.a_materno = a_materno
        self.f_nacimiento = f_nacimiento
        self.edad = edad
        self.sexo = sexo
        self.alergias = alergias
        self.alergia_especifica = alergia_especifica
        self.fecha_ultima_vac_covid = fecha_ultima_vac_covid
        self.fecha_ultima_vac_influenza = fecha_ultima_vac_influenza
        self.comprobante = comprobante
        self.conformidad = conformidad
        self.conformidad_vaxigrip = conformidad_vaxigrip
        self.telefono = telefono
        self.email = email
        self.calle = calle
        self.num_ext = num_ext
        self.colonia = colonia
        self.alcaldia = alcaldia
        self.cp = cp
        self.aplicaVacunaCovid = aplicaVacunaCovid
        self.aplicaVacunaInfluenza = aplicaVacunaInfluenza

    def to_dict(self):
        return {
            'id':self.id,
            'fecha_hora_registro': self.fecha_hora_registro,
            'fecha_emision_comprobante': self.fecha_emision_comprobante,
            'nombre_aplicante': self.nombre_aplicante,
            'lote': self.lote,
            'nombre' : self.nombre,
            'a_paterno' : self.a_paterno,
            'a_materno' : self.a_materno,
            'f_nacimiento': self.f_nacimiento,
            'edad' : self.edad,
            'sexo' : self.sexo,
            'alergias' : self.alergias,
            'alergia_especifica': self.alergia_especifica,
            'fecha_ultima_vac_covid': self.fecha_ultima_vac_covid,
            'fecha_ultima_vac_influenza': self.fecha_ultima_vac_influenza,
            'comprobante' : self.comprobante,
            'conformidad' : self.conformidad,
            'conformidad_vaxigrip' : self.conformidad_vaxigrip,
            'telefono' : self.telefono,
            'email' : self.email,
            'calle' : self.calle,
            'num_ext' : self.num_ext,
            'colonia' : self.colonia,
            'alcaldia' : self.alcaldia,
            'cp' : self.cp,
            'aplicaVacunaCovid': self.aplicaVacunaCovid,
            'aplicaVacunaInfluenza': self.aplicaVacunaInfluenza
        }