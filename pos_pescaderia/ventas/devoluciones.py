from datetime import datetime
from config.database import get_connection
from ventas.productos import reintegrar_stock
from auditoria.acciones import registrar_accion
from impresora.devoluciones import imprimir_devolucion


def registrar_devolucion(
    id_usuario,
    id_caja,
    id_venta,
    id_producto,
    kg=None,
    unidades=None,
    motivo="SIN MOTIVO"
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # =========================
        # 1️⃣ Bloquear detalle venta
        # =========================
        cur.execute("""
            SELECT kg, unidades, subtotal
            FROM detalle_ventas
            WHERE id_venta = %s
            AND id_producto = %s
            FOR UPDATE
        """, (id_venta, id_producto))

        venta = cur.fetchone()

        if not venta:
            raise ValueError("Producto no pertenece a la venta")

        kg_vendido, unidades_vendidas, subtotal = venta

        # =========================
        # 2️⃣ Validar cantidades
        # =========================
        if kg is not None:
            if kg_vendido is None or kg > kg_vendido:
                raise ValueError("Cantidad kg inválida")

        if unidades is not None:
            if unidades_vendidas is None or unidades > unidades_vendidas:
                raise ValueError("Cantidad unidades inválida")

        # =========================
        # 3️⃣ Registrar devolución
        # =========================
        cur.execute("""
            INSERT INTO devoluciones
            (id_venta, id_producto, fecha, motivo, monto)
            VALUES (%s, %s, NOW(), %s, %s)
        """, (
            id_venta,
            id_producto,
            motivo,
            subtotal
        ))

        # =========================
        # 4️⃣ Reintegrar stock
        # =========================
        reintegrar_stock(
            cur,
            id_producto,
            kg=kg,
            unidades=unidades
        )

        # =========================
        # 5️⃣ Movimiento caja
        # =========================
        cur.execute("""
            INSERT INTO caja_movimientos
            (id_caja, tipo, concepto, monto, id_venta)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_caja,
            "EGRESO",
            f"DEVOLUCION VENTA {id_venta}",
            subtotal,
            id_venta
        ))

        conn.commit()

        # =========================
        # 6️⃣ Auditoría
        # =========================
        registrar_accion(
            id_usuario,
            "DEVOLUCION",
            f"Venta #{id_venta} devolución ₡{subtotal:,.0f}"
        )

        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
