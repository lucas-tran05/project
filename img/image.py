import os
import json
from utils.huffman import (
    build_huffman_tree,
    build_code_table,
    encode_data,
    decode_data,
    pad_encoded_data
)

def encode(image_path):
    # Đọc file ảnh (dưới dạng byte)
    with open(image_path, 'rb') as image:
        original_bytes = image.read()

    # Xây cây Huffman và tạo bảng mã
    tree = build_huffman_tree(original_bytes)
    code_table = build_code_table(tree)

    # Mã hóa dữ liệu
    encoded_bits = encode_data(original_bytes, code_table)

    # Padding và chuyển thành bytes
    padded_data = pad_encoded_data(encoded_bits)

    # Tạo đường dẫn lưu
    base_path = os.path.splitext(image_path)[0]
    huff_path = base_path + '.huff'
    map_path = base_path + '.map'

    # Lưu file nén
    with open(huff_path, 'wb') as f:
        f.write(padded_data)

    # Lưu bảng mã Huffman
    json_table = {k.decode('latin1'): v for k, v in code_table.items()}
    with open(map_path, 'w') as f:
        json.dump(json_table, f)

    # Trả về thống kê
    stats = {
        "Kích thước gốc (byte)": len(original_bytes),
        "Kích thước nén (byte)": len(padded_data),
        "Tỉ lệ nén": f"{len(original_bytes) / len(padded_data):.2f}"
    }

    return padded_data, code_table, stats

def decode(huff_path):
    # Đọc file nén đã padding
    with open(huff_path, 'rb') as f:
        compressed_bytes = f.read()

    # Gỡ padding: lấy số bit đệm từ 8 bit đầu
    bit_string = ''.join(bin(byte)[2:].rjust(8, '0') for byte in compressed_bytes)
    extra_padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-extra_padding] if extra_padding > 0 else bit_string

    # Đọc bảng mã Huffman
    map_path = os.path.splitext(huff_path)[0] + '.map'
    with open(map_path, 'r') as f:
        json_table = json.load(f)
    code_table = {k.encode('latin1'): v for k, v in json_table.items()}

    # Giải mã dữ liệu
    decoded_bytes = decode_data(bit_string, code_table)

    # Lưu ảnh đã giải nén
    out_path = os.path.splitext(huff_path)[0] + '_decompressed.jpg'
    with open(out_path, 'wb') as f:
        f.write(decoded_bytes)

    return out_path
