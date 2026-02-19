from config.database import get_connection


def obtener_detalle_egresos(id_cierre):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT concepto, monto, fecha
        FROM caja_movimientos
        WHERE id_cierre = %s
        AND tipo = 'EGRESO'
        AND fecha >= (SELECT fecha + hora_apertura FROM cierre_caja WHERE id_cierre = %s)
        ORDER BY fecha
    """, (id_cierre, id_cierre))

    rows = cur.fetchall()
    conn.close()

    egresos = []

    for concepto, monto, fecha in rows:
        egresos.append({
            "concepto": concepto,
            "monto": monto,
            "fecha": fecha
        })

    return egresos
