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

DATOS_VENTA = """
SELECT v.id_venta,
       v.total,
       u.nombre AS cajero
FROM ventas v
JOIN usuarios u ON v.id_usuario = u.id_usuario
WHERE v.id_venta = %s
"""

DETALLE_TICKET = """
SELECT p.nombre,
       d.cantidad_kg,
       d.cantidad_unidades,
       d.precio_unitario,
       d.subtotal
FROM detalle_ventas d
JOIN productos p ON d.id_producto = p.id_producto
WHERE d.id_venta = %s
"""

PAGOS_TICKET = """
SELECT m.nombre,
       p.monto
FROM pagos p
JOIN metodos_pago m ON p.id_metodo = m.id_metodo
WHERE p.id_venta = %s
"""