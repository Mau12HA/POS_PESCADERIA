from config.database import get_connection

def registrar_accion(id_usuario, accion, detalle=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO historial_acciones (id_usuario, accion, detalle)
        VALUES (%s, %s, %s)
    """, (id_usuario, accion, detalle))

    conn.commit()
    conn.close()
