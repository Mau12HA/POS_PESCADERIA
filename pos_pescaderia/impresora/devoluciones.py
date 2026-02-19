from datetime import datetime
from escpos.printer import Usb

# Epson TM-U220
VENDOR_ID = 0x04b8
PRODUCT_ID = 0x0202


def imprimir_devolucion(
    id_venta,
    id_usuario,
    items,
    total_devuelto,
    motivo="DEVOLUCIÓN"
):
    """
    items = [
        {
            "nombre": "Pargo rojo",
            "cantidad": 1.250,
            "precio": 4500,
            "subtotal": 5625
        }
    ]
    """

    p = Usb(VENDOR_ID, PRODUCT_ID)
    fecha = datetime.now().strftime("%d-%m-%Y %H:%M")

    # ======================
    # ENCABEZADO
    # ======================
    p.set(align="center", bold=True, width=2, height=2)
    p.text("DEVOLUCIÓN\n")

    p.set(align="center", bold=False, width=1, height=1)
    p.text("PESCADERÍA WILLIAM\n")
    p.text("=" * 32 + "\n")

    # ======================
    # DATOS
    # ======================
    p.set(align="left")
    p.text(f"Venta   #: {id_venta}\n")
    p.text(f"Cajero  : {id_usuario}\n")
    p.text(f"Fecha   : {fecha}\n")
    p.text(f"Motivo  : {motivo}\n")
    p.text("-" * 32 + "\n")

    # ======================
    # DETALLE
    # ======================
    p.set(bold=True)
    p.text("DETALLE DEVUELTO\n")
    p.set(bold=False)

    for i in items:
        p.set(bold=True)
        p.text(i["nombre"][:32] + "\n")

        p.set(bold=False)
        linea = (
            f"{i['cantidad']:>6.3f} x "
            f"₡{i['precio']:>7,.0f} "
            f"₡{i['subtotal']:>8,.0f}\n"
        )
        p.text(linea)

        p.text("-" * 32 + "\n")

    # ======================
    # TOTAL
    # ======================
    p.set(align="right", bold=True, width=2, height=2)
    p.text(f"TOTAL ₡{total_devuelto:,.0f}\n")

    p.set(align="left", bold=False, width=1, height=1)
    p.text("=" * 32 + "\n")

    # ======================
    # PIE
    # ======================
    p.set(align="center")
    p.text("DOCUMENTO DE DEVOLUCIÓN\n")
    p.text("Conserve este comprobante\n")
    p.text("\n")

    # ======================
    # CORTE
    # ======================
    p.cut()
