from config.database import get_connection
from db.queries import fetch_one



def obtener_resumen_cierre(id_cierre):

    resumen = fetch_one("""
        SELECT
            monto_apertura,
            total_ventas,
            total_ingresos,
            total_egresos,
            saldo_sistema,
            monto_cierre,
            diferencia,
            efectivo_ingresos,
            efectivo_egresos,
            tarjeta_ingresos,
            sinpe_ingresos
        FROM cierre_caja
        WHERE id_cierre = %s
    """, (id_cierre,))

    return resumen


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



def calcular_total_ventas(id_cierre):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM ventas
        WHERE id_cierre = %s
    """, (id_cierre,))

    total = cur.fetchone()[0]
    conn.close()

    return total


def ventas_por_metodo(id_cierre):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            mp.nombre,
            SUM(vp.monto)
        FROM ventas_pagos vp
        JOIN ventas v ON v.id_venta = vp.id_venta
        JOIN metodos_pago mp ON mp.id_metodo = vp.id_metodo
        WHERE v.id_cierre = %s
        GROUP BY mp.nombre
        ORDER BY mp.nombre
    """, (id_cierre,))

    datos = cur.fetchall()
    conn.close()

    return datos

