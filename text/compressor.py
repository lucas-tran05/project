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

def compress_file(input_path):
    with open(input_path, 'rb') as f:
        text = f.read()

    freq_table = {}
    for ch in text:
        freq_table[ch] = freq_table.get(ch, 0) + 1

    tree = build_huffman_tree(text)
    codebook = build_code_table(tree)

    encoded = encode_data(text, codebook)
    padded_bytes = pad_encoded_data(encoded)

    output_path = input_path + ".huff"
    with open(output_path, 'wb') as out:
        original_ext = os.path.splitext(input_path)[1]  # .txt hoặc .docx
        pickle.dump((tree, padded_bytes, original_ext), out)

    stats = {
        "Kích thước gốc (bytes)": len(text),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(text), 2) if len(text) > 0 else 0
    }

    return padded_bytes, codebook, stats

def decompress_file(input_path, output_path=None):
    with open(input_path, 'rb') as f:
        data = pickle.load(f)
        if len(data) == 3:
            tree, byte_data, original_ext = data
        else:
            tree, byte_data = data
            original_ext = ".txt" 

    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)

    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    decoded_bytes = decode_data(bit_str, tree)

    if output_path is None:
        original_name = os.path.basename(input_path).replace(".huff", "").replace(".text", "")
        output_path = os.path.join(
            os.path.dirname(input_path),
            f"DECODE_{original_name}{original_ext}"
        )


    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)



    return output_path