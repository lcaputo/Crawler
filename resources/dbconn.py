import pyodbc

''' CONNEXION A LA BASE DE DATOS '''
def connection():
    server = 'efi-pro.cflyqudqcoq8.us-east-2.rds.amazonaws.com'
    database = 'efi-pro'
    username = 'sa'
    password = 'Admin12345'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn