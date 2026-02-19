from config.database import get_connection


def obtener_producto_por_codigo(codigo: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id_producto,
                   nombre,
                   maneja_peso,
                   precio_por_kg,
                   precio_unitario,
                   activo
            FROM productos
            WHERE codigo_barras = %s
        """, (codigo,))

        row = cur.fetchone()

        if not row or not row[5]:
            return None

        return {
            "id_producto": row[0],
            "nombre": row[1],
            "maneja_peso": row[2],
            "precio": float(row[3]) if row[2] else float(row[4])
        }

    finally:
        conn.close()



def obtener_producto_por_id(id_producto: int):
    """
    Busca producto por ID interno (usado en balanza).
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id_producto, nombre, precio
            FROM productos
            WHERE id_producto = %s
        """, (id_producto,))

        row = cur.fetchone()

        if not row:
            return None

        return {
            "id_producto": row[0],
            "nombre": row[1],
            "precio": float(row[2])
        }

    finally:
        conn.close()


def descontar_stock(cur, id_producto, kg=None, unidades=None):
    """
    Descuenta stock usando el cursor activo (misma transacción).
    Lanza error si no hay suficiente stock.
    """

    # Bloquear fila (evita doble venta simultánea)
    cur.execute("""
        SELECT maneja_peso, stock_kg, stock_unidades
        FROM productos
        WHERE id_producto = %s
        FOR UPDATE
    """, (id_producto,))

    row = cur.fetchone()

    if not row:
        raise ValueError("Producto no existe")

    maneja_peso, stock_kg, stock_unidades = row

    # =========================
    # Producto por peso
    # =========================
    if maneja_peso:
        if kg is None:
            raise ValueError("Producto requiere kg")

        if stock_kg < kg:
            raise ValueError("Stock insuficiente (kg)")

        nuevo_stock = stock_kg - kg

        cur.execute("""
            UPDATE productos
            SET stock_kg = %s
            WHERE id_producto = %s
        """, (nuevo_stock, id_producto))

    # =========================
    # Producto por unidad
    # =========================
    else:
        if unidades is None:
            raise ValueError("Producto requiere unidades")

        if stock_unidades < unidades:
            raise ValueError("Stock insuficiente (unidades)")

        nuevo_stock = stock_unidades - unidades

        cur.execute("""
            UPDATE productos
            SET stock_unidades = %s
            WHERE id_producto = %s
        """, (nuevo_stock, id_producto))


def reintegrar_stock(cur, id_producto, kg=None, unidades=None):
    """
    Devuelve stock al inventario.
    """

    cur.execute("""
        SELECT maneja_peso, stock_kg, stock_unidades
        FROM productos
        WHERE id_producto = %s
        FOR UPDATE
    """, (id_producto,))

    row = cur.fetchone()

    if not row:
        raise ValueError("Producto no existe")

    maneja_peso, stock_kg, stock_unidades = row

    if maneja_peso:
        if kg is None:
            raise ValueError("Se requiere kg")

        nuevo_stock = stock_kg + kg

        cur.execute("""
            UPDATE productos
            SET stock_kg = %s
            WHERE id_producto = %s
        """, (nuevo_stock, id_producto))

    else:
        if unidades is None:
            raise ValueError("Se requieren unidades")

        nuevo_stock = stock_unidades + unidades

        cur.execute("""
            UPDATE productos
            SET stock_unidades = %s
            WHERE id_producto = %s
        """, (nuevo_stock, id_producto))
