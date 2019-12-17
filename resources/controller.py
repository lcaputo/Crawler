import os, time
import requests
import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

_URL = 'https://www.chip.gov.co/schip_rt/index.jsf'
downloadFolder = r''+os.getcwd()+'\CHIP_REPORTES\\'
oldItemsInFolder = []
itemsInFolder = []
excelDocs = []

class Page():
    def conn():

        chromeDriver = ChromeDriverManager().install()

        """ CONFIG WEBDRIVER OPTIONS """
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-referrers")
        # OCULTAR NAVEGADOR
        # options.add_argument("--headless")
        prefs = {
            "download.default_directory": downloadFolder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "profile.default_content_settings" : 2,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_settings.notifications": 1,
            "profile.managed_default_content_settings.images": 2,
            "profile.browser.cache.disk.enable": False,
            "profile.browser.cache.memory.enable": False,
            "browser.cache.offline.enable": False,
            "network.http.use-cache": False
        }
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=options)
        driver.get(_URL)
        driver.find_element_by_link_text("Consultas").click()
        driver.find_element_by_link_text("Informe al Ciudadano").click()
        time.sleep(1)
        return driver

    def reload():
        driver.delete_cookie('JSESSIONID')
        driver.refresh()
        driver.find_element_by_link_text("Consultas").click()
        driver.find_element_by_link_text("Informe al Ciudadano").click()
        time.sleep(1)

    def consultas():
        time.sleep(1)
        driver.find_element_by_link_text("Consultas").click()
        time.sleep(1)
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
        time.sleep(1)
        categories = []
        time.sleep(1)
        """ GET ENTITY CATEGORIES """
        dropDown = driver.find_element_by_name("frm1:SelBoxCategoria")
        time.sleep(1)
        options = dropDown.find_elements_by_tag_name("option")
        time.sleep(1)
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
        time.sleep(1)
        categoryDropdown = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxCategoria']"))
        time.sleep(1)
        try:
            categoryDropdown.select_by_value(value)
        except:
            return False
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
        time.sleep(1)
        """ FILLING CATEGORIES DROP DOWN BY ENTITY ID """
        periodDropdown = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxPeriodo']"))
        time.sleep(1)
        periodDropdown.select_by_value('0')
        time.sleep(2)
        try:
            periodDropdown.select_by_value('1' + value)
        except:
            return False
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
        time.sleep(3)
        driver.find_element_by_xpath("//*[@title='Descargar a Excel']").click()
        time.sleep(2)
        """ time.sleep(1)
        level = Select(driver.find_element_by_xpath("//select[@id='frm1:SelBoxNivel']"))
        level.select_by_value("11") """
        return True

class Download():
    def convertSet(set):
        return [*set, ]

    def saveDirectoryItems():
        oldItemsInFolder.clear()
        itemsInFolder.clear()
        excelDocs.clear()
        fileNames = os.listdir(downloadFolder)
        for fileName in fileNames:
            oldItemsInFolder.append(fileName)

    def createFolder(folderName=""):
        if not (folderName in oldItemsInFolder):
            os.system('mkdir ' + downloadFolder + folderName)

    def knowNewItems():
        fileNames = os.listdir(downloadFolder)
        for fileName in fileNames:
            itemsInFolder.append(fileName)
        newItem = set(itemsInFolder) - set(oldItemsInFolder)
        print(len(newItem))
        if (len(newItem) != 0):
            items = Download.convertSet(newItem)
            print('New Items: ', len(items))
            for i in range(0, len(items)):
                downloadedFileName = os.path.splitext(items[i])[0]
                extension = os.path.splitext(items[i])[1]
                if (len(downloadedFileName) > 30 and extension == '.xls'):
                    excelDocs.append(items[i])
            print('excel docs = ', excelDocs[0])

    def renameDoc(newFileName):
        os.rename(downloadFolder+'\\'+excelDocs[0], downloadFolder+newFileName+'.xls')

    def compareExcelDocs(docName, entidad=""):
        os.system("cd " + downloadFolder)
        df1 = pd.read_excel(excelDocs[0])
        df2 = pd.read_excel(str(docName2) + '.xls')
        print(df1.equals(df2))

    def deleteExcel():
        os.remove(excelDocs[0])

    def deleteReport(route):
        os.remove(route)

'''
class main():
    if not DriverOpen():
        OpenDriver()
    else:
        Entity()



if __name__ == '__main__':
    main()
'''