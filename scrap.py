from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver import *
import pandas as pd

timeout = 12

#Data variables
loginUser = "D303433012"
loginPassword = "GH0&qsm7"

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
busquedaLinkFrameName = "topFrame"
busquedaPanelFrameName = "leftFrame"
contenidoFrameName = "contenido"

busquedaLinkXPath = "//a[@href='javascript:hideOrShow();']"
busquedaLinkXPartialLinkName = "Búsqueda de Cliente"

numeroLineaMock = '4.7910'
buscaBotonName = 'buscaBtn'

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

def isFrameLoaded(browser, frameName):
    return EC.visibility_of_element_located((By.NAME, frameName))

def areFramesLoaded(browser):
    isTopFrameLoaded = isFrameLoaded(browser,busquedaLinkFrameName)
    isLeftFrameLoaded = isFrameLoaded(browser,busquedaPanelFrameName)
    isContenidoFrameLoaded = isFrameLoaded(browser, contenidoFrameName)

    return isTopFrameLoaded and isLeftFrameLoaded and isContenidoFrameLoaded

import time

def Buscar(browser):
    try:
        time.sleep(1)
        WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,busquedaPanelFrameName)))
        leftFrameElement = browser.find_element_by_name(busquedaPanelFrameName)
        # topFrameElement = browser.find_element_by_name(busquedaLinkFrameName)
        # contenidoFrameElement = browser.find_element_by_name(contenidoFrameName)
        # defaultBrowser = browser

        browser.switch_to.frame(leftFrameElement)
        # dnInputElement = browser.find_element_by_xpath("//input[@name='dn']")
        # dnInputElement.send_keys('3323130989')

        # irButtonElement = browser.find_element_by_id("btIr")
        # irButtonElement.click()


        WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.NAME,buscaBotonName)))
        cuentaInputElement = browser.find_element_by_id('contrato')
        cuentaInputElement.send_keys(numeroLineaMock)

        buscaButtonElement = browser.find_element_by_name(buscaBotonName)
        buscaButtonElement.click()

        #WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.LINK_TEXT, busquedaLinkXPartialLinkName)))
        #WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.XPATH, busquedaLinkXPath)))
        #busquedaLinkElement = browser.find_element_by_xpath(busquedaLinkXPath)
        #busquedaLinkElement2 = browser.find_element_by_link_text(busquedaLinkXPartialLinkName)
        #busquedaLinkElement.click()
        
        WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,numeroLineaMock)))
        lineasLinkItems = browser.find_elements_by_partial_link_text(numeroLineaMock)

        for idx,_ in enumerate(lineasLinkItems):
            WebDriverWait(browser,timeout).until_not(EC.visibility_of_element_located((By.XPATH,'//img[@src="/IusacellDist/img/indicator.gif"]')))
            WebDriverWait(browser,timeout).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,numeroLineaMock)))
            time.sleep(0.01)
            
            lineasLink = browser.find_elements_by_partial_link_text(numeroLineaMock)
            lineaLink = lineasLink[idx]
            lineaLink.click()

        WebDriverWait(browser,timeout).until_not(EC.visibility_of_element_located((By.XPATH,'//img[@src="/IusacellDist/img/indicator.gif"]')))
        WebDriverWait(browser,timeout).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,numeroLineaMock)))

        pageSource = browser.page_source

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(pageSource,'lxml')

        numeroLineaFinder = soup.find_all("a", class_='CUENTAS4')

        print(numeroLineaFinder)

        for numero in numeroLineaFinder:
            print(numero.string)


        pass
    except Exception as ex:
        print(ex)
        pass
    

if __name__ == "__main__":
    try:
        browser = webdriver.Chrome(r'..\web-driver\chromedriver.exe', service_args=["--verbose",r"--log-path=..\web-driver\peas.log"])
        browser.get('http://pvs.iusacell.com.mx/')
        Login(browser)
        ByPassSesionAnterior(browser)
        Buscar(browser)
        pass
    except Exception as ex:
        print(ex)
    finally:
        browser.quit()
        pass
