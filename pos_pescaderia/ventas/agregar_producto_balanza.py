from lector.scanner import leer_scanner
from balanza.ean_parser import interpretar_codigo_barras
from ventas.productos import (
    obtener_producto_por_codigo,
    obtener_producto_por_id
)


def agregar_producto_balanza(detalles):

    print("📦 Escanee el producto...")
    codigo = leer_scanner()
    resultado = interpretar_codigo_barras(codigo)

    if resultado["tipo"] == "invalido":
        print("❌ Código inválido")
        return detalles

    # =========================
    # BALANZA
    # =========================
    if resultado["tipo"] == "balanza_precio":

        data = resultado["data"]
        producto = obtener_producto_por_id(data["id_producto"])

        if not producto:
            print("❌ Producto no encontrado")
            return detalles

        if producto["tipo_venta"] != "KG":
            print("❌ Este producto no se vende por KG.")
            return detalles

        precio_total = data["precio_total"]
        precio_kg = producto["precio"]

        if precio_kg <= 0:
            print("❌ Precio por KG inválido.")
            return detalles

        kg = round(precio_total / precio_kg, 3)

        if kg <= 0:
            print("❌ Cantidad inválida.")
            return detalles

        detalle = {
            "id_producto": producto["id_producto"],
            "nombre": producto["nombre"],
            "kg": kg,
            "unidades": None,
            "precio": precio_kg,
            "subtotal": precio_total
        }

        detalles.append(detalle)

        print(
            f"✔ {producto['nombre']} "
            f"{kg:.3f} kg x ₡{precio_kg:,.0f} = ₡{precio_total:,.0f}"
        )

        return detalles

    # =====================================================
    # PRODUCTO NORMAL (DEBE SER UNIDAD)
    # =====================================================
    if resultado["tipo"] == "normal":

        producto = obtener_producto_por_codigo(resultado["data"]["codigo"])

        if not producto:
            print("❌ Producto no encontrado")
            return detalles

        if producto["tipo_venta"] != "UNIDAD":
            print("❌ Este producto se vende por KG. Use balanza.")
            return detalles

        precio = producto["precio"]

        if precio <= 0:
            print("❌ Precio inválido.")
            return detalles

        detalle = {
            "id_producto": producto["id_producto"],
            "nombre": producto["nombre"],
            "kg": None,
            "unidades": 1,  # siempre entero
            "precio": precio,
            "subtotal": precio
        }

        detalles.append(detalle)

        print(f"✔ {producto['nombre']} ₡{precio:,.0f}")

        return detalles

