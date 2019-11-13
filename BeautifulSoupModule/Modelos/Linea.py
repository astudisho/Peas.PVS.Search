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
