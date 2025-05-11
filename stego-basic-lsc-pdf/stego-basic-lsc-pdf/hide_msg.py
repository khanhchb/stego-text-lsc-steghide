#!/usr/bin/env python3
import sys
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Chuyen doi thong diep thanh chuoi nhi phan
def string_to_bin(message, encoding='utf-8'):
    return ''.join(format(b, '08b') for b in message.encode(encoding))

#Doc tung dong van ban trong file pdf va xac dinh toa do cua chung
'''
def extract_text_and_positions_from_pdf(pdf_file,
                                       start_x=50,
                                       start_y=750,
                                       line_spacing=20,
                                       bottom_margin=50):
    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"Error opening PDF {pdf_file}: {e}")
        sys.exit(1)

    lines = []
    y_positions = []
    usable_height = start_y - bottom_margin
    lines_per_page = int(usable_height // line_spacing)
    total_pages = doc.page_count

    for page_num in range(total_pages):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        idx_in_page = 0
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                if not text:
                    continue
                normal_y = start_y - idx_in_page * line_spacing
                lines.append(text)
                y_positions.append(normal_y)
                idx_in_page += 1
                if idx_in_page >= lines_per_page:
                    break
    doc.close()
    return lines, y_positions, lines_per_page, total_pages
'''

# Ham xu ly giau tin
def hide_message_in_pdf(input_pdf,
                        output_pdf,
                        message,
                        delta_pt=0.24,
                        start_x=50,
                        start_y=750,
                        line_spacing=20,
                        font_name='Helvetica',
                        font_size=12,
                        bottom_margin=50):
                        
    # Xac dinh dong, toa do dong, so dong moi trang va so luong trang trong file pdf dau vao
    lines, base_y, lines_per_page, total_pages = extract_text_and_positions_from_pdf(
        input_pdf, start_x, start_y, line_spacing, bottom_margin)

    bits = string_to_bin(message)
    n_bits = len(bits)

    # Loi neu so dong van ban nho hon do dai chuoi bit
    if len(lines) < n_bits:
        print(f"Error: input PDF has {len(lines)} lines but message needs {n_bits} bits.")
        sys.exit(1)

    # Tao Canva PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont(font_name, font_size)

    positions = []
    total_lines = len(lines)
    
    # Duyet qua tung dong text voi chi so i
    for i, text in enumerate(lines):
        # Tinh trang va vi tri dong moi trang
        page_num = i // lines_per_page
        idx_in_page = i % lines_per_page
        
        # Xu ly khi sang trang moi
        if idx_in_page == 0 and i != 0:
            c.showPage()
            c.setFont(font_name, font_size)

        normal_y = start_y - idx_in_page * line_spacing # Toa do ban dau cua dong
        
        # Phep dich dong, dich len neu giau bit 1, va nguoc lai
        if i < n_bits:
            bit = bits[i]
            y = normal_y + delta_pt if bit == '1' else normal_y - delta_pt
        else:
            y = normal_y
        
        # Ve lai dong van ban len trang PDF theo toa do tinh duoc
        c.drawString(start_x, y, text)
        # Luu lai toa do tung dong van ban
        positions.append(y)

    c.save()
    
    # Ghi toa do tung dong van ban ra file
    with open("positions2.txt", "w") as f:
        for y in positions:
            f.write(f"{y}\n")
    
    print(f"Hidden {n_bits} bits across {total_pages} pages ({total_lines} lines). Output: {output_pdf}")
    print(f"Binary hidden: {bits}")


if __name__ == "__main__":
    input_pdf = 'original.pdf'
    output_pdf = 'output.pdf'

    # Lay thong diep can giau trong file
    try:
        with open("secret_msg.txt", "r", encoding="utf-8") as f:
            secret_message = f.read().strip()
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

    hide_message_in_pdf(input_pdf, output_pdf, secret_message)
