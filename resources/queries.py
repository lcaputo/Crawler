from resources.dbconn import connection
import json

conn = connection()

codigos_chip = []
codigos_reporte = []
periodo = ''

class Get():
    def codigoChip():
        cursor = conn.cursor()
        """ GUARDAR CODIGOS CHIP EN ARRAY """
        cursor.execute(
            "SELECT codigo_chip, entidad FROM entidades where departamento in(select distinct(Departamento) from entidades where id_entidad = (select fk_entidad from empresa where estado=1 ));")
        print('\nCODIGOS CHIP')
        for row in cursor:
            print('Codigo = ', row.codigo_chip, ' Entidad = ', row.entidad)
            codigos_chip.append(row)
        print('\n\n')
        cursor.close()
        return codigos_chip

    def codigoReporte():
        cursor = conn.cursor()
        """ GUARDAR CODIGOS CHIP EN ARRAY """
        cursor.execute("SELECT * FROM reportes_chip WHERE estado =1")
        print('CODIGOS REPORTE')
        for row in cursor:
            print('Codigo = ', row.codigo_chip_reporte, ' Nombre = ', row.nombre)
            codigos_reporte.append(row)
        print('\n\n')
        cursor.close()
        return codigos_reporte

    def periodoActual():
        cursor = conn.cursor()
        """ GUARDAR CODIGOS CHIP EN ARRAY """
        cursor.execute("SELECT codigo_chip, periodo FROM calendario where activo =1")
        print('PERIODO')
        for row in cursor:
            mes = int(row.codigo_chip)
            ano = int(row.periodo)
        mes = str(mes).zfill(4)
        ano = str(ano)
        periodo = [mes,ano,(mes + '|' + ano)]
        print(periodo[2], '\n\n------------------------------------------------------------\n')
        cursor.close()
        return periodo

    def buscarAlertaPorCodigoChip(chip,reporte,ano,mes):
        cursor = conn.cursor()
        matches = []
        """ BUSCAR ALERTAS POR CODIGO CHIP """
        cursor.execute("SELECT * FROM alertas_reportes WHERE codigo_chip = %s and codigo_chip_reporte = '%s' and periodo_anno = %s and periodo_meses = '%s'" % (chip,reporte,ano,mes))
        for row in cursor:
           matches.append(row)
        cursor.close()
        return matches

class Set():
    def alerta(cc,codigo_chip_reporte,periodo_anno,periodo_meses,estado):
        cursor = conn.cursor()
        """ LLENAR TABLA ALERTAS_REPORTES """
        cursor.execute("INSERT INTO alertas_reportes(codigo_chip,codigo_chip_reporte,periodo_anno,periodo_meses,estado) VALUES (?,?,?,?,?);",(cc,codigo_chip_reporte,periodo_anno,periodo_meses,estado))
        conn.commit()
        cursor.close()

class Update():
    def entidad(periodo_anno,periodo_meses,estado,cc,codigo_chip_reporte):
        cursor = conn.cursor()
        """ LLENAR TABLA ALERTAS_REPORTES """
        cursor.execute("UPDATE alertas_reportes SET periodo_anno = %s ,periodo_meses = '%s' ,estado = %s where codigo_chip = %s and codigo_chip_reporte = '%s'" % (periodo_anno,periodo_meses,estado,cc,codigo_chip_reporte))
        conn.commit()
        cursor.close()

"""
if __name__ == '__main__':
    Get.codigoChip()
    Get.codigoReporte()
    Get.periodo()
"""