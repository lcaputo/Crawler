from resources import queries, controller
import time, json

""" VARIABLES """
entidades = queries.Get.codigoChip()
codigos_reporte = queries.Get.codigoReporte()
arregloPeriodos = queries.Get.periodoActual()
p = 0
r = 0

class main():
    """  * ALERTA *  PARA ENTIDADES DESACTUALIZADAS """
    def alerta(i,r, ano, mes, ultimoPeriodo):
        queries.Set.alerta(entidades[i].codigo_chip, codigos_reporte[r].codigo_chip_reporte, ano, mes, 1)
        return print('Alerta ', entidades[i].entidad.upper(), ' - ', codigos_reporte[r].nombre,
        '\nEl periodo actual no ha sido elaborado \nÚltima actulización : ', ultimoPeriodo,'\n---------------------------------\n')


    for a in range( 0, len(arregloPeriodos) ):
        for i in range(0, len(entidades)):
            while True:
                if (r >= len(codigos_reporte)):
                    r = 0
                    break
                time.sleep(2)
                controller.Entity.fillEntityInput(entidades[i].codigo_chip)
                """ for r in range(0, len(codigos_reporte)): """
                
                time.sleep(2)
                controller.Category.fillCategoryDropDown(codigos_reporte[r].codigo_chip_reporte)
                time.sleep(3)
                periodos = controller.Period.getPeriods()
                ultimoPeriodo = periodos[1]['name']

                """ * CICLO WHILE *  PARA RECORRER LOS PERIODOS """
                while True: 
                    p = p + 1
                    """ CONDICIONAL PARA  * TERMINAR *  EL CICLO """
                    if (p > (len(periodos) - 1)):
                        """ NO SE HA ENCONTRADO EL PERIODO ESPECIFICADO  * ALERTA! *  """
                        p = 0
                        alerta(i, r, arregloPeriodos[a]['ano'],arregloPeriodos[a]['mes'], ultimoPeriodo)
                        break
                    periodo = periodos[p]
                    """ VALIDAR SI ESTÄ LA INFORMACION DEL  * PERIODO ACTUAL *  """
                    if (periodo['value'] == arregloPeriodos[a]['value']):
                        p = 0
                        controller.Period.fillPeriodDropDown(periodo['value'])
                        time.sleep(3)
                        formularios = controller.Form.getFormulario()
                        time.sleep(2)
                        existe = queries.Get.buscarAlertaPorCodigoChip(entidades[i].codigo_chip,str(codigos_reporte[r].codigo_chip_reporte),arregloPeriodos[a]['ano'],arregloPeriodos[a]['mes'])
                        """  * VERIFICAR *  SI HAY UN  * EXCEL SUBIDO *  A LA PLATAFORMA CHIP """
                        if (len(formularios) > 0):
                            if (len(existe) == 0):
                                """  * CREAR ALERTA * CON ESTADO 0  * AL DIA! *  """
                                queries.Set.alerta(entidades[i].codigo_chip, codigos_reporte[r].codigo_chip_reporte,
                                arregloPeriodos[a]['ano'],arregloPeriodos[a]['mes'], 0)
                                print(' >', entidades[i].entidad.upper(), '\n', codigos_reporte[r].nombre, '\n',periodo['name'], ' Al Dia! \n---------------------------------\n')
                                
                                """ * DESCARGAR DOCUMENTO EXCEL * """
                                controller.Form.fillFormDropDown(formularios[1]['value'])
                                break
                            else:
                                """  * ACTUALIZAR ALERTA *  CON ESTADO 0  * AL DIA! *  """
                                queries.Update.entidad(arregloPeriodos[a]['ano'],arregloPeriodos[a]['mes'], 0,entidades[i].codigo_chip, codigos_reporte[r].codigo_chip_reporte)
                                print(' >', entidades[i].entidad.upper(), '\n', codigos_reporte[r].nombre, '\n',periodo['name'], ' Al Dia! \n---------------------------------\n')
                                """ * DESCARGAR DOCUMENTO EXCEL * """
                                controller.Form.fillFormDropDown(formularios[1]['value'])
                                """  * IR A CONSULTAS * """
                                time.sleep(2)
                                controller.Page.consultas()
                                break
                        else:
                            """  * ¡NO! HAY FORMULARIO EXCEL | ESTADO 1  * ALERTA !!! *  """
                            alerta(i, r, arregloPeriodos[a]['ano'],arregloPeriodos[a]['mes'], ultimoPeriodo)
                            break

                time.sleep(1)
                r = r + 1
        controller.Page.quit()
        exit()





if __name__ == '__main__':
    main()
