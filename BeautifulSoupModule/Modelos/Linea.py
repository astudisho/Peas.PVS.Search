import datetime as dt

class Linea(object):
    def __init__(self):
        self.numero = ''
        self.nombrePlan = ''
        self.rentaMensual = -1
        self.fechaVencimiento = dt.date.today()
        self.fechaVencimientoText = ''
        self.fechaContratacion = dt.date.today()
        self.fechaContratacionText = ''
        self.plazoForzosoText = ''
        self.plazoForzoso = -1
        self.plazoForzosoTermino = False
    
    def __str__(self):
        return self.numero + ' ' + self.nombrePlan + ' ' + self.fechaVencimientoText

    def to_dict(self):
        return {
            "Numero": self.numero,
            "Nombre plan": self.nombrePlan,
            "Renta mensual": self.rentaMensual,
            "Fecha vencimiento": self.fechaVencimiento,
            "Fecha contratacion": self.fechaContratacion,
            "Plazo forzoso": self.plazoForzoso,
            "Plazo forzoso termino": self.plazoForzosoTermino
        }