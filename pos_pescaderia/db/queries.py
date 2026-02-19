INSERT_VENTA = """
INSERT INTO ventas (id_usuario, id_cierre, total)
VALUES (%s, %s, %s)
RETURNING id_venta
"""

INSERT_DETALLE = """
INSERT INTO detalle_ventas
(id_venta, id_producto, cantidad_kg, cantidad_unidades, precio_unitario, subtotal)
VALUES (%s, %s, %s, %s, %s, %s)
"""

INSERT_PAGO = """
INSERT INTO pagos (id_venta, id_metodo, monto)
VALUES (%s, %s, %s)
"""

DATOS_TICKET = """
SELECT
    p.nombre,
    d.cantidad_kg,
    d.cantidad_unidades,
    d.precio_unitario,
    d.subtotal
FROM detalle_ventas d
JOIN productos p ON p.id_producto = d.id_producto
WHERE d.id_venta = %s
"""
