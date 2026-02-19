ROLES = {
    "admin": [
        "abrir_caja",
        "cerrar_caja",
        "venta",
        "devolucion",
        "reportes",
        "usuarios"
    ],
    "cajero": [
        "venta",
        "devolucion"
    ]
}

def tiene_permiso(rol, permiso):
    return permiso in ROLES.get(rol, [])
