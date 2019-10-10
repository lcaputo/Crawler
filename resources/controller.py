import time
import requests
import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

_URL = 'https://www.chip.gov.co/schip_rt/index.jsf'

class Page():
    def conn():
        chromeDriver = ChromeDriverManager().install()
        """ CONFIG WEBDRIVER OPTIONS """
        option = webdriver.ChromeOptions()
        chrome_prefs = {}
        option.experimental_options["prefs"] = chrome_prefs
        option.add_argument("--disable-infobars")
        chrome_prefs["profile.default_content_settings"] = {"notifications": 1}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=option)
        driver.get(_URL)
        driver.find_element_by_link_text("Consultas").click()
        driver.find_element_by_link_text("Informe al Ciudadano").click()
        time.sleep(1)
        return driver

    def reload():
        driver.get(_URL)
        driver.find_element_by_link_text("Consultas").click()
        driver.find_element_by_link_text("Informe al Ciudadano").click()
        time.sleep(1)

    def quit():
        driver.quit()


""" WEBDRIVER CONNECTION """
driver: webdriver = Page.conn()


class Entity():
    """ FILLING ENTITY INPUT """

    def fillEntityInput(keyword):
        entityInput = driver.find_element_by_xpath("//input[@id='frm1:SelBoxEntidadCiudadano_input']")
        entityInput.clear()
        entityInput.send_keys(keyword)
        time.sleep(1)
        entityInput.send_keys(Keys.ENTER)

    def getEntitiesByKeyword():
        entities = []
        """ Select entities container div """
        div = driver.find_element_by_id("frm1:SelBoxEntidadCiudadano_div")
        """ Select all entity options """
        options = div.find_elements_by_xpath("div//*")
        for elm in options:
            entity = elm.get_attribute('innerHTML')
            """ Separe entity code """
            codeAndEntity = str(entity).split(' ', 1)
            json = {
                "code": int(codeAndEntity[0]),
                "name": codeAndEntity[1][2:len(codeAndEntity[1])]
            }
            entities.append(json)
        return entities


class Category():

    def getCategories():
        categories = []
        """ GET ENTITY CATEGORIES """
        dropDown = driver.find_element_by_name("frm1:SelBoxCategoria")
        options = dropDown.find_elements_by_tag_name("option")
        for elm in options:
            value = elm.get_attribute("value")
            name = elm.get_attribute("innerHTML")
            json = {
                "value": value,
                "name": name
            }
            categories.append(json)
        return categories

    def fillCategoryDropDown(value):
        """ FILLING CATEGORIES DROP DOWN BY ENTITY ID """
        categoryDropdown = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxCategoria']"))
        categoryDropdown.select_by_value(value)
        return True


class Period():
    def getPeriods():
        periods = []
        """ GET PERIODOS """
        options = driver.find_elements_by_xpath("//select[@id='frm1:SelBoxPeriodo']//*")
        for elm in options:
            json = {
                "value": elm.get_attribute("value")[1:len(elm.get_attribute("value"))],
                "name": elm.get_attribute("innerHTML")
            }
            periods.append(json)
        return periods

    def fillPeriodDropDown(value):
        """ FILLING CATEGORIES DROP DOWN BY ENTITY ID """
        periodDropdown = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxPeriodo']"))
        periodDropdown.select_by_value('0')
        time.sleep(2)
        periodDropdown.select_by_value('1' + value)
        return True


class Form():
    def getFormulario():
        formulario = []
        """ GET FORMULARIO """
        selectDiv = driver.find_element_by_id("frm1:SelBoxForma")
        options = selectDiv.find_elements_by_tag_name("option")
        for elm in options:
            json = {
                "value": elm.get_attribute("value"),
                "name": elm.get_attribute("innerHTML")
            }
            formulario.append(json)
        return formulario

    def fillFormDropDown(value):
        """ FILLING CATEGORIES DROP DOWN BY ENTITY ID """
        formDropdown = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxForma']"))
        formDropdown.select_by_value(value)
        """ CLICK ON SUBMIT BUTTON """
        driver.find_element_by_id("frm1:BtnConsular").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@title='Descargar a Excel']").click()
        time.sleep(1)
        level = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxNivel']"))
        level.select_by_value("11")
        return True


'''
class main():
    if not DriverOpen():
        OpenDriver()
    else:
        Entity()



if __name__ == '__main__':
    main()
'''