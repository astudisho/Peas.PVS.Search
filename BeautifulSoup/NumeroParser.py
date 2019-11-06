from bs4 import BeautifulSoup
import re
from dateutil import parser as duParser
from '..\Modelos\Linea' import Linea

telefonoTdId = 'telefonopacambio'
planTdText = 'Nombre del Plan:'

tableInfoPlanId = 'tableInfoPlan'
vencimientoTableText = 'Fecha de Vencimiento:'

regexPlan = r'\d{3,4}'
regexRenta = r'\d{3,4}\.00'
regexNumero = r'\d{10}'
regexPlazo = r'\d{2}'

class NumeroParser(object):
    def __init__(self, fileName = '4421970772.html', debug = False):
        import os
        print(os.getcwd())
        f = open(fileName,'r')
        self.dom = f.read()
        f.close()
        pass

    def parseNumero(self):
        soup = BeautifulSoup(self.dom, 'lxml')
        linea = Linea()

        tableInfoPlan = soup.find(id=tableInfoPlanId)
        tableInfoPlanTr = tableInfoPlan.find_all('tr')
        
        #Asigna el numero a una variable y lo parsea
        numeroRaw = self.removeAllNewLines(tableInfoPlanTr[1].getText())
        numero = re.search(regexNumero, numeroRaw).group()
        linea.numero = numero

        #Asigna el plan como string y parsea la renta mensual
        plan = self.removeAllNewLines(tableInfoPlanTr[6].getText())
        linea.nombrePlan = plan

        #Busca el plan y lo parsea
        rentaMensualRaw = self.removeAllNewLines(tableInfoPlanTr[9].getText())
        rentaMensual =  re.search(regexRenta, rentaMensualRaw).group()
        linea.rentaMensual = rentaMensual

        #numero = self.getNumeroFromRaw(rentaMensualRaw)

        #Asigna la tabla como raiz a la variable
        vencimientoTable = soup.find('td',string=vencimientoTableText).parent.parent
        #Asigna los TR de la tabla como raiz a la variable
        vencimientoTableTr = vencimientoTable.find_all('tr')

        #Toma el texto de los tr que corresponden a cada valor y los parsea
        #Fecha vencimiento
        fechaVencimientoRaw = self.removeAllNewLines(vencimientoTableTr[0].getText())
        fechaVencimientoValor = self.getValorDelimitado(fechaVencimientoRaw)
        fechaVencimiento = duParser.parse(fechaVencimientoValor)

        linea.fechaVencimientoText = fechaVencimientoValor
        linea.fechaVencimiento = fechaVencimiento

        #Fecha de contratacion
        fechaContratacionRaw = self.removeAllNewLines(vencimientoTableTr[1].getText())
        fechaContratacionValor = self.getValorDelimitado(fechaContratacionRaw)
        fechaContratacion = duParser.parse(fechaContratacionValor)
        
        linea.fechaContratacionText = fechaContratacionValor
        linea.fechaContratacion = fechaContratacion

        #Plazo forzoso
        plazoForzosoRaw = self.removeAllNewLines(vencimientoTableTr[2].getText())
        plazoForzosoText = self.getValorDelimitado(plazoForzosoRaw)
        plazoForsozo = re.search(regexPlazo, plazoForzosoRaw).group()

        linea.plazoForzoso = plazoForsozo
        linea.plazoForzosoText = plazoForzosoText

        #Termino contrato
        terminaContratoRaw = self.removeAllNewLines(vencimientoTableTr[3].getText())        
        terminaContrato = self.removeAllNewLines(self.getValorDelimitado(terminaContratoRaw))

        

        pass

    def removeAllNewLines(self, text):
        return text.strip().replace('\n','').replace('\r','')

    def getNumeroFromRaw(self,text):
        return re.match(r'\d{3,4}(\.\d{2})?',text)

    def getValorDelimitado(self, texto ,delimitador = ':'):
        return texto.partition(delimitador)[2]

if __name__ == "__main__":
    parser = NumeroParser()
    parser.parseNumero()