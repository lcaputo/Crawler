SELECT E.entidad, A.periodo_anno, A.periodo_meses, E.Telefonos, E.correo
FROM entidades E, alertas_reportes A
WHERE E.codigo_chip = A.codigo_chip and A.estado = 1