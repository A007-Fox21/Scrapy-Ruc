#-*- coding: utf-8 -*-

import requests
import io
import random
import time
import os
import sys
import json

# Selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from xvfbwrapper import Xvfb
from io import open
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# check if using python 3
if sys.version_info[0] > 3:
    xrange = range

# Firefox / Gecko Driver Related
#FIREFOX_BIN_PATH = r"/usr/lib/firefox/firefox"
#GECKODRIVER_BIN = r"/usr/local/bin/geckodriver.sh"

# Randomization Related
MIN_RAND        = 0.84
MAX_RAND        = 1.14
LONG_MIN_RAND   = 4.76
LONG_MAX_RAND   = 8.1

NUMBER_OF_ITERATIONS = 2
RECAPTCHA_PAGE_URL = "https://etax2.mef.gob.pa/etax2web/Par/AdministrarParametro.aspx?p=pZz9L4JCroiikGiJCwsiz7KAPxkk7gW0PFEfJu0/SyY5zPAI+K9PwpP6dFp8haipI9ufWHfDqmHjys6SpQTiqqHZUNPX73uw8JB2o+0URrzADwWMaECY8OLnvprbcTYBJa8jjOg3/YLB+Y0bF5totw=="
             
class breakcaptcha(object):
    def __init__(self):
        #os.environ["PATH"] += os.pathsep + GECKODRIVER_BIN
        #self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(FIREFOX_BIN_PATH))

        #self.firefox_profile = webdriver.FirefoxProfile()
        #self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        #self.driver = webdriver.Firefox(firefox_profile=self.firefox_profile)

        self.op = Options()
        self.op.add_argument('-private')
        self.driver = webdriver.Firefox(firefox_options=self.op)
        self.breakrecaptcha = 'false'

    def is_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def current_page(self):
        pag_actual = self.driver.find_element_by_xpath('//td/table/tbody/tr/td/span')
        return  str(pag_actual.text)

    def next_link(self,html):
        link = "".join([x for x in html[-9:-3] if x.isdigit()])
        return  str(link)

    def is_exists_by_text_link(self,text):
        try:
            link_text = self.driver.find_element_by_link_text(text)
        except NoSuchElementException:
            return False
        return True

    def get_recaptcha_challenge(self):
        #Empresa a consultar
        #COMPANY = raw_input('Empresa o Razon Social: ')
        COMPANY = 'montero'

        # Navigate to a ReCaptcha page
        self.driver.get(RECAPTCHA_PAGE_URL)
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
            
        a = self.driver.find_element_by_id('Contenedor_Contenedor_C_NOMBRE_RAZON_SOCIAL').send_keys(COMPANY)
        #a.send_keys(COMPANY)
        
        print('COMENZAMOS OK ;P.')

        # Get all the iframes on the page
        iframes = self.driver.find_elements_by_tag_name("iframe")
            
        # Switch focus to ReCaptcha iframe
        self.driver.switch_to_frame(iframes[0])
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        self.driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]').click()
        while 1:
            # Verify ReCaptcha checkbox is present
            if not self.is_exists_by_xpath('//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]'):
                print("[{0}] No element in the frame!!".format(self.current_iteration))
                continue
            else:
                # Click on ReCaptcha checkbox
                pages=0

                while not self.is_exists_by_xpath('//span[@aria-checked="true"]'):
                    time.sleep(random.uniform(MIN_RAND, MAX_RAND))
                else:
                    self.breakrecaptcha = self.is_exists_by_xpath('//span[@aria-checked="true"]')
                    #print('Entrando al ELSE del bucle While ok.')
                    self.driver.switch_to.default_content()
                    b = self.driver.find_element_by_id('Contenedor_Contenedor_botonBuscar')
                    b.click()
                    time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
                    arch_dato = open("datos.txt","w")
                    inicio = 1
                    salir = 0
                    last_break = 0
                    r=2
                    #CHECK EXISTE MAS PAGINAS
                    while salir == 0:
                        #print('Entre al bucle While, paginas:',pages,' current_pages:',self.current_page())
                        for x in range(inicio,21):
                            self.driver.switch_to.default_content()
                                    
                            #Abrir y obtener datos de la siguientes paginas  
                            if self.is_exists_by_xpath('//td/table/tbody/tr/td[' + str(x) + ']'):
                                while salir==0:
                                    try:
                                        b1= self.driver.find_element_by_xpath('//td/table/tbody/tr/td[' + str(x) + ']')
                                        html = b1.get_attribute("innerHTML")
                                        #print(html)
                                        b1.click()
                                        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
                                        salir=1
                                    except:
                                        salir=0
                                        print('Exception!, pero, trataremos de seguir ;D...')
                                        continue
                                salir=0
                                #print('Valor de X:'+str(x),' Existe siguiente link?:', self.is_exists_by_text_link(str(pages+1)),  'next_link:' + self.next_link(html), 'pages:',pages+1, 'current_page:' + self.current_page())
                                
                                if self.current_page() == str(pages+1):
                                    pages +=1
                                    #print('IF current_page = pages?:'+self.current_page()+'='+str(pages),'is_exists_by_text_link(Última página)', self.is_exists_by_text_link('Última página'), 'X:'+str(x))
                                    
                                    if pages == 1:
                                        datos = self.driver.find_element_by_xpath('//*[@id="Contenedor_Contenedor_grv"]/tbody/tr[1]')
                                        arch_dato.write(datos.text+'\n')

                                    try:
                                        for n in range(r,17):
                                            datos = self.driver.find_element_by_xpath('//*[@id="Contenedor_Contenedor_grv"]/tbody/tr['+ str(n) +']')
                                            #print(datos.text +'\n')
                                            arch_dato.write(datos.text+'\n')
                                    except (NoSuchElementException):
                                        break
                           
                                    print('GRABADO datos de la pagina: ',pages, 'Pagina Actual: ' + str(self.current_page()))
                                    #print('Next_link:',self.next_link(html))
                                    if self.next_link(html) == '' and self.is_exists_by_text_link('Última página'):
                                        inicio = 4
                                        last_break = pages
                                        #print('Last Break: '+str(last_break))
                                        break
                                    else:
                                        #print('Else:, Existe la pagina:', str(self.current_page()), 'Existe Pagina '+str(pages),self.is_exists_by_text_link(str(int(self.current_page())+1)))
                                        if self.next_link(html) == '':
                                            for y in range(int(self.current_page())+1,64):
                                                if self.is_exists_by_text_link(str(y)) and self.current_page() == str(pages):
                                                    link = self.driver.find_element_by_link_text(str(y))
                                                    link.click()
                                                    time.sleep(random.uniform(MIN_RAND, MAX_RAND))
                                                    pages +=1
                                                    try:
                                                        for n in range(r,17):
                                                            datos = self.driver.find_element_by_xpath('//*[@id="Contenedor_Contenedor_grv"]/tbody/tr['+ str(n) +']')
                                                            #print(datos.text +'\n')
                                                            arch_dato.write(datos.text+'\n')
                                                    except (NoSuchElementException):
                                                        break
                                                    print('GRABADO datos de la pagina: ',pages, 'Pagina Actual: ' + str(self.current_page()))
                                                else:
                                                    #print('TERMINO!..., NO existe la pagina:', str(y))
                                                    break
                                            
                                else:
                                    print ('Link actual', self.next_link(html))
                                        
                            else:
                                salir = 1
                                print('NO!!! hay mas paginas creo :P, pagina: ', pages, ' Current_page:', self.current_page())
                                break
                    #except (RuntimeError, TypeError, NameError, NoSuchElementException):
                    #    print('EXCEPTION :( ...')

                #print('Final del While not self.is_exists_by_xpath, con not self.is_exists_by_xpath', self.is_exists_by_xpath('//span[@aria-checked="true"]'))

                arch_dato.close()
                print('CANTIDAD DE PAGINAS LEIDAS ',pages)
                return
                                         
    def solve(self, current_iteration):
        self.current_iteration = current_iteration + 1

        # Get a ReCaptcha Challenge
        self.get_recaptcha_challenge()

        print(self.breakrecaptcha)
        self.driver.close()
        
        return self.breakrecaptcha
                
def main():
    #Para ocultar el browser on virtual
    #display = Xvfb()
    #display.start()

    breakcaptcha_obj = breakcaptcha()
    
    counter = 0
    for i in xrange(NUMBER_OF_ITERATIONS):
        if breakcaptcha_obj.solve(i):
            counter += 1
            
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        print("Successful breaks: {0}".format(counter))
        break
    #Stop virtual window
    #display.stop()   
    print("Total successful breaks: {0}\{1}".format(counter, NUMBER_OF_ITERATIONS))

if __name__ == '__main__':
    main()
