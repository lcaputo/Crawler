from resources import queries, controller
import time, json

""" VARIABLES """
entidades = queries.Get.codigoChip()
codigos_reporte = queries.Get.codigoReporte()
periodo_actual = queries.Get.periodoActual()


class main():

    def alerta(i,j):
        queries.Set.alerta(entidades[i].codigo_chip, codigos_reporte[j].codigo_chip_reporte, periodo_actual[1],periodo_actual[0], 1)
        return print('Alerta ', entidades[i].entidad, ' - ', codigos_reporte[j].nombre,
        '\nEl periodo actual no ha sido elaborado \nÚltima actulización : ', ultimoPeriodo,'\n\n')

    for i in range( 0, len(entidades) ):
        controller.Entity.fillEntityInput(entidades[i].codigo_chip)
        time.sleep(2)
        for j in range( 0, len(codigos_reporte) ):
            controller.Category.fillCategoryDropDown(codigos_reporte[j].codigo_chip_reporte)
            time.sleep(3)
            periodos = controller.Period.getPeriods()
            ultimoPeriodo = periodos[1]['name']
            for p in range( 0, len(periodos) ):
                if ( periodos[p]['value'] == periodo_actual[2] ):
                    periodo = periodos[p]

                    controller.Period.fillPeriodDropDown(periodo['value'])
                    time.sleep(3)
                    formularios = controller.Form.getFormulario()
                    time.sleep(2)

                    existe = queries.Get.buscarAlertaPorCodigoChip(entidades[i].codigo_chip,
                        str(codigos_reporte[j].codigo_chip_reporte),periodo_actual[1],periodo_actual[0])

                    if ( len(formularios) > 0 ):
                        if ( len(existe) == 0 ):
                            queries.Set.alerta(entidades[i].codigo_chip, codigos_reporte[j].codigo_chip_reporte,
                                               periodo_actual[1], periodo_actual[0], 0)
                        else:
                            queries.Update.entidad(periodo_actual[1], periodo_actual[0], 0, entidades[i].codigo_chip, codigos_reporte[j].codigo_chip_reporte)
                        print(entidades[i].entidad, '\n' ,codigos_reporte[j].nombre, '\n' ,periodo['name'], ' Al Dia! ' '\n---------------------------------\n')
                    else:
                        alerta(i, j)
                    break
            time.sleep(1)
    controller.Page.quit()
    exit()





if __name__ == '__main__':
    main()
