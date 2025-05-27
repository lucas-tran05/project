# Project: A data encryption and decryption application using the Huffman algorithm with a graphical user interface.
# To fulfil the requirement of FIT Course by Pham@PTIT
# Tran Quoc Cuong - B23DCAT034 - 13
# Duong Thien Ngan - B23DCAT209 - 13
# Le Van Duy - B23DCAT074 - 13

import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_image(input_path):
    with open(input_path, 'rb') as f:
        image_data = f.read()

    freq_table = {}
    for byte in image_data:
        freq_table[byte] = freq_table.get(byte, 0) + 1

    tree = build_huffman_tree(image_data)
    codebook = build_code_table(tree)

    encoded = encode_data(image_data, codebook)
    padded_bytes = pad_encoded_data(encoded)

    base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi
    output_path = base_name + ".image.huff"
    
    with open(output_path, 'wb') as out:
        pickle.dump((tree, padded_bytes), out)

    stats = {
        "Kích thước gốc (bytes)": len(image_data),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(image_data), 2) if len(image_data) > 0 else 0
    }

    return padded_bytes, codebook, stats

def decompress_image(input_path, output_path=None):
    with open(input_path, 'rb') as f:
        tree, byte_data = pickle.load(f)

    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)

    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    decoded_bytes = decode_data(bit_str, tree)

    if output_path is None:
        base_name = os.path.splitext(input_path)[0]  
        base_name = base_name.replace(".image", "")  
        original_ext = os.path.splitext(base_name)[1] or ".png"
        output_path = base_name

    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    return output_path