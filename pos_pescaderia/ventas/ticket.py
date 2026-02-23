from impresora.tickets import imprimir_ticket
from config.database import get_connection
import psycopg2.extras


def imprimir_ticket_venta(*args, **kwargs):
    imprimir_ticket(*args, **kwargs)



def obtener_datos_ticket(id_venta):

    conn = get_connection()

    try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 1️⃣ Cabecera
            cur.execute("""
                SELECT v.id_venta,
                    v.total,
                    u.nombre AS cajero
                FROM ventas v
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                WHERE v.id_venta = %s
            """, (id_venta,))

            venta = cur.fetchone()

            if not venta:
                conn.close()
                return None

            # 2️⃣ Items
            cur.execute("""
                SELECT p.nombre,
                    d.cantidad_kg,
                    d.cantidad_unidades,
                    d.precio_unitario,
                    d.subtotal
                FROM detalle_ventas d
                JOIN productos p ON d.id_producto = p.id_producto
                WHERE d.id_venta = %s
            """, (id_venta,))

            items = cur.fetchall()

            # 3️⃣ Pagos
            cur.execute("""
                SELECT m.nombre,
                    p.monto
                FROM pagos p
                JOIN metodos_pago m ON p.id_metodo = m.id_metodo
                WHERE p.id_venta = %s
            """, (id_venta,))

            pagos = cur.fetchall()
    finally:
        conn.close()

    # 4️⃣ Calcular vuelto (si aplica)
    total_pagado = sum(p["monto"] for p in pagos)
    vuelto = total_pagado - venta["total"]

    # 5️⃣ Construir estructura que espera reimpresión
    return {
        "id": venta["id_venta"],
        "cajero": venta["cajero"],
        "items": items,
        "total": venta["total"],
        "pagos": pagos,
        "vuelto": vuelto if vuelto > 0 else 0
    }
