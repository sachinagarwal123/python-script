import io
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys

def add_text_to_pdf(input_pdf, output_pdf, text1, text2, font_path):
    try:
        # Register the font
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    except:
        print(f"Error: Unable to load font from {font_path}. Using default font.")
        font_name = 'Helvetica'  # Use a default font that supports Russian characters

    # Read your existing PDF
    existing_pdf = PdfReader(open(input_pdf, "rb"))
    output = PdfWriter()

    # Get the first page
    page = existing_pdf.pages[0]
    
    # Get page dimensions
    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    # Create a new PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.setFont(font_name, 16)  # Increased font size

    # Add text to the new PDF
    # Positioning is now relative to page dimensions
    can.drawString(page_width * 0.39, page_height * 0.41, text1)  # Center mein, page ke 55% neeche
    can.drawString(page_width * 0.1, page_height * 0.07, text2)  # Left side, about 1/5 up from bottom
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Merge the new PDF with the existing page
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Finally, write "output" to a real file
    output_stream = open(output_pdf, "wb")
    output.write(output_stream)
    output_stream.close()

# Usage
input_pdf = "ttt.pdf"  # Make sure this matches your input PDF name
output_pdf = "certificate_filled.pdf"

# Get user input
text1 = input("Enter the first text in Russian: ")
text2 = input("Enter the second text in Russian: ")

# Default font path (you may need to adjust this)
if sys.platform.startswith('win'):
    default_font = 'C:\\Windows\\Fonts\\arial.ttf'
elif sys.platform.startswith('darwin'):  # macOS
    default_font = '/Library/Fonts/Arial Unicode.ttf'
else:  # Linux and others
    default_font = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

# Ask user for font file path
font_path = input(f"Enter the path to a TrueType font file (press Enter to use default: {default_font}): ")
if not font_path:
    font_path = default_font

if not os.path.exists(font_path):
    print(f"Warning: Font file not found at {font_path}. Using Helvetica font.")
    font_path = None  # This will cause the script to use Helvetica

add_text_to_pdf(input_pdf, output_pdf, text1, text2, font_path)
print(f"Modified PDF saved as {output_pdf}")