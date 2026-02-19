from config.database import get_connection
from auditoria.acciones import registrar_accion
from ventas.productos import descontar_stock


def registrar_venta_completa(
    id_usuario,
    id_caja,
    detalles,
    pagos
):
    """
    Registra venta completa con:
    - Cabecera
    - Detalle
    - Pagos
    - Movimiento de caja por método
    """

    if not detalles:
        raise ValueError("No se puede registrar una venta sin productos")

    if not pagos:
        raise ValueError("La venta no tiene pagos registrados")

    conn = get_connection()
    cur = conn.cursor()

    try:
        # =========================
        # 🔒 0️⃣ Validar cierre abierto
        # =========================
        cur.execute("""
            SELECT id_cierre, id_caja
            FROM cierre_caja
            WHERE cerrado = FALSE
            ORDER BY id_cierre DESC
            LIMIT 1
        """)

        cierre_row = cur.fetchone()

        if not cierre_row:
            raise Exception("No hay caja abierta. No se puede registrar ventas.")

        id_cierre, id_caja_abierta = cierre_row

        if id_caja_abierta != id_caja:
            raise Exception("La caja enviada no coincide con la caja abierta.")

        # =========================
        # 1️⃣ Calcular total
        # =========================
        total = 0

        for d in detalles:
            precio = d["precio"]

            if d["kg"] is not None:
                subtotal = d["kg"] * precio
            else:
                subtotal = d["unidades"] * precio

            d["subtotal"] = subtotal
            total += subtotal

        # =========================
        # 2️⃣ Validar pagos
        # =========================
        total_pagos = sum(p["monto"] for p in pagos)

        if abs(total_pagos - total) > 1:
            raise ValueError(
                f"Pagos ₡{total_pagos:,.0f} no coinciden con total ₡{total:,.0f}"
            )

        # =========================
        # 3️⃣ Insertar venta
        # =========================
        cur.execute("""
            INSERT INTO ventas (id_usuario, id_cierre, total)
            VALUES (%s, %s, %s)
            RETURNING id_venta
        """, (id_usuario, id_cierre, total))

        id_venta = cur.fetchone()[0]

        # =========================
        # 4️⃣ Insertar detalle + descontar stock
        # =========================
        for d in detalles:

            kg = d["kg"]
            unidades = d["unidades"]
            precio = d["precio"]
            subtotal = d["subtotal"]

            cur.execute("""
                INSERT INTO detalle_ventas
                (id_venta, id_producto, kg, unidades, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_venta,
                d["id_producto"],
                kg,
                unidades,
                precio,
                subtotal
            ))

            descontar_stock(
                cur,
                d["id_producto"],
                kg=kg,
                unidades=unidades
            )

        # =========================
        # 5️⃣ Insertar pagos
        # =========================
        for p in pagos:
            cur.execute("""
                INSERT INTO pagos (id_venta, id_metodo, monto)
                VALUES (%s, %s, %s)
            """, (
                id_venta,
                p["id_metodo"],
                p["monto"]
            ))

        # =========================
        # 6️⃣ Movimiento caja por método
        # =========================
        for p in pagos:
            cur.execute("""
                INSERT INTO caja_movimientos
                (id_caja,id_cierre, tipo, concepto, monto, id_venta, id_metodo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                id_caja,
                id_cierre,
                "INGRESO",
                f"VENTA {id_venta}",
                p["monto"],
                id_venta,
                p["id_metodo"]
            ))

        # =========================
        # 7️⃣ Commit final
        # =========================
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    # =========================
    # 8️⃣ Auditoría (fuera transacción)
    # =========================
    registrar_accion(
        id_usuario,
        "VENTA",
        f"Venta #{id_venta} registrada por ₡{total:,.0f}"
    )

    return id_venta, total
