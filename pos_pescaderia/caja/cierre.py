from config.database import get_connection
from auditoria.acciones import registrar_accion
from impresora import imprimir_cierre_caja
from caja.detalle_egresos import obtener_detalle_egresos

def cerrar_caja(id_usuario, monto_real_efectivo):

    if monto_real_efectivo < 0:
        raise Exception("El monto real no puede ser negativo")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id_cierre, id_caja, monto_apertura
            FROM cierre_caja
            WHERE cerrado = FALSE
            ORDER BY id_cierre DESC
            LIMIT 1
            FOR UPDATE
        """)
        row = cur.fetchone()

        if not row:
            raise Exception("No hay caja abierta")

        id_cierre, id_caja, monto_apertura = row

        # ==========================
        # Movimientos
        # ==========================
        cur.execute("""
            SELECT id_metodo,
                   COALESCE(SUM(CASE WHEN tipo='INGRESO' THEN monto ELSE 0 END),0),
                   COALESCE(SUM(CASE WHEN tipo='EGRESO' THEN monto ELSE 0 END),0)
            FROM caja_movimientos
            WHERE id_cierre = %s
            GROUP BY id_metodo
        """, (id_cierre,))

        resultados = cur.fetchall()

        efectivo_ing = efectivo_egr = 0
        tarjeta_ing = sinpe_ing = 0
        total_ingresos = total_egresos = 0

        for id_metodo, ingresos, egresos in resultados:

            total_ingresos += ingresos
            total_egresos += egresos

            if id_metodo == 1:
                efectivo_ing = ingresos
                efectivo_egr = egresos
            elif id_metodo == 2:
                tarjeta_ing = ingresos
            elif id_metodo == 3:
                sinpe_ing = ingresos

        saldo_sistema = monto_apertura + total_ingresos - total_egresos
        efectivo_sistema = monto_apertura + efectivo_ing - efectivo_egr

        diferencia = monto_real_efectivo - efectivo_sistema

        # ==========================
        # Total ventas FINALIZADAS
        # ==========================
        cur.execute("""
            SELECT COALESCE(SUM(total),0)
            FROM ventas
            WHERE id_cierre = %s
            AND estado = 'FINALIZADA'
        """, (id_cierre,))
        total_ventas = cur.fetchone()[0]

        # ==========================
        # Update
        # ==========================
        cur.execute("""
            UPDATE cierre_caja
            SET
                hora_cierre = NOW(),
                total_ingresos = %s,
                total_egresos = %s,
                saldo_sistema = %s,
                total_ventas = %s,
                monto_cierre = %s,
                diferencia = %s,
                efectivo_ingresos = %s,
                efectivo_egresos = %s,
                tarjeta_ingresos = %s,
                sinpe_ingresos = %s,
                cerrado = TRUE
            WHERE id_cierre = %s
        """, (
            total_ingresos,
            total_egresos,
            saldo_sistema,
            total_ventas,
            monto_real_efectivo,
            diferencia,
            efectivo_ing,
            efectivo_egr,
            tarjeta_ing,
            sinpe_ing,
            id_cierre
        ))

        conn.commit()

    except:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {
        "id_cierre": id_cierre,
        "monto_apertura": monto_apertura,
        "total_ventas": total_ventas,
        "saldo_sistema": saldo_sistema,
        "efectivo_sistema": efectivo_sistema,
        "monto_cierre": monto_real_efectivo,
        "diferencia": diferencia
    }



