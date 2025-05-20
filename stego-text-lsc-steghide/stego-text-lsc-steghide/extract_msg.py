#!/usr/bin/env python3
import sys
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter

PAGE_WIDTH, PAGE_HEIGHT = letter

def extract_text_and_actual_positions(pdf_file):
    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"Error opening PDF {pdf_file}: {e}")
        sys.exit(1)

    lines = []
    actual_y = []

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
                fitz_y = spans[0]['bbox'][1]
                y = PAGE_HEIGHT - fitz_y
                lines.append(text)
                actual_y.append(y)
    doc.close()
    return lines, actual_y

def extract_message(original_pdf,
                    encoded_pdf,
                    start_line,  
                    delta_pt=0.24,
                    tol=0.1):
    
    lines_o, y_o = extract_text_and_actual_positions(original_pdf)
    lines_e, y_e = extract_text_and_actual_positions(encoded_pdf)

    if len(lines_o) != len(lines_e):
        print(f"Error: line counts differ: {len(lines_o)} vs {len(lines_e)}")
        sys.exit(1)

    bits = []
    for i, (yo, ye) in enumerate(zip(y_o, y_e)):
        if i < start_line:
            continue
        deviation = ye - yo
        if abs(deviation) < tol:
            continue
        if abs(deviation - delta_pt) < tol:
            bits.append('1')
        elif abs(deviation + delta_pt) < tol:
            bits.append('0')
        else:
            print(f"Warning: deviation at line {i} = {deviation:.3f} not recognized")
            continue

    binary_str = ''.join(bits)
    '''
    #Code chuyen doi nhi phan sang ky tu
    n = len(binary_str) - (len(binary_str) % 8)
    binary_trimmed = binary_str[:n]
    message = ''
    for i in range(0, n, 8):
        byte = binary_trimmed[i:i+8]
        message += chr(int(byte, 2))
    '''
    
    print("Extraction complete.")
    print(f"Total bits found: {len(bits)}")
    print(f"Binary string: {binary_str}")
    #print(f"Decoded message: {message}")

if __name__ == '__main__':
    orig = 'original.pdf'
    enc = 'output.pdf'
    #Dien vi tri dong bat dau tach tin
    extract_message(orig, enc, start_line=)
