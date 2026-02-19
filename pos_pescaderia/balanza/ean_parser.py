# =========================
# Validación EAN-13
# =========================

def validar_ean13(codigo: str) -> bool:
    if len(codigo) != 13 or not codigo.isdigit():
        return False

    digitos = [int(d) for d in codigo]

    suma_impares = sum(digitos[i] for i in range(0, 12, 2))
    suma_pares = sum(digitos[i] for i in range(1, 12, 2)) * 3

    total = suma_impares + suma_pares
    digito_calculado = (10 - (total % 10)) % 10

    return digito_calculado == digitos[12]


# =========================
# Parser balanza precio
# =========================

def parsear_ean_precio(codigo: str):
    id_producto = int(codigo[2:7])
    precio_total = int(codigo[7:12])

    return {
        "id_producto": id_producto,
        "precio_total": precio_total
    }


# =========================
# Parser balanza peso (futuro)
# =========================

def parsear_ean_peso(codigo: str):
    id_producto = int(codigo[2:7])
    gramos = int(codigo[7:12])
    peso_kg = gramos / 1000

    return {
        "id_producto": id_producto,
        "peso_kg": peso_kg
    }


# =========================
# Función central inteligente
# =========================

def interpretar_codigo_barras(codigo: str):
    """
    Detecta automáticamente:
    - Balanza por precio
    - Producto normal
    - Código inválido
    """

    if not validar_ean13(codigo):
        return {"tipo": "invalido", "data": None}

    # Prefijos balanza
    if codigo.startswith(("20", "21", "22", "23")):
        return {
            "tipo": "balanza_precio",
            "data": parsear_ean_precio(codigo)
        }

    # Producto normal
    return {
        "tipo": "normal",
        "data": {"codigo": codigo}
    }
