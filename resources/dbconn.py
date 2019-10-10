import pyodbc

def connection():
    server = 'salud.cflyqudqcoq8.us-east-2.rds.amazonaws.com'
    database = 'efi_dev'
    username = 'sa'
    password = 'Admin123'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn