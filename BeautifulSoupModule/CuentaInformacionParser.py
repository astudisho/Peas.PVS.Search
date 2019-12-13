from bs4 import BeautifulSoup
import re
from dateutil import parser as duParser
import BeautifulSoupModule.Modelos
from datetime import date, datetime, timedelta

mesesDiccionario = {
    'Ene': 1,
    'Feb': 2,
    'Mar': 3,
    'Abr': 4, 
    'May': 5, 
    'Jun': 6,
    'Jul': 7, 
    'Ago': 8,
    'Sep': 9,
    'Oct': 10, 
    'Nov': 11,
    'Dic': 12
}

tablaInfoCuentaId = 'table_infoGeneralCuenta'
saldoTableXPath = '//*[@id="BORDE"]/tbody/tr/td[2]/table[2]'
facturaTableXpath = '#BORDE > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr > td > table > tbody > tr:nth-child(8) > td > table'

class CuentaParser(object):
    def __init__(self, dom):
        self.dom = dom
        self.soup = BeautifulSoup(dom, 'lxml')

    def __call__(self):
        facturas = []
        tablaFacturas = self.soup.select_one(facturaTableXpath)
        trFacturas = tablaFacturas.find_all('tr')

        for factura in trFacturas:
            fechaRaw = CuentaParser.removeAllNewLines(factura.td.text)
            fechaFactura = CuentaParser.getDateFromText(fechaRaw)
            monto =  CuentaParser.removeAllNewLines(factura.td.next_sibling.next_sibling.text)

            facturas.append(BeautifulSoupModule.Modelos.Factura(fechaFactura, monto))            

        tablaInformacion = self.soup.find(id = tablaInfoCuentaId)
        trs = tablaInformacion.find_all('tr')

        numCuenta =  CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[0].text))
        nombres = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[2].text))
        apellidos = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[3].text))
        rfc = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[4].text))
        sexo = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[6].text))
        tipoPersona = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[7].text))
        telefonos = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[9].text))
        direccionFiscal = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[10].text)) #Dejar los espacios
        direccionEnvio = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[11].text)) #Dejar los espacios
        tipoCliente = CuentaParser.getValorDelimitado(CuentaParser.removeAllNewLines(trs[12].text))
        cuentaActiva = CuentaParser.isCuentaActive(facturas[0].fecha)

        cuenta = BeautifulSoupModule.Modelos.Cuenta(numCuenta, nombres, apellidos, rfc, sexo, tipoPersona, telefonos, direccionFiscal, direccionEnvio, tipoCliente, '',facturas, cuentaActiva)
        return cuenta
        #BeautifulSoupModule.Modelos.Cuenta()
        pass

    @staticmethod
    def removeAllNewLines(text):
        return text.strip().replace('\n','').replace('\r','').replace('\t','')

    @staticmethod
    def getValorDelimitado(texto ,delimitador = ':'):
        return texto.partition(delimitador)[2]

    @staticmethod
    def getDateFromText(text):
        strings = text.split(' ')
        mes = mesesDiccionario[strings[2]]
        ano = int(strings[4])

        return date(ano, mes, 1)

    @staticmethod
    def isCuentaActive(fechaFactura):
        now = datetime.now().date()
        
        delta = now - fechaFactura

        return delta < timedelta(days=62)