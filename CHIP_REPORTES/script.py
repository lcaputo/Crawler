import os,time
from itertools import zip_longest
import pandas as pd

downloadFolder = r''+os.getcwd()
oldItemsInFolder = []
itemsInFolder = []
excelDocs = []

def convertSet(set):
    return [*set, ]

def saveDirectoryItems(dir):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        oldItemsInFolder.append(fileName)


def createFolder(dir, folderName=""):
    if not(folderName in oldItemsInFolder):
        os.system('mkdir '+folderName)
    else:
        print(folderName +' Ya Existe!')

def createFile(dir, filerName=""):
    if not(filerName in oldItemsInFolder):
        os.system('echo some-text > '+filerName+'.txt')
        os.system('echo some-text > '+filerName+'2.xls')
        os.system('echo some-text > ' + '21010800158K2644070920191572027099676.xls')
    else:
        print(filerName +' Ya Existe!')


def knowNewItems(dir):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        itemsInFolder.append(fileName)
    newItem = set(itemsInFolder)-set(oldItemsInFolder)
    print(len(newItem))
    if (len(newItem) != 0):
        items = convertSet(newItem)
        print('New Items: ', len(items))
        for i in range(0, len(items)):
            downloadedFileName = os.path.splitext(items[i])[0]
            extension = os.path.splitext(items[i])[1]
            if(len(downloadedFileName) > 30 and extension == '.xls'):
                excelDocs.append(items[i])
        print('excel docs = ',excelDocs)


def renameDoc(fileName, newFileName):
    os.rename(fileName, newFileName)

def compareExcelDocs(docName1, docName2, entidad=""):
    os.system("cd "+downloadFolder)
    df1 = pd.read_excel(str(docName1)+'.xls')
    df2 = pd.read_excel(str(docName2)+'.xls')
    print(df1.equals(df2))


# TODO: os.rename(original, nuevoNombre)

if __name__ == '__main__':
    saveDirectoryItems(downloadFolder)
    createFile(downloadFolder, 'Barranquilla')
    knowNewItems(downloadFolder)
    time.sleep(2)
    compareExcelDocs(1,2)
    renameDoc(str(excelDocs[0]), 'renamed.xls')
