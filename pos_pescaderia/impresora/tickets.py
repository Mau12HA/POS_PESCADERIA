from datetime import datetime
from impresora import imprimir

ANCHO_PAPEL = 32


def imprimir_ticket(id_venta, cajero, items, total, pagos, vuelto=0):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    ticket = []

    # ===== ENCABEZADO =====
    ticket.append(centrar("PESCADERÍA WILLIAM"))
    ticket.append(centrar("ZARAGOZA, PALMARES"))
    ticket.append("=" * ANCHO_PAPEL)

    ticket.append(f"Ticket #: {id_venta}")
    ticket.append(f"Cajero : {cajero}")
    ticket.append(f"Fecha  : {ahora}")
    ticket.append("-" * ANCHO_PAPEL)

    # ===== DETALLE =====
    for item in items:
        nombre = item["nombre"]
        cantidad = item["cantidad"]
        precio = item["precio"]
        subtotal = item["subtotal"]

        ticket.append(nombre[:ANCHO_PAPEL])

        # Cantidad
        ticket.append(f" {cantidad:>6.3f} kg")

        # Precio por KG resaltado
        ticket.append(f" PRECIO KG: ₡{precio:>7,.0f}")

        # Subtotal alineado a la derecha
        ticket.append(f"{'':>16}₡{subtotal:>10,.0f}")

        # Separador por producto
        ticket.append("-" * ANCHO_PAPEL)

    # ===== TOTAL =====
    ticket.append(f"{'TOTAL':<16} ₡{total:>14,.0f}")

    # ===== PAGOS =====
    ticket.append("-" * ANCHO_PAPEL)
    ticket.append("FORMAS DE PAGO")

    for p in pagos:
        metodo = "EFECTIVO" if p["id_metodo"] == 1 else "SINPE"
        ticket.append(f"{metodo:<12} ₡{p['monto']:>14,.0f}")

    if vuelto > 0:
        ticket.append("-" * ANCHO_PAPEL)
        ticket.append(f"VUELTO{'':>9} ₡{vuelto:>14,.0f}")

    ticket.append("=" * ANCHO_PAPEL)
    ticket.append(centrar("GRACIAS POR SU COMPRA"))
    ticket.append("\n\n")

    imprimir("\n".join(ticket))


def centrar(texto):
    return texto.center(ANCHO_PAPEL)