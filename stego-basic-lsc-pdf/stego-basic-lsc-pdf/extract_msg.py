#!/usr/bin/env python3
import sys
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter

PAGE_WIDTH, PAGE_HEIGHT = letter

# Ham trich xuat danh sach dong va vi tri Y thuc te tu PDF
def extract_text_and_actual_positions(pdf_file):
    # Mo file PDF
    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"Error opening PDF {pdf_file}: {e}")
        sys.exit(1)

    lines = []
    actual_y = []

    # Doc tung dong van ban trong file PDF va trich xuat toa do cua chung
    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                spans = line.get('spans', [])
                if not spans:
                    continue
                text = ''.join(s['text'] for s in spans).strip()
                if not text:
                    continue
                # Lay y thuc te tu bbox baseline
                fitz_y = spans[0]['bbox'][1]
                # Chuyen sang he toa do reportlib
                y = PAGE_HEIGHT - fitz_y
                # Luu noi dung text cua dong
                lines.append(text)
                # Luu toa do dong
                actual_y.append(y)
    doc.close()
    return lines, actual_y

# Ham thuc hien tach tin
def extract_message(original_pdf,
                    encoded_pdf,
                    delta_pt=0.24,
                    tol=0.1):
    # Trich xuat van ban va vi tri thuc te
    lines_o, y_o = extract_text_and_actual_positions(original_pdf)
    lines_e, y_e = extract_text_and_actual_positions(encoded_pdf)

    # Loi neu so dong trong 2 file khong dong nhat
    if len(lines_o) != len(lines_e):
        print(f"Error: line counts differ: {len(lines_o)} vs {len(lines_e)}")
        sys.exit(1)

    bits = []
    
    # Tach tin bang cach so sanh vi tri dong ban dau va sau khi dich
    for i, (yo, ye) in enumerate(zip(y_o, y_e)):
        deviation = ye - yo
        if abs(deviation) < tol:
            continue
        # Can xu ly lai logic tai day (hint: phep cong tru) 
        if abs(deviation + delta_pt) < tol:
            bits.append('1')
        elif abs(deviation - delta_pt) < tol:
            bits.append('0')
        else:
            print(f"Warning: deviation at line {i} = {deviation:.3f} not recognized")
            continue

    # Noi cac bit lai thanh chuoi
    binary_str = ''.join(bits)
    
    # Chuyen doi chuoi nhi phan thanh chuoi ky tu
    n = len(binary_str) - (len(binary_str) % 8)
    binary_trimmed = binary_str[:n]
    message = ''
    for i in range(0, n, 8):
        byte = binary_trimmed[i:i+8]
        message += chr(int(byte, 2))

    print("Extraction complete.")
    print(f"Total bits found: {len(bits)}")
    print(f"Binary string: {binary_str}")
    print(f"Decoded message: {message}")


if __name__ == '__main__':
    orig = 'original.pdf'
    enc = 'output.pdf'
    extract_message(orig, enc)
