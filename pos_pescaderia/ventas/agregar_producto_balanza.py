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

        precio_total = data["precio_total"]
        precio_kg = producto["precio"]

        kg = round(precio_total / precio_kg, 3)

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

    # =========================
    # PRODUCTO NORMAL
    # =========================
    if resultado["tipo"] == "normal":

        producto = obtener_producto_por_codigo(resultado["data"]["codigo"])

        if not producto:
            print("❌ Producto no encontrado")
            return detalles

        detalle = {
            "id_producto": producto["id_producto"],
            "nombre": producto["nombre"],
            "kg": None,
            "unidades": 1,
            "precio": producto["precio"],
            "subtotal": producto["precio"]
        }

        detalles.append(detalle)

        print(f"✔ {producto['nombre']} ₡{producto['precio']:,.0f}")

        return detalles


