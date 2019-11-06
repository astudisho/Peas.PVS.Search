import datetime as dt

class Linea(object):
    def __init__(self):
        self.numero = ''
        self.nombrePlan = ''
        self.rentaMensual = -1
        self.fechaVencimiento = dt.date()
        self.fechaVencimientoText = ''
        self.fechaContratacion = dt.date()
        self.fechaContratacionText = ''
        self.plazoForzosoText = ''
        self.plazoForzoso = -1
    
    def __str__(self):
        return self.numero + ' ' + self.nombrePlan + ' ' + self.fechaVencimiento
