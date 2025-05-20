#!/usr/bin/env python3
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_original_pdf(input_txt,
                          output_pdf,
                          start_x=50,
                          start_y=750,
                          line_spacing=20,
                          font_name='Helvetica',
                          font_size=12,
                          bottom_margin=50):
    
    with open(input_txt, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f if line.strip() != '']

    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont(font_name, font_size)

    usable_height = start_y - bottom_margin
    lines_per_page = int(usable_height // line_spacing)

    for i, line in enumerate(lines):
        page_num = i // lines_per_page
        index_in_page = i % lines_per_page

        if index_in_page == 0 and i != 0:
            c.showPage()
            c.setFont(font_name, font_size)

        y = start_y - index_in_page * line_spacing
        c.drawString(start_x, y, line)

    c.save()
    print(f"Generated original PDF: {output_pdf} ({len(lines)} lines across {page_num+1} pages)")

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'original.pdf'
    generate_original_pdf(input_file, output_file)

