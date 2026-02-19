from caja.apertura import abrir_caja
from caja.cierre import cerrar_caja, resumen_cierre, resumen_por_metodo
from reportes.ticket_cierre import imprimir_cierre_caja
from reportes.cierre_caja import ventas_por_metodo
from ventas.agregar_producto_balanza import agregar_producto_balanza
from ventas.pagos import capturar_pagos
from ventas.venta import (
    registrar_venta_completa,
    obtener_pagos_venta,
    ajustar_pagos_con_vuelto
)

from ventas.ticket import imprimir_ticket


ID_USUARIO = 1
MONTO_APERTURA = 20000


def flujo_venta_balanza(id_cierre):
    detalles = []

    # =========================
    # Escaneo de productos
    # =========================
    while True:
        opcion = input("[S] Escanear | [C] Cobrar: ").upper()

        if opcion == "S":
            detalles = agregar_producto_balanza(detalles)

        elif opcion == "C":
            if not detalles:
                print("⚠ No hay productos")
                continue
            break

    # =========================
    # Calcular total
    # =========================
    total = sum(
        d["kg"] * d["precio"] if d["kg"] is not None
        else d["unidades"] * d["precio"]
        for d in detalles
    )

    print(f"Total a pagar: ₡{total:,.0f}")

    # =========================
    # Capturar pagos
    # =========================
    pagos = capturar_pagos(total)

    # =========================
    # Ajustar pagos + vuelto
    # =========================
    pagos_ajustados, vuelto = ajustar_pagos_con_vuelto(total, pagos)

    # =========================
    # Registrar venta
    # =========================
    id_venta, total = registrar_venta_completa(
        id_usuario=ID_USUARIO,
        id_caja=id_caja,
        detalles=detalles,
        pagos=pagos_ajustados
    )

    # =========================
    # Pagos reales desde BD
    # =========================
    pagos_reales = obtener_pagos_venta(id_venta)

    # =========================
    # Ticket
    # =========================
    imprimir_ticket(
        id_venta=id_venta,
        cajero=f"Usuario {ID_USUARIO}",
        items=detalles,
        total=total,
        pagos=pagos_reales,
        vuelto=vuelto
    )

    if vuelto > 0:
        print(f"Vuelto: ₡{vuelto:,.0f}")

    print(f"✅ Venta realizada: ₡{total:,.0f}")


def main():

    # =========================
    # Apertura de caja
    # =========================
    id_cierre = abrir_caja(
        id_usuario=ID_USUARIO,
        monto_apertura=MONTO_APERTURA
    )

    # =========================
    # Ventas
    # =========================
    flujo_venta_balanza(id_cierre)

    # =========================
    # Resumen general
    # =========================
    resumen = resumen_cierre()
    print("Resumen cierre:", resumen)

    # =========================
    # Cierre de caja
    # =========================
    resultado = cerrar_caja(
    id_usuario=ID_USUARIO,
    monto_real_efectivo=150000
)

imprimir_cierre_caja(
    id_cierre=resultado["id_cierre"],
    id_usuario=ID_USUARIO,
    monto_apertura=resultado["monto_apertura"],
    total_ventas=resultado["total_ventas"],
    total_ingresos=resultado["total_ingresos"],
    total_egresos=resultado["total_egresos"],
    saldo_sistema=resultado["saldo_sistema"],
    efectivo_sistema=resultado["efectivo_sistema"],
    monto_cierre=resultado["monto_cierre"],
    diferencia=resultado["diferencia"],
    pagos=[
        {"metodo": "EFECTIVO", "total": resultado["efectivo"]},
        {"metodo": "TARJETA", "total": resultado["tarjeta"]},
        {"metodo": "SINPE", "total": resultado["sinpe"]}
    ],
    egresos=resultado["detalle_egresos"]
)



if __name__ == "__main__":
    main()
