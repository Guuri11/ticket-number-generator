from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

# Crear un estilo personalizado
styles = getSampleStyleSheet()
custom_style = ParagraphStyle(
    'custom_style',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=24,
    textColor=colors.white
)

for i in range(1000):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Dibujar el número de iteración en el lienzo
    text = "<b>#{}</b>".format(i)
    p = Paragraph(text, custom_style)
    p.wrapOn(can, 200, 200)
    p.drawOn(can, 160, 75)

    can.save()

    packet.seek(0)

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open("ticket-rifa-sopar.pdf", "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    output_stream = open(f"tickets/ticket-rifa-sopar-{i}.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
