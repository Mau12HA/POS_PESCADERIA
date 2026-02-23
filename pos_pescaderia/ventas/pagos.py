METODOS_PAGO = {
    1: "Efectivo",
    2: "SINPE"
}

def capturar_pagos(total):

    if total <= 0:
        return [], 0

    pagos = []
    total_pagado = 0
    restante = total

    while restante > 0:

        print(f"\nPendiente: ₡{restante:,}")
        print("[1] Efectivo")
        print("[2] SINPE")

        # ==========================
        # Validar método
        # ==========================
        try:
            metodo = int(input("Método de pago: "))
        except ValueError:
            print("❌ Método inválido")
            continue

        if metodo not in METODOS_PAGO:
            print("❌ Método no válido")
            continue

        # ==========================
        # Validar monto
        # ==========================
        try:
            monto = int(input("Monto: "))
        except ValueError:
            print("❌ Monto inválido")
            continue

        if monto <= 0:
            print("❌ El monto debe ser mayor a cero")
            continue

        # ==========================
        # Control de exceso
        # ==========================
        if monto > restante and metodo != 1:
            print("❌ Solo se permite excedente en pago en efectivo")
            continue

        pagos.append({
            "id_metodo": metodo,
            "monto": monto
        })

        total_pagado += monto
        restante = total - total_pagado

        if restante < 0:
            restante = 0

    vuelto = total_pagado - total

    if vuelto > 0:
        print(f"\n💵 Vuelto: ₡{vuelto:,}")

    return pagos, vuelto
