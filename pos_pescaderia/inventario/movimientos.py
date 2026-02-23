def ingresar_stock(id_producto, kg=None, unidades=None, motivo="ENTRADA MANUAL"):

    conn = get_connection()
    cur = conn.cursor()

    # Obtener tipo venta
    cur.execute("SELECT tipo_venta FROM productos WHERE id = %s", (id_producto,))
    row = cur.fetchone()

    if not row:
        raise ValueError("Producto no existe")

    tipo_venta = row[0]

    if tipo_venta == "KG":
        if not kg or kg <= 0:
            raise ValueError("Debe ingresar KG válido")

        cur.execute("""
            UPDATE productos
            SET stock_kg = stock_kg + %s
            WHERE id = %s
        """, (kg, id_producto))

        cur.execute("""
            INSERT INTO inventario_movimientos
            (id_producto, tipo, cantidad_kg, motivo)
            VALUES (%s, 'ENTRADA', %s, %s)
        """, (id_producto, kg, motivo))

    elif tipo_venta == "UNIDAD":
        if not unidades or unidades <= 0:
            raise ValueError("Debe ingresar unidades válidas")

        cur.execute("""
            UPDATE productos
            SET stock_unidades = stock_unidades + %s
            WHERE id = %s
        """, (unidades, id_producto))

        cur.execute("""
            INSERT INTO inventario_movimientos
            (id_producto, tipo, cantidad_unidades, motivo)
            VALUES (%s, 'ENTRADA', %s, %s)
        """, (id_producto, unidades, motivo))

    conn.commit()
    conn.close()