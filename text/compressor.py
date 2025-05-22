import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_file(input_path):
    """Nén file văn bản bằng Huffman và trả về dữ liệu"""
    with open(input_path, 'rb') as f:
        text = f.read()

    # Đếm tần số ký tự
    freq_table = {}
    for ch in text:
        freq_table[ch] = freq_table.get(ch, 0) + 1

    # Xây cây Huffman và bảng mã
    tree = build_huffman_tree(text)
    codebook = build_code_table(tree)

    # Mã hóa văn bản
    encoded = encode_data(text, codebook)
    padded_bytes = pad_encoded_data(encoded)

    output_path = input_path + ".huff"
    with open(output_path, 'wb') as out:
        pickle.dump((tree, padded_bytes), out)

    stats = {
        "Kích thước gốc (bytes)": len(text),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(text), 2) if len(text) > 0 else 0
    }

    return padded_bytes, codebook, stats

def decompress_file(input_path, output_path=None):
    """Giải nén file .huff và lưu vào output_path (hoặc mặc định)"""
    with open(input_path, 'rb') as f:
        tree, byte_data = pickle.load(f)

    # Chuyển byte về chuỗi bit
    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)

    # Loại bỏ padding
    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    # Giải mã
    decoded_bytes = decode_data(bit_str, tree)

    # Lưu kết quả
    if output_path is None:
        output_path = input_path.replace(".huff", "_decoded.txt")

    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    return output_path