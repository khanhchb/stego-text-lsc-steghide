#!/usr/bin/env python3
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
'''
    Doc file van ban dau vao va sinh file PDF voi dinh dang
    ho tro nhieu trang, can chinh font, xu ly ngat trang.
    '''
def generate_original_pdf(input_txt,
                          output_pdf,
                          start_x=50,
                          start_y=750,
                          line_spacing=20,
                          font_name='Helvetica',
                          font_size=12,
                          bottom_margin=50):
    
    # Doc tat ca dong van ban (chi lay dong co noi dung)
    with open(input_txt, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f if line.strip() != '']


    # Tao canvas PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont(font_name, font_size)

    # Tinh so dong toi da tren moi trang
    usable_height = start_y - bottom_margin
    lines_per_page = int(usable_height // line_spacing)
    positions = []

    for i, line in enumerate(lines):
        # Tinh trang va vi tri dong moi trang
        page_num = i // lines_per_page
        index_in_page = i % lines_per_page

        # Xu ly khi can sang trang moi
        '''
        if index_in_page == 0 and i != 0:
            c.showPage()
            c.setFont(font_name, font_size)
        '''

        # Tinh toa do Y
        y = start_y - index_in_page * line_spacing
        # Ve lai dong van ban len trang PDF theo dung toa do
        c.drawString(start_x, y, line)
        # Luu lai toa do tung dong
        positions.append(y)

    c.save()
    
    # Ghi toa do tung dong van ban ra file
    with open("positions1.txt", "w") as f:
        for y in positions:
            f.write(f"{y}\n")
            
    print(f"Generated original PDF: {output_pdf} ({len(lines)} lines across {page_num+1} pages)")

if __name__ == "__main__":
    input_file = 'input.txt' 
    output_file = 'original.pdf'
    generate_original_pdf(input_file, output_file)

