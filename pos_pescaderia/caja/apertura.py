from config.database import get_connection
from auditoria.acciones import registrar_accion

def abrir_caja(id_usuario, monto_apertura):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cierre_caja (fecha, hora_apertura, monto_apertura, cerrado)
        VALUES (CURRENT_DATE, CURRENT_TIMESTAMP, %s, FALSE)
        RETURNING id_cierre
    """, (monto_apertura,))

    id_cierre = cur.fetchone()[0]
    conn.commit()
    conn.close()

    registrar_accion(id_usuario, "APERTURA_CAJA", f"Monto: {monto_apertura}")
    return id_cierre
