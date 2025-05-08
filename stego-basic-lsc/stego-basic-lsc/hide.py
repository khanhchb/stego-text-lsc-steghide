#!/usr/bin/env python3
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def hide_message_in_pdf(input_txt, output_pdf, bits,
                        delta_pt=0.5,
                        start_x=50,
                        start_y=750,
                        line_spacing=20,
                        font_name='Helvetica',
                        bottom_margin=50):  

    #Doc tung dong van ban, bo qua ky tu "\n"
    with open(input_txt, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    n_bits = len(bits)

    #Kiem tra van ban dau vao co du so dong de giau thong diep khong
    if len(lines) < n_bits:
        print(f"Error: The input file has {len(lines)} lines, while length of the binary string is {n_bits} bits!")
        sys.exit(1)

    #Tao trang PDF moi
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont(font_name, 12)

    positions = []
    bit_index = 0
    lines_per_page = int((start_y - bottom_margin) // line_spacing) #Tong so dong van ban trong 1 trang

    for i, line in enumerate(lines):
        page_num = i // lines_per_page
        index_in_page = i % lines_per_page
        y = start_y - index_in_page * line_spacing #Xac dinh toa do dong
        
        #Sang trang
        if i == lines_per_page:
            c.showPage()
            c.setFont(font_name, 12)

        #Thuat toan giau tin, quy uoc bit 0 dich xuong, bit 1 dich len
        if bit_index < n_bits:
            bit = bits[bit_index]
            offset = -delta_pt if bit == '0' else delta_pt
            y_adj = y + offset
            positions.append(y_adj)
            bit_index += 1
        else:
            y_adj = y #Neu da giau het bit, ngung viec thay doi vi tri dong

        #In van ban ra file pdf
        c.drawString(start_x, y_adj, line)

    c.save()

    #Tao file positions va dien toa do cac dong van ban sau khi giau tin vao
    with open("positions.txt", "w") as f:
        for y in positions:
            f.write(f"{y}\n")

    #In ra thong bao giau tin thanh cong
    print(f"Successfully hide {n_bits} bits into file {output_pdf}")

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.pdf'
    #Dan chuoi nhi phan vao day
    secret_bits = ''
    hide_message_in_pdf(input_file, output_file, secret_bits)
