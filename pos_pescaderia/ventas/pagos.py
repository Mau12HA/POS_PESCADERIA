def capturar_pagos(total):
    pagos = []
    restante = total

    while restante > 0:
        print(f"\nPendiente: ₡{restante:,.0f}")
        print("[1] Efectivo")
        print("[2] SINPE")

        metodo = int(input("Método de pago: "))
        monto = float(input("Monto: "))

        if monto <= 0:
            print("Monto inválido")
            continue

        if monto > restante:
            print("El monto excede el pendiente")
            continue

        pagos.append({
            "id_metodo": metodo,
            "monto": monto
        })

        restante -= monto

    return pagos
