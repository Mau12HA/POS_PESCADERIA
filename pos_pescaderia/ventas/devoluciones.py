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

    if kg is None and unidades is None:
        raise ValueError("Debe indicar kg o unidades a devolver")

    conn = get_connection()
    cur = conn.cursor()

    monto = 0

    try:

        # =========================
        # 0️⃣ Validar cierre abierto
        # =========================
        cur.execute("""
            SELECT id_cierre, id_caja
            FROM cierre_caja
            WHERE cerrado = FALSE
            ORDER BY id_cierre DESC
            LIMIT 1
            FOR UPDATE
        """)

        cierre = cur.fetchone()

        if not cierre:
            raise Exception("No hay caja abierta")

        id_cierre, id_caja_abierta = cierre

        if id_caja_abierta != id_caja:
            raise Exception("Caja no coincide con la abierta")

        # =========================
        # 1️⃣ Bloquear detalle venta
        # =========================
        cur.execute("""
            SELECT cantidad_kg,
                   cantidad_unidades,
                   precio_unitario
            FROM detalle_ventas
            WHERE id_venta = %s
            AND id_producto = %s
            FOR UPDATE
        """, (id_venta, id_producto))

        row = cur.fetchone()

        if not row:
            raise ValueError("Producto no pertenece a la venta")

        kg_vendido, unidades_vendidas, precio_unitario = row

        # =========================
        # 2️⃣ Validar cantidades
        # =========================
        if kg is not None:
            if kg_vendido is None or kg <= 0 or kg > kg_vendido:
                raise ValueError("Cantidad kg inválida")

        if unidades is not None:
            if unidades_vendidas is None or unidades <= 0 or unidades > unidades_vendidas:
                raise ValueError("Cantidad unidades inválida")

        # =========================
        # 3️⃣ Calcular monto devolución
        # =========================
        if kg is not None:
            monto = kg * precio_unitario
        else:
            monto = unidades * precio_unitario

        # =========================
        # 4️⃣ Registrar devolución
        # =========================
        cur.execute("""
            INSERT INTO devoluciones
            (id_venta, id_producto, fecha, motivo, monto)
            VALUES (%s, %s, NOW(), %s, %s)
        """, (
            id_venta,
            id_producto,
            motivo,
            monto
        ))

        # =========================
        # 5️⃣ Actualizar detalle venta
        # =========================
        nuevo_kg = None
        nuevo_unidades = None

        if kg is not None:
            nuevo_kg = kg_vendido - kg

        if unidades is not None:
            nuevo_unidades = unidades_vendidas - unidades

        cur.execute("""
            UPDATE detalle_ventas
            SET cantidad_kg = COALESCE(%s, cantidad_kg),
                cantidad_unidades = COALESCE(%s, cantidad_unidades)
            WHERE id_venta = %s
            AND id_producto = %s
        """, (
            nuevo_kg,
            nuevo_unidades,
            id_venta,
            id_producto
        ))

        # =========================
        # 6️⃣ Reintegrar stock
        # =========================
        reintegrar_stock(
            cur,
            id_producto,
            kg=kg,
            unidades=unidades
        )

        # =========================
        # 7️⃣ Movimiento caja
        # =========================
        cur.execute("""
            INSERT INTO caja_movimientos
            (id_caja, id_cierre, tipo, concepto, monto, id_venta)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            id_caja,
            id_cierre,
            "EGRESO",
            f"DEVOLUCION VENTA {id_venta}",
            monto,
            id_venta
        ))

        
         # =========================
         # 8️⃣ Auditoría
         # =========================
        registrar_accion(
                id_usuario,
                "DEVOLUCION",
                f"Venta #{id_venta} devolución ₡{monto:,.0f}"
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return True