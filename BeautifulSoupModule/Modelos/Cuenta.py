class Cuenta(object):
    def __init__(self, 
                numCuenta, 
                nombres, 
                apellidos, 
                rfc,
                sexo,
                tipoPersona,
                telefonos,
                direccionFiscal, 
                direccionEnvio,
                tipoCliente,
                fechaCorte,
                facturas,
                activa):

        self.numeroCuenta = numCuenta
        self.representanteLegal = RepresentanteLegal(nombres, apellidos, sexo)
        self.rfc = rfc
        self.tipoPersona = tipoPersona
        self.telefonos = telefonos.split()
        self.direccionFiscal = direccionFiscal
        self.direccionEnvio = direccionEnvio
        self.tipoCliente =  tipoCliente
        self.fechaCorte = fechaCorte
        self.facturas = facturas
        self.activa = activa
        
        pass

    def to_dict(self):
        return{
            "Numero cuenta": self.numeroCuenta,
            "Razon social": self.representanteLegal.nombreCompleto,
            "Sexo": self.representanteLegal.sexo,
            "RFC": self.rfc,
            "Tipo persona": self.tipoPersona,
            "Telefono": self.telefonos[0] if any(self.telefonos) else "No disponible",
            "Direccion fiscal": self.direccionFiscal,
            "Ultima factura": str(self.facturas[0] if any(self.facturas) else "" ),
            "Activa": self.activa
        }

class Factura(object):
    def __init__(self,fecha,monto):
        self.fecha = fecha
        self.monto = monto

    def __str__(self):
        return str(self.fecha) + ' ' + self.monto

    def __repr__(self):
        return "Factura(fecha:{}, monto:{})".format(self.fecha, self.monto)

class RepresentanteLegal(object):
    def __init__(self, nombres, apellidos, sexo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.nombreCompleto = nombres +  apellidos
        self.sexo = sexo

    def __str__(self):
        return '{} {}'.format(self.nombreCompleto, self.sexo)

    def __repr__(self):
        return 'RepresentanteLegal(NombreCompleto:{}, Sexo:{})'.format(self.nombreCompleto, self.sexo)