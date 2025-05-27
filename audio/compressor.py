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

def compress_audio(input_path):
    """Nén file audio bằng Huffman và trả về dữ liệu"""
    # Đọc dữ liệu audio từ file
    with open(input_path, 'rb') as f:
        audio_data = f.read()

    # Đếm tần số ký tự
    freq_table = {}
    for byte in audio_data:
        freq_table[byte] = freq_table.get(byte, 0) + 1

    # Xây cây Huffman và bảng mã
    tree = build_huffman_tree(audio_data)
    codebook = build_code_table(tree)

    # Mã hóa dữ liệu audio
    encoded = encode_data(audio_data, codebook)
    padded_bytes = pad_encoded_data(encoded)

    # Tạo tên file đầu ra với đuôi .audio.huff
    base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi
    output_path = base_name + ".audio.huff"
    
    # Lưu cây Huffman và dữ liệu mã hóa vào cùng một file
    with open(output_path, 'wb') as out:
        pickle.dump((tree, padded_bytes), out)

    # Tính toán thống kê
    stats = {
        "Kích thước gốc (bytes)": len(audio_data),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(audio_data), 2) if len(audio_data) > 0 else 0
    }

    return padded_bytes, codebook, stats

def decompress_audio(input_path, output_path=None):
    """Giải nén file .audio.huff và lưu vào output_path (hoặc mặc định)"""
    # Đọc cây Huffman và dữ liệu mã hóa
    with open(input_path, 'rb') as f:
        tree, byte_data = pickle.load(f)

    # Chuyển byte về chuỗi bit
    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)

    # Loại bỏ padding
    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    # Giải mã dữ liệu
    decoded_bytes = decode_data(bit_str, tree)

    # Tạo tên file đầu ra nếu không được cung cấp
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi .audio.huff
        base_name = base_name.replace(".audio", "")  # Loại bỏ .audio nếu có
        output_path = base_name + "_decoded.mp3"

    # Lưu file giải mã
    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    return output_path