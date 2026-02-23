from ventas.ticket import imprimir_ticket, obtener_datos_ticket


def reimprimir_ticket(id_venta):

    datos = obtener_datos_ticket(id_venta)

    if not datos:
        print("Venta no encontrada")
        return

    imprimir_ticket(
        id_venta=datos["id"],
        cajero=datos["cajero"],
        items=datos["items"],
        total=datos["total"],
        pagos=datos["pagos"],
        vuelto=datos["vuelto"]
    )

