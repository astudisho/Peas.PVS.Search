from bs4 import BeautifulSoup
import re

telefonoTdId = 'telefonopacambio'
planTdText = 'Nombre del Plan:'

tableInfoPlanId = 'tableInfoPlan'
vencimientoTableText = 'Fecha de Vencimiento:'

class NumeroParser(object):
    def __init__(self, fileName = '4421970772.html'):
        f = open(fileName,'r')
        self.dom = f.read()
        f.close()
        pass

    def parseNumero(self):
        soup = BeautifulSoup(self.dom, 'lxml')

        tableInfoPlan = soup.find(id=tableInfoPlanId)
        tableInfoPlanTr = tableInfoPlan.find_all('tr')
        
        numeroRaw = self.removeAllNewLines(tableInfoPlanTr[1].getText())
        plan = self.removeAllNewLines(tableInfoPlanTr[6].getText())
        rentaMensualRaw = self.removeAllNewLines(tableInfoPlanTr[9].getText())
        numero = self.getNumeroFromRaw(rentaMensualRaw)



        vencimientoTable = soup.find('td',string=vencimientoTableText).parent.parent

        vencimientoTableTr = vencimientoTable.find_all('tr')

        fechaVencimientoRaw = self.removeAllNewLines(vencimientoTableTr[0].getText())
        fechaContratacionRaw = self.removeAllNewLines(vencimientoTableTr[1].getText())
        plazoForzosoRaw = self.removeAllNewLines(vencimientoTableTr[2].getText())
        terminaContrato = self.removeAllNewLines(vencimientoTableTr[3].getText())

        pass

    def removeAllNewLines(self, text):
        return text.strip().replace('\n','').replace('\r','')

    def getNumeroFromRaw(self,text):
        return re.match(r'\d{3,4}\.\d{2}',text)

if __name__ == "__main__":
    parser = NumeroParser()
    parser.parseNumero()