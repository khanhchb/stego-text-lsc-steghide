#!/usr/bin/env python3

#Ham chuyen chuoi ky tu sang chuoi nhi phan
def string_to_bin(message, encoding='utf-8'):
    return ''.join(format(byte, '08b') for byte in message.encode(encoding))

if __name__ == "__main__":
    input_file = "secret_message.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            message = f.read().strip()

        binary_string = string_to_bin(message) #Noi cac bit lai thanh chuoi nhi phan
        print("Converted to binary string!")
        print(f"Secret message: {message}")
        print(f"Binary string: {binary_string}")

    except FileNotFoundError:
        print(f"File {input_file} not found!")
