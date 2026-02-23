from config.database import get_connection

def crear_producto(
    nombre: str,
    id_categoria: int,
    maneja_peso: bool,
    precio: int,
    codigo_barras: str | None = None
):
    """
    Crea un producto de forma segura y validada.
    - maneja_peso = True  -> producto por KG
    - maneja_peso = False -> producto por UNIDAD
    """

    # =========================
    # 1️⃣ VALIDACIONES BASE
    # =========================

    if not nombre or not nombre.strip():
        raise ValueError("El nombre es obligatorio.")

    if precio <= 0:
        raise ValueError("El precio debe ser mayor a cero.")

    if not isinstance(precio, int):
        raise ValueError("El precio debe ser entero.")

    if not isinstance(maneja_peso, bool):
        raise ValueError("maneja_peso debe ser boolean.")

    conn = get_connection()
    cur = conn.cursor()

    try:
        # =========================
        # 2️⃣ VALIDAR CATEGORÍA
        # =========================

        cur.execute(
            "SELECT 1 FROM categorias WHERE id_categoria = %s",
            (id_categoria,)
        )

        if not cur.fetchone():
            raise ValueError("La categoría no existe.")

        # =========================
        # 3️⃣ VALIDAR CÓDIGO DE BARRAS ÚNICO
        # =========================

        if codigo_barras:
            cur.execute(
                "SELECT 1 FROM productos WHERE codigo_barras = %s",
                (codigo_barras,)
            )

            if cur.fetchone():
                raise ValueError("El código de barras ya existe.")

        # =========================
        # 4️⃣ ASIGNAR CAMPOS SEGÚN TIPO
        # =========================

        if maneja_peso:
            precio_por_kg = precio
            precio_unitario = 0
            stock_kg = 0
            stock_unidades = 0
        else:
            precio_por_kg = 0
            precio_unitario = precio
            stock_kg = 0
            stock_unidades = 0

        # =========================
        # 5️⃣ INSERT
        # =========================

        cur.execute("""
            INSERT INTO productos
            (nombre, id_categoria, maneja_peso,
             precio_por_kg, precio_unitario,
             stock_kg, stock_unidades,
             activo, codigo_barras)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE, %s)
            RETURNING id_producto
        """, (
            nombre.strip(),
            id_categoria,
            maneja_peso,
            precio_por_kg,
            precio_unitario,
            stock_kg,
            stock_unidades,
            codigo_barras
        ))

        id_producto = cur.fetchone()[0]

        conn.commit()
        return id_producto

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()