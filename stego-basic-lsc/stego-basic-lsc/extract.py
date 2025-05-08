#!/usr/bin/env python3
import sys

def extract_message_from_pdf(positions_file,
                              delta_pt=0.5,
                              page_height=792,
                              start_y=750,
                              line_spacing=20,
                              bottom_margin=50):

    #Lay ra toa do cac dong van ban sau khi giau
    with open(positions_file, 'r') as f:
        actual_positions = [float(line.strip()) for line in f]

    #Xac dinh so dong toi da trong 1 trang
    usable_height = start_y - bottom_margin
    lines_per_page = int(usable_height // line_spacing)

    bits = []

    for i in range(len(actual_positions)):
        actual_y = actual_positions[i] #Toa do hien tai cua dong van ban
        page_num = i // lines_per_page
        index_in_page = i % lines_per_page

        normal_y = start_y - index_in_page * line_spacing #Xac dinh toa do goc cua tung dong van ban
        deviation = actual_y - normal_y

        #Tach tin: Neu toa do goc < toa do moi thi lay ra bit 1, va nguoc lai
        if deviation > 0:
            bits.append('1')
        elif deviation < 0:
            bits.append('0')
        else:
            bits.append('?')

    #Noi cac bit lai thanh chuoi nhi phan
    binary_string = ''.join(bits)
    print("Successfully extract hidden bits!")
    print(f"Binary string: {binary_string}")
    
''' #Chuyen doi chuoi nhi phan sang chuoi ky tu
    ascii_str = ''.join(chr(int(binary_string[i:i+8], 2))
                        for i in range(0, len(binary_string), 8))
    print(f"Secret message: {ascii_str}")
'''

if __name__ == "__main__":
    extract_message_from_pdf("positions.txt")
