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
        """ cursor.execute(
            "SELECT codigo_chip, entidad FROM entidades where departamento in(select distinct(Departamento) from entidades where id_entidad = (select fk_entidad from empresa where estado=1 ));") """
        cursor.execute("SELECT codigo_chip, entidad FROM entidades where estado = 1;")
        print('\n CODIGOS CHIP\n ---------------')
        for row in cursor:
            print(' Codigo = ', row.codigo_chip, ' Entidad = ', row.entidad)
            codigos_chip.append(row)
        print('\n\n')
        cursor.close()
        return codigos_chip

    def codigoReporte():
        cursor = conn.cursor()
        """ GUARDAR CODIGOS CHIP EN ARRAY """
        cursor.execute("SELECT * FROM reportes_chip WHERE estado =1")
        print(' CODIGOS REPORTE\n ---------------')
        for row in cursor:
            print(' Nombre = ', row.nombre + '\t Valor = ', row.codigo_chip_reporte)
            codigos_reporte.append(row)
        print('\n\n')
        cursor.close()
        return codigos_reporte

    def periodoActual():
        cursor = conn.cursor()
        """ GUARDAR CODIGOS CHIP EN ARRAY """
        cursor.execute("SELECT codigo_chip, periodo, descripcion_chip FROM calendario where activo =1")
        periodos = []
        for row in cursor:
            mes = str(int(row.codigo_chip)).zfill(4)
            ano = str(int(row.periodo)).zfill(4)
            descripcion = row.descripcion_chip
            name = descripcion + ano
            value = str(mes + '|' + ano)
            json = {
                "mes": mes,
                "ano": ano,
                "name": name,
                "value": value
            }
            periodos.append(json)


        if ( len(periodos) > 1 ):
            print(' PERIODOS\n ---------------')
            for i in range(0, len(periodos)):
                print(' #',i + 1, ' => ',periodos[i]["name"])
        else:
            print(' PERIODO\n ---------------\n',periodos[0]["name"])


        print('\n\n--------------------------------------------------\n')
        cursor.close()
        return periodos

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