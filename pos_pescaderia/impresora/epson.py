import win32print

def imprimir_ticket(texto):
    printer = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer)

    hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
    win32print.StartPagePrinter(hPrinter)

    win32print.WritePrinter(hPrinter, texto.encode("cp437", "ignore"))

    win32print.EndPagePrinter(hPrinter)
    win32print.EndDocPrinter(hPrinter)
    win32print.ClosePrinter(hPrinter)


import win32print
import win32ui
import win32con


NOMBRE_IMPRESORA = "EPSON TM-U220 Receipt"  
# ⚠️ Debe coincidir EXACTO con el nombre en Windows


def imprimir(texto):
    hprinter = win32print.OpenPrinter(NOMBRE_IMPRESORA)
    try:
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(NOMBRE_IMPRESORA)

        hdc.StartDoc("Ticket POS")
        hdc.StartPage()

        y = 100
        for linea in texto.split("\n"):
            hdc.TextOut(100, y, linea)
            y += 20

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

    finally:
        win32print.ClosePrinter(hprinter)

from datetime import datetime
from escpos.printer import Usb

# VID / PID comunes Epson TM-U220
# Si no imprime, los ajustamos
VENDOR_ID = 0x04b8   # Epson
PRODUCT_ID = 0x0202 # TM-U220


