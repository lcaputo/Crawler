import os, time
from itertools import zip_longest
import pandas as pd

userFolder = os.environ['USERPROFILE']
downloadFolder = r''+userFolder+'\Desktop\\REPORTES CHIP'
firstDocsInFolder = []
actualatityDocsInFolder = []


def listDir(dir):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        print('File Name: ' + fileName)
        firstDocsInFolder.append(fileName)

def compareDir(dir):
    if not('prueba' in firstDocsInFolder):
        os.system("mkdir prueba")
        fileNames = os.listdir(dir)
        for fileName in fileNames:
            print('File Name: ' + fileName)
            actualatityDocsInFolder.append(fileName)
    else:
        print('prueba ya existe')


def compareExcelDoc(docName1, docName2, entidad=""):
    os.system("cd "+downloadFolder+"\\"+entidad)
    df1 = pd.read_excel(str(docName1)+'.xls')
    df2 = pd.read_excel(str(docName2)+'.xls')
    print(df1.equals(df2))


# TODO: os.rename(original, nuevoNombre)

if __name__ == '__main__':
    listDir(downloadFolder)
    print(firstDocsInFolder)
    compareDir(downloadFolder)
    print(actualatityDocsInFolder)
    time.sleep(2)
    print(set(actualatityDocsInFolder)-set(firstDocsInFolder))
    compareExcelDoc(1,2)
