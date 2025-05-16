import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_file(input_path):
    """Nén file văn bản bằng Huffman và lưu vào file .huff"""
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Đếm tần số ký tự
    freq_table = {}
    for ch in text:
        freq_table[ch] = freq_table.get(ch, 0) + 1

    # Xây cây Huffman và bảng mã
    tree = build_huffman_tree(freq_table)
    codebook = build_code_table(tree)

    # Mã hóa văn bản
    encoded = encode_data(text, codebook)
    padded = pad_encoded_data(encoded)

    # Chuyển thành byte và lưu
    byte_data = bytearray(int(padded[i:i+8], 2) for i in range(0, len(padded), 8))
    output_path = input_path + ".huff"

    with open(output_path, 'wb') as out:
        pickle.dump((tree, byte_data), out)

def decompress_file(input_path):
    """Giải nén file .huff thành file văn bản gốc"""
    with open(input_path, 'rb') as f:
        tree, byte_data = pickle.load(f)

    # Chuyển byte về chuỗi bit
    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)

    # Giải mã
    decoded_text = decode_data(bit_str, tree)

    # Lưu kết quả
    output_path = input_path.replace(".huff", "_decoded.txt")
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(decoded_text)