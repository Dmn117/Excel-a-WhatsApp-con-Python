import time
import os
from Frutas import Frutas
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Mensaje:
    def __init__(self):
        #---------------------------------------------Carga de Variables de Entorno mediante .env
        load_dotenv()
        # Intenta Descargar el ChromeDriver usando servicios de Internet del equipo
        try:
            self._service = Service(ChromeDriverManager().install())
        # En caso de no lograrlo, utilizara un ChromeDriver descargado manualmente en la carpeta chromedriver_win32 de la riz del proyecto
        # Asegurarse de que dicho archivo este actualizado de acuerdo a su versión de chrome
        # Referencias: https://chromedriver.chromium.org/downloads
        except Exception as error:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Error al Instalar ChromeDriverManager: {error}')
            self._service = Service(executable_path=f'{os.getcwd()}/chromedriver_win32/chromedriver.exe')
        self._options = webdriver.ChromeOptions()
        self._driver = None
        self._whatsApp = os.environ.get('URL_WHATSAPP')
        self._xPathBusqueda = os.environ.get('XPATH_BUSQUEDA')
        self._xPathMensaje = os.environ.get('XPATH_MENSAJE')
        self._xPathMenu = os.environ.get('XPATH_MENU')
        self._menuButton = os.environ.get('MENU_BUTTON')
        self._logoutButton = os.environ.get('LOGOUT_BUTTON')
        self._confirmButton = os.environ.get('CONFIRM_BUTTON')
        self._mensaje = None
        self._contacto = None
        self._isOpen = False
        self._frutas = Frutas()

    # Metodos GET
    def getService(self):
        return self._service
    
    def getDriver(self):
        return self._driver
    
    def getWhatsApp(self):
        return self._whatsApp
    
    def getMensaje(self):
        return self._mensaje
    
    def getContacto(self):
        return self._contacto
    
    def getIsOpen(self):
        return self._isOpen
    
    def getFrutas(self):
        return self._frutas
    
    # Metodos SET
    def setService(self, service):
        self._service = service

    def setDriver(self, driver):
        self._driver = driver

    def setWhatsApp(self, whatsApp):
        self._whatsApp = whatsApp

    def setMensaje(self, mensaje):
        self._mensaje = mensaje

    def setContacto(self, contacto):
        self._contacto = contacto

    def setIsOpen(self, isOpen):
        self._isOpen = isOpen

    def setFrutas(self, frutas):
        self._frutas = frutas


    def returnShortCode(self, key):
        return self._frutas.__dict__.get(f'{key}', "")


    def saludo(self):
        horaActual = int(datetime.now().strftime('%H'))
        if(horaActual in range(5, 12)):
            return f'Buenos Días, les comparto los precios:'
        elif(horaActual in range(12, 20)):
            return f'Buenas Tardes, les comparto los precios:'
        else:
            return f'Buenas Noches, les comparto los precios:'


    # Metodos Varios
    def openWhatssApp(self):
        self._driver = webdriver.Chrome(service=self._service, options=self._options)
        self._driver.get(self._whatsApp)
        self._isOpen = True


    def buscarContactoWp(self):
        try:
            entradaBusqueda = self._driver.find_element(By.XPATH, self._xPathBusqueda)
            entradaBusqueda.send_keys(f'{self._contacto}')
            time.sleep(1)
            entradaBusqueda.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception as error:
            print(f'Error en Clase: Mensaje || Metodo: buscarContactoWp || {error}')


    def escribirMensaje(self):
        try:
            lineas = self._mensaje.splitlines()
            entradaMensaje = self._driver.find_element(By.XPATH, self._xPathMensaje)
            entradaMensaje.send_keys(f'*{self.saludo()}*')
            entradaMensaje.send_keys(Keys.SHIFT + Keys.ENTER)
            for linea in lineas:
                if(linea.strip()):
                    if(':' in linea):
                        substring = [item for item in linea.split(':') if not item.isspace()]
                        entradaMensaje.send_keys(Keys.SHIFT + Keys.ENTER)
                        for palabra in substring:
                            if (palabra != substring[0] and palabra != substring[-1]):
                                entradaMensaje.send_keys(f'{self.returnShortCode(palabra)}')
                                entradaMensaje.send_keys(Keys.ENTER)
                            else:
                                entradaMensaje.send_keys(f'{palabra} ')
                        # time.sleep(3)
                    else:
                        entradaMensaje.send_keys(f'{linea}')
                    entradaMensaje.send_keys(Keys.SHIFT + Keys.ENTER)
        except Exception as error:
            print(f'Error en Clase: Mensaje || Metodo: escribirMensaje || {error}')


    def enviarMensajeWp(self):
            try:
                self.buscarContactoWp()
                self.escribirMensaje()
            except Exception as error:
                print(f'Error en Clase: Mensaje || Metodo: enviarMensajeWp || {error}')   


    def cerrarSesion(self):
        try:
            menu_button = self._driver.find_element(By.CSS_SELECTOR, self._menuButton)
            menu_button.click()
            time.sleep(1)
            # Encuentra el botón "Cerrar sesión" y haz clic en él
            logout_button = self._driver.find_element(By.XPATH, self._logoutButton)
            logout_button.click()
            time.sleep(1)
            # Confirma el cierre de sesión
            confirm_button = self._driver.find_element(By.XPATH, self._logoutButton)

            confirm_button.click()
            time.sleep(1)
            self.delete()
        except Exception as error:
            print(f'Error en Clase: Mensaje || Metodo: close || {error}')


    def delete(self):
        try:
            self._driver.quit()
            self._isOpen = False
        except Exception as error:
            print(f'Error en Clase: Mensaje || Metodo: delete || {error}')