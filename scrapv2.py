from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
#from selenium.webdriver import *
#import pandas as pd
from bs4 import BeautifulSoup
import time

timeout = 6
timeoutContenido = 30
sleepForSwitch = 0.1
sleepForReload = 0.3

#Data variables
loginUser = "D303433012"
loginPassword = "Guadalajara9506"

#Selectors
#"//img[@class=’avatar width-full rounded-2']"
loginInputUserElementName = "login"
loginInputPassElementName = "llave"
#button onclick="javascript:enviaLogin();"

#//img[@src='img/login/bot_entrar.jpg']
loginBotonUserXPath = "//img[@src='img/login/bot_entrar.jpg']"
loginBotonPassXPath = "//img[@onclick='document.forms[0].submit();']"
loginCerrarSesionElementXpath = "//button[@onclick='javascript:enviaLogin();']"

#a href="javascript:hideOrShow();" class="menuNVTC"
leftFrameName = "leftFrame"
contenidoFrameName = "contenido"

topFrameName = "topFrame"
busquedaClienteXPath = "//a[@href='javascript:hideOrShow();']"
topFramePartialLinkName = "Búsqueda de Cliente"
leftFrameLoaderXpath = '//img[@src="/IusacellDist/img/indicator.gif"]'

numeroLineaPrefijo = '4.'
numeroLineaSufijo = '7916'
numeroLineaMock = '4.7910'
buscaBotonName = 'buscaBtn'
dnInputName = 'dn'

busquedaDnInputXpath = "//input[@name='dn']"
busquedaBotonId = 'btIr'

#Contenido del numero 
telefonoTdId = 'telefonopacambio'

class UniCuentaException(Exception):    
    pass

def Login(browser):
    try:
        #Introduce Username
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.NAME, loginInputUserElementName)))
        loginElement = browser.find_element_by_name(loginInputUserElementName)
        loginElement.send_keys(loginUser)

        logionUserButon = browser.find_element_by_xpath(loginBotonUserXPath)
        logionUserButon.click()

        #introduce Password
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.NAME, loginInputPassElementName)))        
        loginPassElement = browser.find_element_by_name(loginInputPassElementName)
        loginPassElement.send_keys(loginPassword)

        loginPassButon = browser.find_element_by_xpath(loginBotonPassXPath)
        loginPassButon.click()

        pass

    except TimeoutException as toex:
        print("Timeout reached", toex)
        pass
    except Exception as ex:
        print(ex)

def ByPassSesionAnterior(browser):
    try:
        time.sleep(1)
        WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.XPATH,loginCerrarSesionElementXpath)))
        loginCerrarSesionButonElement = browser.find_element_by_xpath(loginCerrarSesionElementXpath)
        loginCerrarSesionButonElement.click()
        pass
    except Exception as ex:
        print(ex)
        
    finally:
        pass

def WaitAndSwitchToLeftFrame(browser):
    browser.switch_to.default_content()    
    # Espera a que el leftframe este disponible y hace el switch hacia el
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,leftFrameName)))
    WebDriverWait(browser,timeout).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,leftFrameName)))
    time.sleep(sleepForSwitch)

def WaitAndSwitchToContenidoFrame(browser):
    browser.switch_to.default_content()    
    # Espera a que el leftframe este disponible y hace el switch hacia el
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,contenidoFrameName)))
    WebDriverWait(browser,timeout).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,contenidoFrameName)))
    time.sleep(sleepForSwitch)

def GetTelefonosDeCuenta(browser,cuenta):
    WaitAndSwitchToLeftFrame(browser)
    # Espera a que el input "cuenta" este disponible y escribe el numero de cuenta
    # una vez hecho esto, da click al boton buscar
    # WebDriverWait(browser,timeout).until(EC.element_to_be_clickable((By.NAME,buscaBotonName)))
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.ID,'contrato')))
    cuentaInputElement = browser.find_element_by_id('contrato')
    time.sleep(sleepForReload)
    cuentaInputElement.clear()
    cuentaInputElement.send_keys(cuenta)
    time.sleep(sleepForReload)
    WebDriverWait(browser,timeout).until(EC.element_to_be_clickable((By.NAME,buscaBotonName)))
    buscaButtonElement = browser.find_element_by_name(buscaBotonName)
    buscaButtonElement.click()   

    ValidarUniCuenta(browser)
    # Obtiene los links de las subcuentas
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,cuenta)))
    numeroLineasLink = len(browser.find_elements_by_partial_link_text(cuenta))
    # Da click en todas las subcuentas
    for idx in range(numeroLineasLink):
        WebDriverWait(browser,timeout).until_not(EC.visibility_of_element_located((By.XPATH,leftFrameLoaderXpath)))
        WebDriverWait(browser,timeout).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,cuenta)))
        # browser.implicitly_wait(6000)
        # time.sleep(3)
        lineasLink = browser.find_elements_by_partial_link_text(cuenta)
        lineaLink = lineasLink[idx]
        lineaLink.click()

    # Pasa el DOM para crear un objeto Soup
    soup =  BeautifulSoup(browser.page_source,'lxml')

    numeroLineaFinder = soup.find_all("a", class_='CUENTAS4')
    listaNumeros = [num.string for num in numeroLineaFinder]

    return listaNumeros

def GetPanelBusquedaLimpio(browser):
    browser.switch_to.default_content()
    time.sleep(sleepForSwitch)

    # WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,leftFrameName)))
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.XPATH,'/html/frameset/frameset')))
    isLeftFrameVisible = browser.find_element_by_name(leftFrameName).is_displayed()

    topFrame = browser.find_element_by_name(topFrameName)
    browser.switch_to.frame(topFrame)
    busquedaClienteLinkElement = browser.find_element_by_xpath(busquedaClienteXPath)

    if(isLeftFrameVisible):
        WebDriverWait(browser,timeout).until(EC.element_to_be_clickable((By.XPATH,busquedaClienteXPath)))
        busquedaClienteLinkElement.click()
        time.sleep(1)

    WebDriverWait(browser,timeout).until(EC.element_to_be_clickable((By.XPATH,busquedaClienteXPath)))
    busquedaClienteLinkElement.click()
    
def ValidarUniCuenta(browser):
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.XPATH,'//td[@class="CUENTAS1"]')))
    cuentaMasIconXpath = '//img[@src="/IusacellDist/config/treeNodeCloseLast.gif"]'
    try:
        iconoMas = browser.find_element_by_xpath(cuentaMasIconXpath)
        iconoMas.click()
    except NoSuchElementException:
        pass

def getNumeroDom(browser,numero):
    GetPanelBusquedaLimpio(browser)
    WaitAndSwitchToLeftFrame(browser)
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,dnInputName)))
    WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.ID,busquedaBotonId)))
    browser.find_element_by_name(dnInputName).send_keys(numero)
    browser.find_element_by_id(busquedaBotonId).click()
    
    WaitAndSwitchToContenidoFrame(browser)
    WebDriverWait(browser,timeoutContenido).until(EC.text_to_be_present_in_element((By.ID,telefonoTdId),numero))

    html = browser.page_source
    
    print(html)
    pass

def parseNumeroFromContenidoDom(dom):
    soup =  BeautifulSoup(browser.page_source,'lxml')

    # numeroLineaFinder = soup.find_all("a", class_='CUENTAS4')
    #soup.find()
    #listaNumeros = [num.string for num in numeroLineaFinder]
    pass

if __name__ == "__main__":
    try:
        cuentaSufijo = int(numeroLineaSufijo)

        #browser = webdriver.Chrome(r'..\web-driver\chromedriver.exe', service_args=["--verbose",r"--log-path=..\web-driver\peas.log"])
        #browser = webdriver.Chrome()
        #browser = webdriver.Ie()
        #browser = webdriver.Edge()
        #browser = webdriver.Firefox(executable_path=r'..\web-driver\geckodriver.exe')
        browser = webdriver.Firefox()
        browser.get('http://pvs.iusacell.com.mx/')
        Login(browser)
        ByPassSesionAnterior(browser)

        for i in range(1):
            try:
                time.sleep(1)
                cuenta = numeroLineaPrefijo + str(cuentaSufijo + i)
                GetPanelBusquedaLimpio(browser)
                telefonos = GetTelefonosDeCuenta(browser, cuenta)
                print(cuenta, telefonos)
                for tel in telefonos:
                    numeroDom = getNumeroDom(browser, tel)
                    numeroObject = parseNumeroFromContenidoDom(numeroDom)
            except UniCuentaException as ucex:
                pass
            except TimeoutException as toex:
                pass

        # Buscar(browser)
        pass
    except WebDriverException as wex:
        print(wex.msg, wex.screen, wex.stacktrace)
    except Exception as ex:
        print(ex)
    finally:
        browser.quit()
        pass
