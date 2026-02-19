from ventas.ticket import imprimir_ticket
from config.database import get_connection
from db.queries import DATOS_TICKET
import psycopg2.extras

def reimprimir_ticket(id_venta):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


    cur.execute(DATOS_TICKET, (id_venta,))
    datos = cur.fetchone()

    conn.close()

    imprimir_ticket(
        id_venta=datos["id"],
        cajero=datos["cajero"],
        items=datos["items"],
        total=datos["total"],
        pagos=datos["pagos"],
        vuelto=datos["vuelto"]
    )

