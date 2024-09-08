import io
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_blank_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.save()

def add_text_to_pdf(input_pdf, output_pdf, text1, text2, x1, y1, x2, y2, font_path):
    try:
        # Register the font
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    except:
        print(f"Error: Unable to load font from {font_path}. Using default font.")
        font_name = 'Helvetica'  # Use a default font that supports Russian characters

    # Create a new PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont(font_name, 12)

    # Add text to the new PDF
    can.drawString(x1, y1, text1)
    can.drawString(x2, y2, text2)
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Read your existing PDF
    existing_pdf = PdfReader(open(input_pdf, "rb"))
    output = PdfWriter()

    # If the existing PDF is empty, use the new PDF page
    if len(existing_pdf.pages) == 0:
        output.add_page(new_pdf.pages[0])
    else:
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # Finally, write "output" to a real file
    output_stream = open(output_pdf, "wb")
    output.write(output_stream)
    output_stream.close()

# Usage
input_pdf = "input.pdf"
output_pdf = "output.pdf"

# Create input.pdf if it doesn't exist
if not os.path.exists(input_pdf):
    print(f"{input_pdf} does not exist. Creating a blank PDF.")
    create_blank_pdf(input_pdf)

# Get user input
text1 = input("Enter the first text in Russian: ")
text2 = input("Enter the second text in Russian: ")

# You can adjust these coordinates as needed
x1, y1 = 100, 700  # coordinates for text1
x2, y2 = 100, 680  # coordinates for text2

# Ask user for font file path
default_font = 'C:\\Windows\\Fonts\\arial.ttf'  # Default Windows font path
font_path = input(f"Enter the path to a TrueType font file (press Enter to use default: {default_font}): ")
if not font_path:
    font_path = default_font

if not os.path.exists(font_path):
    print(f"Warning: Font file not found at {font_path}. Using default font.")
    font_path = default_font

add_text_to_pdf(input_pdf, output_pdf, text1, text2, x1, y1, x2, y2, font_path)
print(f"Modified PDF saved as {output_pdf}")