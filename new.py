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


    def center_text(text, width):
        text_width = can.stringWidth(text, font_name, 16)
        return (width - text_width) / 2
    
    print(len(text1))
    
    if len(text1) <= 5:
        x1 = center_text(text1, page_width)
    elif 5 < len(text1) <= 10:
        x1 = page_width * 0.46
    elif 10 < len(text1) <= 15:
        x1 = page_width * 0.44
    elif 15 < len(text1) <= 20:
        x1 = page_width * 0.42
    elif 21 < len(text1) <= 40:
        x1 = page_width * 0.35
    else:
        x1 = page_width * 0.40
    
    can.drawString(x1, page_height * 0.41, text1)

    print(len(text2))
    if len(text2) <= 5:
        x2 = page_width * 0.11
    elif 5 < len(text2) <= 10:
        x2 = page_width * 0.11
    elif 10 < len(text2) <= 15:
        x2 = page_width * 0.09
    elif 15 < len(text2) <= 20:
        x2 = page_width * 0.07
    elif 20 < len(text2) <= 40:
        x2 = page_width * 0.03
    else:
        x2 = page_width * 0.05

    can.drawString(x2, page_height * 0.07, text2)
    can.save()

    # Add text to the new PDF
    # Positioning is now relative to page dimensions
    # if len(text1) < 5:
    #     can.drawString(page_width * 0.48, page_height * 0.41, text1)
    #     if len(text2) < 5:
    #         # can.drawString(page_width * 0.48, page_height * 0.41, text1)  # Center mein, page ke 55% neeche
    #         can.drawString(page_width * 0.13, page_height * 0.07, text2)
    #     else:

    #         can.drawString(page_width * 0.13, page_height * 0.07, text2)

    #      # Center mein, page ke 55% neeche
    #     # can.drawString(page_width * 0.13, page_height * 0.07, text2) 

    # if len(text1) > 10 and len(text1)<15:
    #     if len(text2) 
    #     can.drawString(page_width * 0.44, page_height * 0.41, text1)  # Center mein, page ke 55% neeche
    #     can.drawString(page_width * 0.08, page_height * 0.07, text2)  # Left side, about 1/5 up from bottom
    # if len(text1) > 15:
    #     can.drawString(page_width * 0.4, page_height * 0.41, text1)  # Center mein, page ke 55% neeche
    #     can.drawString(page_width * 0.03, page_height * 0.07, text2)  #
    # can.save()

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
