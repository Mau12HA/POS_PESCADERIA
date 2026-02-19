from datetime import datetime
from impresora import imprimir


from datetime import datetime


def imprimir_cierre_caja(
    id_cierre,
    id_usuario,
    monto_apertura,
    total_ventas,
    total_ingresos,
    total_egresos,
    saldo_sistema,
    efectivo_sistema,
    monto_cierre,
    diferencia,
    pagos,
    egresos
):

    ancho = 40  # ticket 80mm

    def linea():
        return "-" * ancho

    def money(valor):
        return f"₡{valor:,.0f}"

    texto = ""
    texto += linea() + "\n"
    texto += "        CIERRE DE CAJA\n"
    texto += linea() + "\n"
    texto += f"Cierre #: {id_cierre}\n"
    texto += f"Usuario  : {id_usuario}\n"
    texto += f"Fecha    : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    texto += linea() + "\n"

    texto += f"Apertura        {money(monto_apertura).rjust(15)}\n"
    texto += linea() + "\n"

    texto += "VENTAS POR METODO\n"
    texto += linea() + "\n"

    for metodo in pagos:
        nombre = metodo["metodo"]
        monto = metodo["total"]
        texto += f"{nombre:<20}{money(monto).rjust(20-len(nombre))}\n"

    texto += linea() + "\n"

    texto += f"Total Ventas    {money(total_ventas).rjust(15)}\n"
    texto += f"Ingresos        {money(total_ingresos).rjust(15)}\n"
    texto += f"Egresos         {money(total_egresos).rjust(15)}\n"
    texto += linea() + "\n"


    texto += linea() + "\n"
    texto += "DETALLE DE EGRESOS\n"
    texto += linea() + "\n"

    if not egresos:
        texto += "No hubo egresos\n"
    else:
        for e in egresos:
            concepto = e["concepto"][:20]
            monto = money(e["monto"])
            texto += f"{concepto:<20}{monto.rjust(20-len(concepto))}\n"

    texto += linea() + "\n"
    texto += f"Total Egresos    {money(total_egresos).rjust(15)}\n"
    

    texto += f"Saldo Sistema   {money(saldo_sistema).rjust(15)}\n"
    texto += f"Efectivo Sistema{money(efectivo_sistema).rjust(15)}\n"
    texto += linea() + "\n"

    texto += f"Efectivo Real   {money(monto_cierre).rjust(15)}\n"
    texto += linea() + "\n"

    if diferencia == 0:
        texto += "DIFERENCIA: 0 (CUADRADA)\n"
    elif diferencia > 0:
        texto += f"SOBRANTE: {money(diferencia)}\n"
    else:
        texto += f"FALTANTE: {money(diferencia)}\n"

    texto += linea() + "\n"
    texto += "   *** FIN CIERRE DE CAJA ***\n\n\n"

    imprimir(texto)  # Tu función real de impresión
